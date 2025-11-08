from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk4.intro import Sections, get_back_to_types
from .service import get_listening_service
from .states import ListeningThirdStates, ListeningSecondStates
import asyncio


router = Router()
service = asyncio.run(get_listening_service())

### Callback значения
CALLBACK_LISTENING_VARIANT = "hsk4_listening_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_PART_3 = "Задание 3"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"
TEXT_NO_TASKS = "Задания не найдены."
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_TASKS_COMPLETED = "Общий результат: <b>{score}/{total}</b>"

TEXT_TASK_1 = "Прослушайте краткие отрывки, и выберите истинны ли утверждения к ним или нет:"
TEXT_TASK_2 = "Прослушайте диалоги между двумя людьми, и ответьте на поставленный диктором вопрос:"
TEXT_TASK_3 = "Прослушайте диалоги или монологи (4-5 предложений), и ответьте на 1-2 вопроса:"

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
                callback_data="back_to_sections_hsk4"
            )
        )
    builder.adjust(1)
    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_LISTENING_VARIANT))
async def start_listening(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])
    await state.update_data(variant_id=var_id)
    await start_listening_variant(callback, state)


async def start_listening_variant(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    var_id = data["variant_id"]
    variant = await service.get_listening_variant(variant_id=var_id)

    if not variant:
        await callback.message.answer("Вариант не найден.")
        await callback.answer()
        return

    # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=var_id,
        total_score=0
    )

    await callback.bot.send_audio(callback.message.chat.id, variant.audio_id)
    await callback.message.answer(TEXT_PART_1)
    await start_part_1(callback, state)
    await callback.answer()


async def start_part_1(callback: CallbackQuery, state: FSMContext):
    variant_id = int((await state.get_data())["variant_id"])
    if first_tasks := await service.get_first_tasks_by_variant(variant_id=variant_id):
        await state.update_data(
            first_tasks=first_tasks,
            index=0,
            score=0
        )

        await callback.message.answer(text=TEXT_TASK_1)
        await handle_first_tasks(callback, state)

    else:
        await callback.message.answer(TEXT_NO_TASKS)
        await callback.answer()
        await callback.message.answer(TEXT_PART_2)
        await start_part_2(callback, state)


async def handle_first_tasks(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tasks = data["first_tasks"]
    index = data["index"]
    score = data["score"]
    total_score = data["total_score"]

    if index < len(tasks):
        current_task = tasks[index]

        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=TEXT_TRUE,
                callback_data=f"hsk4_true_{index + 1}"
            ),
            InlineKeyboardButton(
                text=TEXT_FALSE,
                callback_data=f"hsk4_false_{index + 1}"
            )
        )
        await callback.message.answer(
            text=f"Вопрос {index + 1}/{len(tasks)}\n{current_task.text}",
            reply_markup=builder.as_markup()
        )
    else:
        total_score += score

        await callback.message.answer(TEXT_TASK_COMPLETED.format(score=total_score, total=10))

        await state.update_data(
            total_score=total_score
        )

        await callback.message.answer(text=TEXT_PART_2)
        await start_part_2(callback, state)


@router.callback_query(F.data.startswith(("hsk4_true_", "hsk4_false_")))
async def handle_first_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tasks = data["first_tasks"]
    index = data["index"]
    score = data["score"]

    bool_dict = {
        "true": True,
        "false": False
    }

    curr_task = tasks[index]
    answer = callback.data.split("_")[1]

    if bool_dict[answer] == curr_task.is_correct:
        score = score + 1
        await callback.message.edit_text(
            f"{callback.message.text}\n{ANSWER_RIGHT}"
        )
    else:
        await callback.message.edit_text(f"{callback.message.text}\n{ANSWER_FALSE}")

    new_index = index + 1

    await state.update_data(
        index=new_index,
        score=score
    )

    await handle_first_tasks(callback, state)


