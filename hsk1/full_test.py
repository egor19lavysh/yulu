from aiogram import Router, F, Bot
from .intro import Sections, get_back_to_types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk1.listening.service import service as listening_service
from hsk1.reading.service import service as reading_service


router = Router()

###
CALLBACK_FULL_VARIANT = "hsk1_full"

TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_FULL_TEST_COMPLETED = "Полный тест HSK1 завершен! 🎉"
TEXT_MOVING_TO_READING = "Переходим к части \"Чтение\" 📖"


@router.callback_query(F.data == Sections.full_test)
async def show_all_variants(callback: CallbackQuery):
    listening_vars = len(listening_service.get_listening_variants())
    reading_vars = len(reading_service.get_reading_variants())

    min_vars_count = min(listening_vars, reading_vars)

    builder = InlineKeyboardBuilder()
    for num in range(min_vars_count):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num + 1}",
                callback_data=f"{CALLBACK_FULL_VARIANT}_{num + 1}"
            )
        )
    builder.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_sections_hsk1"
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

    await state.update_data(
        listening_variant_id=listening_var_id,
        reading_variant_id=reading_var_id,
        variant_score=0,
        is_full_test=True,
        listening_score=0,
        reading_score=0,
    )

    from hsk1.listening.handlers import start_listening_variant
    await start_listening_variant(callback, state)

async def finish_full_test(bot: Bot, state: FSMContext):
    """Завершение полного теста с выводом итогов"""
    data = await state.get_data()
    listening_score = data.get("listening_score", 0)
    reading_score = data.get("reading_score", 0)
    chat_id = data["chat_id"]
    
    total_full_score = listening_score + reading_score

    result_text = f"""
{TEXT_FULL_TEST_COMPLETED}

📊 Результаты по частям:
🎧 Аудирование: <b>{listening_score}/20</b>
📖 Чтение: <b>{reading_score}/20</b>

🏆 Итоговый результат: <b>{total_full_score}/40</b>
"""

    await bot.send_message(chat_id, result_text)
    await state.clear()
    await get_back_to_types(bot, chat_id, Sections.full_test)