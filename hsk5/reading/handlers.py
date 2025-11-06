from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk5.intro import Sections, get_back_to_types
from .service import service
from .states import *


router = Router()

### Callback значения
CALLBACK_READING_VARIANT = "hsk5_reading_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_PART_3 = "Задание 3"


TEXT_TASK_1 = "Даны несколько коротких текстов: объявления, заметки, сообщения. После каждого текста есть вопрос с вариантами ответов. Вам нужно выбрать один правильный вариант ответа."
TEXT_TASK_2 = "Дан текст, в котором пропущено 5 предложений. Ниже даны эти предложения вперемешку, плюс 1-2 лишних. Для каждого пропуска нужно выбрать наиболее подходящее предложение из списка"
TEXT_TASK_3 = "Вам даны 2-3 длинных текста. Ответьте на вопросы, выбрав для каждого правильный вариант ответа"


TEXT_TRUE = "Правда"
TEXT_FALSE = "Ложь"
ANSWER_RIGHT = "✅ Верно!"
ANSWER_FALSE = "❌ Неверно!"

TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"
TEXT_NO_TASKS = "Задания не найдены."
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_TASKS_COMPLETED = "Общий результат: <b>{score}/{total}</b>"

TEXT_NO_VARIANTS = "Нет вариантов"


@router.callback_query(F.data == Sections.reading)
async def show_reading_variants(callback: CallbackQuery):
    if variants := service.get_reading_variants():
        builder = InlineKeyboardBuilder()
        for num, variant in enumerate(variants, start=1):
            builder.add(
                InlineKeyboardButton(
                    text=f"Вариант {num}",
                    callback_data=f"{CALLBACK_READING_VARIANT}_{variant.id}"
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
    else:
        await callback.message.answer(TEXT_NO_VARIANTS)
        await get_back_to_types(callback.bot, callback.message.chat.id, Sections.listening)

    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data.startswith(CALLBACK_READING_VARIANT))
async def start_reading(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])
    await state.update_data(
        variant_id=var_id,
        chat_id=callback.message.chat.id
    )
    await start_reading_variant(callback=callback, state=state)


async def start_reading_variant(state: FSMContext, callback: CallbackQuery = None, bot: Bot = None):
    if bot is None:
        bot = callback.bot
    
    data = await state.get_data()

    if data.get("reading_variant_id", False):
        var_id = data["reading_variant_id"]
    else:
        var_id = data["variant_id"]

    chat_id = data["chat_id"]

    if callback:
        await callback.message.delete()
        await callback.answer()

        # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=var_id,
        total_score=0,
    )

    # Запускаем первую часть
    await bot.send_message(chat_id, TEXT_PART_1)
    await start_part_1(bot, state)

async def start_part_1(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := service.get_first_tasks_by_variant(var_id=variant_id):
        await bot.send_message(chat_id, TEXT_TASK_1)

        await state.update_data(
            tasks=tasks,
            task_index=0,
            score=0
        )

        await handle_first_task_batch(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим ко второму заданию")
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)
        await start_part_2(bot, state)


async def handle_first_task_batch(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    task_index = data["task_index"]
    tasks = data["tasks"]
    score = data["score"]

    if task_index < len(tasks):
        current_task = tasks[task_index]
        await bot.send_message(chat_id, current_task.text)

        await state.update_data(
            questions=current_task.questions,
            index=0
        )

        await handle_first_task(bot, state)
    else:
        
        total_questions = sum(len(task.questions) for task in tasks)
        await state.update_data(
            total_score=data["total_score"] + score,
        )
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=total_questions))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)
        await start_part_2(bot, state)


async def handle_first_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    index = data["index"]
    score = data["score"]
    questions = data["questions"]
    task_index = data["task_index"]
    tasks = data["tasks"]
    task_index = data["task_index"]


    if index < len(questions):
        curr_question = questions[index]

        options = [f"{op.letter}. {op.text}" for op in curr_question.options]


        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            correct_option_id=ord(curr_question.correct_letter) - ord("A"),
            is_anonymous=False,
            question=f"{index + 1}/{len(questions)}. {curr_question.text}",
            type="quiz"
        )

        await state.set_state(HSK5ReadingFirstTask.answer)
    else:
        await state.update_data(
            task_index=task_index + 1
        )
        await handle_first_task_batch(bot, state)


