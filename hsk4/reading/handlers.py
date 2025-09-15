from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk4.intro import Sections, get_back_to_types
from .service import service
from .states import *

router = Router()

### Callback значения
CALLBACK_READING_VARIANT = "hsk4_reading_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_PART_3 = "Задание 3"

TEXT_TASK_1 = "Прочтите 1-2 предложения с пропусками слов/фраз и выберите один из вариантов ответов:"
TEXT_TASK_2 = 'Прочтите 3 предложения и запишите их в правильном порядке\n\n* запишите ответ одним сообщением из 3 заглавных букв через пробел\nПример: "A B C"'
TEXT_TASK_3 = "Прочтите краткий отрывок и ответьте на 1-2 вопроса по нему:"

TEXT_NO_TASKS = "Задания не найдены."
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_TASKS_COMPLETED = "Общий результат: <b>{score}/{total}</b>"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"


@router.callback_query(F.data == Sections.reading)
async def show_reading_variants(callback: CallbackQuery):
    variants = service.get_reading_variants()
    builder = InlineKeyboardBuilder()
    for num, variant in enumerate(variants, start=1):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num}",
                callback_data=f"{CALLBACK_READING_VARIANT}_{variant.id}"
            )
        )
    builder.adjust(1)
    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_READING_VARIANT))
async def start_reading_variant(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])

    # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=var_id,
        total_score=0,
        chat_id=callback.message.chat.id
    )

    # Запускаем первую часть
    await callback.message.answer(TEXT_PART_1)
    await start_part_1(callback, state)
    await callback.answer()


async def start_part_1(callback: CallbackQuery, state: FSMContext):
    variant_id = (await state.get_data())["variant_id"]
    if first_tasks := service.get_first_tasks_by_variant(var_id=variant_id):
        await state.update_data(
            first_tasks=first_tasks,
            index=0,
            score=0
        )

        await callback.message.answer(text=TEXT_TASK_1)
        await handle_first_tasks(bot=callback.bot, state=state)

    else:
        await callback.message.answer(TEXT_NO_TASKS)
        await callback.answer()
        await callback.message.answer(TEXT_PART_2)
        await start_part_2(bot=callback.bot, state=state)


async def handle_first_tasks(bot: Bot, state: FSMContext,):
    data = (await state.get_data())
    tasks = data["first_tasks"]
    index = data["index"]
    score = data["score"]
    chat_id = data["chat_id"]
    total_score = data["total_score"]


    if index < len(tasks):
        curr_task = tasks[index]
        option_text = "Варианты ответов:\n"
        options = []
        for option in curr_task.options:
            option_text += f"<b>{option.letter}</b>. {option.text}\n"
            options.append(f"{option.letter}. {option.text}")

        await state.update_data(sentence_index=0,
                                options=options,
                                sentences=curr_task.sentences)

        await bot.send_message(chat_id=chat_id, text=option_text)
        await handle_first_task(bot=bot, state=state)
    else:
        total_score += score

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=10))

        await state.update_data(
            total_score=total_score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)
        await start_part_2(bot=bot, state=state)


async def handle_first_task(state: FSMContext, bot: Bot):
    data = await state.get_data()
    sentence_index = data["sentence_index"]
    options = data["options"]
    sentences = data["sentences"]
    chat_id = data["chat_id"]
    index = data["index"]


    if sentence_index < len(sentences):
        curr_sentence = sentences[sentence_index]
        await bot.send_message(chat_id=chat_id, text=f"{sentence_index + 1}. {curr_sentence.text}")
        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            type="quiz",
            is_anonymous=False,
            correct_option_id=(ord(curr_sentence.correct_letter) - ord("A")),
            question="Выберите вариант ответа"
        )

        await state.set_state(ReadingFirstTask.answer)
    else:
        await state.update_data(
            index=index + 1
        )
        await handle_first_tasks(bot=bot, state=state)


@router.poll_answer(ReadingFirstTask.answer)
async def handle_first_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    sentences = data["sentences"]
    index = data["sentence_index"]
    score = data["score"]

    curr_sentence = sentences[index]

    if poll_answer.option_ids:
        is_correct = (ord(curr_sentence.correct_letter) - ord("A")) == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            sentence_index=index + 1
        )

    await handle_first_task(bot=poll_answer.bot, state=state)


