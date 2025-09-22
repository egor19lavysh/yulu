from aiogram import Router, F, Bot
from .intro import Sections, get_back_to_types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk4.listening.service import service as listening_service
from hsk4.reading.service import service as reading_service
from hsk4.writing.service import service as writing_service

router = Router()

###
CALLBACK_FULL_VARIANT = "hsk4_full"

TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_FULL_TEST_COMPLETED = "Полный тест HSK4 завершен! 🎉"
TEXT_MOVING_TO_READING = "Переходим к части \"Чтение\" 📖"
TEXT_MOVING_TO_WRITING = "Переходим к части \"Письмо\" ✏️"


class MockMessage:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat = MockChat(chat_id)
        self.chat_id = chat_id

    async def answer(self, text, **kwargs):
        return await self.bot.send_message(self.chat_id, text, **kwargs)

    async def delete(self):
        pass  # Заглушка для метода delete


class MockChat:
    def __init__(self, chat_id):
        self.id = chat_id


class MockCallback:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.message = MockMessage(bot, chat_id)

    async def answer(self):
        pass  # Заглушка для метода answer


@router.callback_query(F.data == Sections.full_test)
async def show_all_variants(callback: CallbackQuery):
    listening_vars = len(listening_service.get_listening_variants())
    reading_vars = len(reading_service.get_reading_variants())
    writing_vars = len(writing_service.get_writing_variants())

    min_vars_count = min(listening_vars, writing_vars, reading_vars)

    builder = InlineKeyboardBuilder()
    for num in range(min_vars_count):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num + 1}",
                callback_data=f"{CALLBACK_FULL_VARIANT}_{num + 1}"
            )
        )
    builder.adjust(1)

    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_FULL_VARIANT))
async def start_full_variant(callback: CallbackQuery, state: FSMContext):
    variant_index = int(callback.data.split("_")[-1]) - 1

    listening_var_id = listening_service.get_listening_variants()[variant_index].id
    reading_var_id = reading_service.get_reading_variants()[variant_index].id
    writing_var_id = writing_service.get_writing_variants()[variant_index].id

    await state.update_data(
        variant_id=listening_var_id,
        reading_variant_id=reading_var_id,
        writing_variant_id=writing_var_id,
        total_score=0,
        variant_score=0,
        is_full_test=True,
        listening_score=0,
        reading_score=0,
        writing_score=0
    )

    from hsk4.listening.handlers import start_listening_variant
    await start_listening_variant(callback, state)


async def move_to_reading_part(bot: Bot, chat_id: int, state: FSMContext):
    """Переход к части чтения в полном тесте"""
    await bot.send_message(chat_id, TEXT_MOVING_TO_READING)

    data = await state.get_data()
    reading_var_id = data["reading_variant_id"]

    await state.update_data(
        variant_id=reading_var_id,
        total_score=0,
        chat_id=chat_id
    )

    mock_callback = MockCallback(bot, chat_id)
    from hsk4.reading.handlers import start_reading_variant
    await start_reading_variant(mock_callback, state)


async def move_to_writing_part(bot: Bot, chat_id: int, state: FSMContext):
    """Переход к части письма в полном тесте"""
    await bot.send_message(chat_id, TEXT_MOVING_TO_WRITING)

    data = await state.get_data()
    writing_var_id = data["writing_variant_id"]

    await state.update_data(
        variant_id=writing_var_id,
        total_score=0,
        chat_id=chat_id
    )

    mock_callback = MockCallback(bot, chat_id)
    from hsk4.writing.handlers import start_writing_variant
    await start_writing_variant(mock_callback, state)


async def finish_full_test(bot: Bot, chat_id: int, state: FSMContext):
    """Завершение полного теста с выводом итогов"""
    data = await state.get_data()
    listening_score = data.get("listening_score", 0)
    reading_score = data.get("reading_score", 0)
    writing_score = data.get("writing_score", 0)

    total_full_score = listening_score + reading_score + writing_score

    result_text = f"""
{TEXT_FULL_TEST_COMPLETED}

📊 Результаты по частям:
🎧 Аудирование: <b>{listening_score}/45</b>
📖 Чтение: <b>{reading_score}/40</b>
✏️ Письмо: <b>{writing_score}/15</b> +5 возможных баллов

🏆 Итоговый результат: <b>{total_full_score}/100</b> +5 возможных баллов
"""

    await bot.send_message(chat_id, result_text)
    await state.clear()
    await get_back_to_types(bot, chat_id, Sections.full_test)