@router.poll_answer(HSK5ReadingFirstTask.answer)
async def handle_first_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    questions = data["questions"]
    index = data["index"]
    curr_question = questions[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_question.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_first_task(bot=poll_answer.bot, state=state)

async def start_part_2(bot: Bot, state: State):
    data = await state.get_data()
    chat_id = data["chat_id"]
    variant_id = data["variant_id"]

    if tasks := service.get_second_tasks_by_variant(var_id=variant_id):
        await state.update_data(
            tasks=tasks,
            index=0,
            score=0
        )

        await bot.send_message(chat_id, TEXT_TASK_2)

        await handle_second_task(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим к третьему заданию")
        await start_part_3(bot, state)

async def handle_second_task(bot: Bot, state: State):
    data = await state.get_data()
    chat_id = data["chat_id"]
    variant_id = data["variant_id"]
    tasks = data["tasks"] 
    index = data["index"]
    score = data["score"]

    if index < len(tasks):
        curr_task = tasks[index]

        options = [f"{op.letter}. {op.text}" for op in curr_task.options]


        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            correct_option_id=ord(curr_task.correct_letter) - ord("A"),
            is_anonymous=False,
            question=f"{index + 1}/{len(tasks)}. {curr_task.text}",
            type="quiz"
        )

        await state.set_state(HSK5ReadingSecondTask.answer)
    else:
        await state.update_data(
            total_score=data["total_score"] + score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=10))
        await bot.send_message(chat_id, TEXT_PART_3)
        await start_part_3(bot, state)


@router.poll_answer(HSK5ReadingSecondTask.answer)
async def handle_second_answer(poll_answer: PollAnswer, state: FSMContext):
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

    await handle_second_task(bot=poll_answer.bot, state=state)


async def start_part_3(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    variant_id = data["variant_id"]

    if tasks := service.get_third_tasks_by_variant(var_id=variant_id):
        await state.update_data(
            tasks=tasks,
            task_index=0,
            score=0
        )

        await bot.send_message(chat_id, TEXT_TASK_3)

        await handle_third_task_batch(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим к концу варианта")
        await finish_reading(bot, state)
    
async def handle_third_task_batch(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    task_index = data["task_index"]
    tasks = data["tasks"]
    score = data["score"]

    if task_index < len(tasks):
        current_task = tasks[task_index]
        if current_task.photo_id:
            await bot.send_photo(chat_id, current_task.photo_id, caption=current_task.text)
        else:
            await bot.send_message(chat_id, current_task.text)

        await state.update_data(
            questions=current_task.questions,
            index=0
        )

        await handle_third_task(bot, state)
    else:
        
        total_questions = sum(len(task.questions) for task in tasks)
        await state.update_data(
            total_score=data["total_score"] + score,
        )
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=total_questions))
        await finish_reading(bot, state)


async def handle_third_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    index = data["index"]
    questions = data["questions"]
    task_index = data["task_index"]

    if index < len(questions):
        curr_question = questions[index]

        options = sorted([f"{op.letter}. {op.text}" for op in curr_question.options])

        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            correct_option_id=ord(curr_question.correct_letter) - ord("A"),
            is_anonymous=False,
            question=f"{index + 1}/{len(questions)}. {curr_question.text}",
            type="quiz"
        )

        await state.set_state(HSK5ReadingThirdTask.answer)
    else:
        await state.update_data(
            task_index=task_index + 1
        )
        await handle_third_task_batch(bot, state)


@router.poll_answer(HSK5ReadingThirdTask.answer)
async def handle_third_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    questions = data["questions"]
    index = data["index"]
    curr_question = questions[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_question.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_third_task(bot=poll_answer.bot, state=state)

async def finish_reading(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    total_score = data["total_score"]

    await state.update_data(
        reading_score=total_score,
    )

    if data.get("is_full_test", False):
        await state.update_data(
            reading_score=total_score
        )
        await bot.send_message(
            chat_id=chat_id,
            text=f"Чтение завершено!\nПереходим к письму."
        )

        from hsk5.writing.handlers import start_writing_variant
        await start_writing_variant(bot=bot, state=state)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}/45</b>"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.reading)
    