async def start_part_2(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if second_tasks := service.get_second_tasks_by_variant(var_id=variant_id):
        await state.update_data(
            second_tasks=second_tasks,
            index=0,
            score=0
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_2)
        await handle_second_tasks(bot=bot, state=state)

    else:
        await bot.send_message(chat_id=chat_id, text=TEXT_NO_TASKS)
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
        await start_part_3(bot=bot, state=state)


async def handle_second_tasks(bot: Bot, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    score = data["score"]
    chat_id = data["chat_id"]
    second_tasks = data["second_tasks"]
    total_score = data["total_score"]

    if index < len(second_tasks):
        curr_task = second_tasks[index]
        task_text = ""
        for option in curr_task.options:
            task_text += f"{option.letter} {option.text}\n"

        await bot.send_message(chat_id=chat_id, text=task_text)
        await state.set_state(ReadingSecondTask.answer)
    else:
        total_score += score
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=10))

        await state.update_data(
            total_score=total_score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
        await start_part_3(bot=bot, state=state)


@router.message(ReadingSecondTask.answer)
async def handle_second_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    tasks = data["second_tasks"]
    score = data["score"]
    answer = tasks[index].correct_sequence

    if msg.text:
        if msg.text.upper() == answer:
            await msg.reply("Правильно!\n<b>+ 1 балл</b>")
            await state.update_data(score=score + 1)
        else:
            await msg.reply(f"Неправильно!\nПравильно будет так: <b>{answer}</b>")
    else:
        await msg.reply("Ответьте текстом!")
        await state.set_state(ReadingSecondTask.answer)
        return

    await state.update_data(index=index + 1)

    await handle_second_tasks(msg.bot, state)


async def start_part_3(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if third_tasks := service.get_third_tasks_by_variant(var_id=variant_id):
        await state.update_data(
            third_tasks=third_tasks,
            index=0,
            score=0
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_3)
        await handle_third_tasks(bot, state)

    else:
        await bot.send_message(chat_id=chat_id, text=TEXT_NO_TASKS)
        await finish_reading(bot, state)


async def handle_third_tasks(bot: Bot, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    index = data["index"]
    chat_id = data["chat_id"]
    total_score = data["total_score"]
    third_tasks = data["third_tasks"]

    if index < len(third_tasks):
        curr_task = third_tasks[index]
        await state.update_data(
            current_third_task=curr_task,
            third_task_index=0
        )
        await bot.send_message(chat_id=chat_id, text=curr_task.text)
        await handle_third_task(bot, state)
    else:
        total_score += score
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=20))

        await state.update_data(
            total_score=total_score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_ALL_PARTS_COMPLETED)
        await finish_reading(bot=bot, state=state)


async def handle_third_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    third_task_index = data["third_task_index"]
    index = data["index"]
    chat_id = data["chat_id"]
    curr_task = data["current_third_task"]
    questions = curr_task.questions

    if third_task_index < len(questions):
        curr_question = questions[third_task_index]
        await bot.send_message(chat_id=chat_id, text=f"{third_task_index + 1}/{len(questions)}\n" + curr_question.text)
        options = [f"{option.letter}. {option.text}" for option in curr_question.options]
        correct_id = ord(curr_question.correct_letter) - ord("A")
        await state.update_data(
            correct_third_task_question_answer=correct_id
        )
        await bot.send_poll(chat_id=chat_id,
                            type='quiz',
                            options=options,
                            is_anonymous=False,
                            question=f"{third_task_index + 1}/{len(questions)}",
                            correct_option_id=correct_id
                            )
        await state.set_state(ReadingThirdTask.answer)
    else:
        await state.update_data(
            index=index + 1
        )
        await handle_third_tasks(bot, state)


@router.poll_answer(ReadingThirdTask.answer)
async def handle_third_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    answer = data["correct_third_task_question_answer"]
    index = data["third_task_index"]

    if poll_answer.option_ids:
        is_correct = answer == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            third_task_index=index + 1
        )

    await handle_third_task(bot=poll_answer.bot, state=state)


async def finish_reading(bot: Bot, state: FSMContext):
    data = await state.get_data()
    total_score = data["total_score"]
    chat_id = data["chat_id"]

    await bot.send_message(
        chat_id=chat_id,
        text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}/45</b>"
    )

    await state.clear()
    await get_back_to_types(bot, chat_id, Sections.listening)
