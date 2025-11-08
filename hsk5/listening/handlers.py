from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk5.intro import Sections, get_back_to_types
from .service import get_listening_service
from .states import HSK5ListeningStates
import asyncio


router = Router()
service = asyncio.run(get_listening_service())

### Callback значения
CALLBACK_LISTENING_VARIANT = "hsk5_listening_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"
TEXT_NO_TASKS = "Задания не найдены."
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_TASKS_COMPLETED = "Общий результат: <b>{score}/{total}</b>"

TEXT_TASK_1 = "Прослушайте диалоги (или монологи) и ответьте на вопросы:"

TEXT_TRUE = "Правда"
TEXT_FALSE = "Ложь"

ANSWER_RIGHT = "✅ Верно!"
ANSWER_FALSE = "❌ Неверно!"


@router.callback_query(F.data == Sections.listening)
async def show_listening_variants(callback: CallbackQuery):
    variants = await service.get_listening_variants()
    builder = InlineKeyboardBuilder()
    for num, variant in enumerate(variants, start=1):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num}",
                callback_data=f"{CALLBACK_LISTENING_VARIANT}_{variant.id}"
            )
        )
    builder.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_sections_hsk5"
            )
        )
    builder.adjust(1)
    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_LISTENING_VARIANT))
async def start_listening(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()

    var_id = int(callback.data.split("_")[-1])
    await state.update_data(variant_id=var_id,
                            chat_id=callback.message.chat.id)
    await start_listening_variant(callback.bot, state)


async def start_listening_variant(bot: Bot, state: FSMContext):
    data = await state.get_data()

    if data.get("listening_variant_id", False):
        var_id = data["listening_variant_id"]
    else:
        var_id = data["variant_id"]

    chat_id = data["chat_id"]
    variant = await service.get_listening_variant(variant_id=var_id)

    if not variant:
        await bot.send_message(chat_id, "Вариант не найден.")
        return

    # Сохраняем данные варианта в состояние
    await state.update_data(
        total_score=0,
        variant_id=var_id 
    )

    await bot.send_audio(chat_id, variant.audio_id)
    await start_part_1(bot, state)


async def start_part_1(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := await service.get_first_tasks_by_variant(variant_id=variant_id):
        await state.update_data(
            tasks=tasks,
            index=0,
            score=0
        )

        await bot.send_message(chat_id, TEXT_TASK_1)
        await bot.send_message(chat_id, TEXT_PART_1)
        await handle_first_tasks(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим к концу варианта")
        await finish_listening(bot, state)

    
async def handle_first_tasks(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    score = data["score"]
    tasks = data["tasks"]
    index = data["index"]


    if index < len(tasks):
        curr_task = tasks[index]
        
        if index == 20: # Костыль для 2 задания
            await bot.send_message(chat_id, TEXT_PART_2)

        options = [f"{op.letter}. {op.text}" for op in curr_task.options]

        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            correct_option_id=ord(curr_task.correct_letter) - ord("A"),
            is_anonymous=False,
            question=f"Задание {2 if index >= 20 else 1}, Вопрос {index + 1 - 20 if index >= 20 else index + 1}/{25 if index >= 20 else 20}",
            type="quiz"
        )

        await state.set_state(HSK5ListeningStates.answer)
    else:
        await state.update_data(
            total_score=data["total_score"] + score
        )
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=45))
        await finish_listening(bot, state)

@router.poll_answer(HSK5ListeningStates.answer)
async def handle_first_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    tasks = data["tasks"]
    index = data["index"]
    curr_question = tasks[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_question.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_first_tasks(bot=poll_answer.bot, state=state)

async def finish_listening(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    total_score = data["total_score"]

    if data.get("is_full_test", False):
        await state.update_data(
            listening_score=total_score
        )
        await bot.send_message(
            chat_id=chat_id,
            text=f"Аудирование завершено!\nПереходим к чтению."
        )

        from hsk5.reading.handlers import start_reading_variant
        await start_reading_variant(bot=bot, state=state)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\n{TEXT_ALL_TASKS_COMPLETED.format(score=total_score, total=45)}"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.listening)