async def start_part_2(callback: CallbackQuery, state: FSMContext):
    variant_id = int((await state.get_data())["variant_id"])
    if second_tasks := await service.get_second_tasks_by_variant(variant_id=variant_id):
        await state.update_data(
            second_tasks=second_tasks,
            index=0,
            score=0
        )

        await callback.message.answer(text=TEXT_TASK_2)
        await handle_second_tasks(callback, state)

    else:
        await callback.message.answer(TEXT_NO_TASKS)
        await callback.answer()
        await callback.message.answer(TEXT_PART_3)
        await start_part_3(callback, state)


async def handle_second_tasks(callback: CallbackQuery = None, state: FSMContext = None,
                              bot: Bot = None, chat_id: int = None):
    data = await state.get_data()
    tasks = data["second_tasks"]
    index = data["index"]
    score = data["score"]
    total_score = data["total_score"]

    if not bot:
        bot = callback.bot
        chat_id = callback.message.chat.id

    if index < len(tasks):
        task = tasks[index]
        options = [f"{option.letter}. {option.text}" for option in task.options]
        correct_answer_id = ord(task.correct_letter) - ord("A")
        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            question=f"Вопрос {index + 1}/{len(tasks)}",
            correct_option_id=correct_answer_id,
            is_anonymous=False,
            type="quiz"
        )
        await state.update_data(
            correct_answer_id=correct_answer_id,
            chat_id=chat_id
        )
        await state.set_state(ListeningSecondStates.poll_answer)
    else:
        total_score += score

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=15))

        await state.update_data(
            total_score=total_score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
        await start_part_3(callback, state, bot, chat_id)


@router.poll_answer(ListeningSecondStates.poll_answer)
async def handle_second_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    correct_answer_id = data["correct_answer_id"]
    score = data["score"]
    index = data["index"]
    chat_id = data["chat_id"]

    if poll_answer.option_ids:
        is_correct = correct_answer_id == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_second_tasks(bot=poll_answer.bot, state=state, chat_id=chat_id)


async def start_part_3(callback: CallbackQuery = None, state: FSMContext = None,
                       bot: Bot = None, chat_id: int = None):
    if not bot:
        bot = callback.bot
        chat_id = callback.message.chat.id

    variant_id = int((await state.get_data())["variant_id"])
    if third_tasks := await service.get_third_tasks_by_variant(variant_id=variant_id):
        await state.update_data(
            third_tasks=third_tasks,
            index=0,
            score=0
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_3)
        await handle_third_tasks(bot, chat_id, state)

    else:
        await bot.send_message(chat_id=chat_id, text=TEXT_NO_TASKS)
        #await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
        await finish_listening(bot, chat_id, state)


async def handle_third_tasks(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    tasks = data["third_tasks"]
    index = data["index"]
    score = data["score"]
    total_score = data["total_score"]

    if index < len(tasks):
        task = tasks[index]
        options = [f"{option.letter}. {option.text}" for option in task.options]
        correct_answer_id = ord(task.correct_letter) - ord("A")
        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            question=f"Вопрос {index + 1}/{len(tasks)}",
            correct_option_id=correct_answer_id,
            is_anonymous=False,
            type="quiz"
        )
        await state.update_data(
            correct_answer_id=correct_answer_id,
            chat_id=chat_id
        )
        await state.set_state(ListeningThirdStates.poll_answer)
    else:
        total_score += score

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=20))

        await state.update_data(
            total_score=total_score
        )

        await finish_listening(bot, chat_id, state)


@router.poll_answer(ListeningThirdStates.poll_answer)
async def handle_third_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    correct_answer_id = data["correct_answer_id"]
    score = data["score"]
    index = data["index"]
    chat_id = data["chat_id"]

    if poll_answer.option_ids:
        is_correct = correct_answer_id == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_third_tasks(bot=poll_answer.bot, state=state, chat_id=chat_id)


async def finish_listening(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    total_score = data["total_score"]

    if data.get("is_full_test", False):
        # Сохраняем результат аудирования и переходим к чтению
        await state.update_data(
            listening_score=total_score,
            total_score=0
        )
        # Импортируем функцию из full_test
        from hsk4.full_test import move_to_reading_part
        await move_to_reading_part(bot, chat_id, state)
        return
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}/45</b>"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.listening)
