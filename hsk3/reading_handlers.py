from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from hsk3.states import QuizStates
from aiogram.types import PollAnswer, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from hsk3.intro import get_back_to_types, Sections
from .services import reading_service

router = Router()


@router.callback_query(F.data == "hsk3_reading")
async def get_reading(callback: CallbackQuery):
    text = "Выберите тип задания:"
    type_one = InlineKeyboardButton(text="Тип 1", callback_data="hsk_3_reading_type_one_tasks")
    type_two = InlineKeyboardButton(text="Тип 2", callback_data="hsk_3_reading_type_two_tasks")
    type_three = InlineKeyboardButton(text="Тип 3", callback_data="hsk_3_reading_type_three_tasks")

    builder = InlineKeyboardBuilder()
    builder.add(type_one, type_two, type_three)
    builder.adjust(1)

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "hsk_3_reading_type_one_tasks")
async def get_reading_type_one_tasks(callback: CallbackQuery):
    tasks = reading_service.get_type_one_tasks()
    builder = InlineKeyboardBuilder()
    text = "Есть следующие варианты этого типа задания:"
    for task in tasks:
        builder.button(text=f"Вариант {task.id}\n",
                       callback_data=f"hsk3/reading/one/{task.id}")

    builder.adjust(1)
    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("hsk3/reading/one/"))
async def start_quiz_hsk3(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("/")[-1])
    task = reading_service.get_type_one_task(task_id=task_id)

    task_text = task.description + "\n\n"
    for option in task.sentence_options:
        task_text += f"{option.letter} {option.text}\n"
    await callback.message.answer(task_text)

    await state.update_data(
        questions=task.questions,
        options=[option.letter for option in task.sentence_options],
        current_question_index=0,
        score=0
    )

    # Отправляем первый вопрос
    await send_next_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_question(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    question_index = data['current_question_index']
    questions = data['questions']
    options = data['options']
    score = data['score']

    if question_index < len(questions):
        question = questions[question_index]
        await bot.send_poll(
            chat_id=chat_id,
            question=f"{question_index + 1}. {question.text}",
            options=options,
            type="quiz",
            correct_option_id=ord(question.correct_letter) - ord('A'),
            is_anonymous=False
        )
        await state.set_state(QuizStates.WAITING_FOR_ANSWER)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"Тест завершен! 🎉\nРезультат: {score}/{len(questions)}"
        )
        await state.clear()


@router.poll_answer(QuizStates.WAITING_FOR_ANSWER)
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext, bot: Bot):
    data = await state.get_data()

    # Обработка заданий типа 1 и 2
    if 'questions' in data:
        current_question = data['questions'][data['current_question_index']]
        await state.update_data(
            current_question_index=data['current_question_index'] + 1,
            score=data["score"] + (poll_answer.option_ids[0] == ord(current_question.correct_letter) - ord("A"))
        )
        await send_next_question(bot, poll_answer.user.id, state)

    # Обработка заданий типа 3
    elif 'tasks' in data:
        current_index = data['current_task_index']
        current_task = data['tasks'][current_index]

        is_correct = poll_answer.option_ids[0] == ord(current_task.correct_answer_letter) - ord("A")
        await state.update_data(
            current_task_index=current_index + 1,
            score=data['score'] + int(is_correct)
        )
        await send_next_type_three_task(bot, poll_answer.user.id, state)


@router.callback_query(F.data == "hsk_3_reading_type_two_tasks")
async def get_reading_type_two_tasks(callback: CallbackQuery):
    tasks = reading_service.get_type_two_tasks()
    builder = InlineKeyboardBuilder()
    text = "Есть следующие варианты этого типа задания:"
    for task in tasks:
        builder.button(text=f"Вариант {task.id}\n",
                       callback_data=f"hsk3/reading/two/{task.id}")

    builder.adjust(1)
    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith("hsk3/reading/two/"))
async def start_quiz_hsk3(callback: CallbackQuery, state: FSMContext):
    task_id = int(callback.data.split("/")[-1])
    task = reading_service.get_type_two_task(task_id=task_id)

    task_text = task.description + "\n\n"
    for option in task.sentence_options:
        task_text += f"{option.letter} {option.text}\n"
    await callback.message.answer(task_text)

    await state.update_data(
        questions=task.questions,
        options=[option.letter for option in task.sentence_options],
        current_question_index=0,
        score=0
    )

    # Отправляем первый вопрос
    await send_next_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data == "hsk_3_reading_type_three_tasks")
async def start_type_three_quiz(callback: CallbackQuery, state: FSMContext):
    tasks = reading_service.get_random_type_three_tasks()

    await state.update_data(
        tasks=tasks,
        current_task_index=0,
        score=0
    )

    # Отправляем первое задание
    await send_next_type_three_task(callback.bot, callback.from_user.id, state)
    await callback.answer()


async def send_next_type_three_task(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    task_index = data['current_task_index']
    tasks = data['tasks']

    if task_index >= len(tasks):
        # Все задания завершены
        await bot.send_message(
            chat_id=chat_id,
            text=f"Тест завершен! 🎉\nРезультат: {data['score']}/{len(tasks)}"
        )
        await state.clear()
        await get_back_to_types(bot, chat_id, section=Sections.reading)
        return

    task = tasks[task_index]

    # Формируем текст задания
    task_text = (
        f"Задание {task_index + 1}/{len(tasks)}\n\n"
        f"{task.description}\n\n"
        f"{task.text}\n"
        f"★ {task.question}"
    )

    # Отправляем текст задания
    await bot.send_message(chat_id, task_text)

    # Подготавливаем варианты для викторины
    options = [f"{opt.letter}. {opt.text}" for opt in task.options]
    correct_index = ord(task.correct_answer_letter) - ord("A")

    # Отправляем викторину
    await bot.send_poll(
        chat_id=chat_id,
        question="Выберите правильный ответ:",
        options=options,
        type="quiz",
        correct_option_id=correct_index,
        is_anonymous=False,
    )

    await state.set_state(QuizStates.WAITING_FOR_ANSWER)


@router.poll_answer(QuizStates.WAITING_FOR_ANSWER)
async def handle_type_three_poll_answer(poll_answer: PollAnswer, state: FSMContext, bot: Bot):
    data = await state.get_data()
    tasks = data['tasks']
    current_index = data['current_task_index']
    current_task = tasks[current_index]

    # Проверяем правильность ответа
    is_correct = poll_answer.option_ids[0] == ord(current_task.correct_answer_letter) - ord("A")

    # Обновляем состояние
    await state.update_data(
        current_task_index=current_index + 1,
        score=data['score'] + int(is_correct)
    )

    # Отправляем следующее задание
    await send_next_type_three_task(bot, poll_answer.user.id, state)



