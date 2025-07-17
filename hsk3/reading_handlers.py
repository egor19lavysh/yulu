from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import PollAnswer, CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from hsk3.states import QuizStates
from hsk3.intro import get_back_to_types, Sections
from hsk3.services import reading_service

router = Router()

# Константы для callback данных
CALLBACK_HSK3_READING = "hsk3_reading"
CALLBACK_TYPE_ONE_TASKS = "hsk_3_reading_type_one_tasks"
CALLBACK_TYPE_TWO_TASKS = "hsk_3_reading_type_two_tasks"
CALLBACK_TYPE_THREE_TASKS = "hsk_3_reading_type_three_tasks"
CALLBACK_TASK_PREFIX = "hsk3/reading"

# Текстовые константы
TEXT_CHOOSE_TASK_TYPE = "Выберите тип задания:"
TEXT_TASK_VARIANTS = "Есть следующие варианты этого типа задания:"
TEXT_TEST_COMPLETED = "Тест завершен! 🎉\nРезультат: {score}/{total}"
TEXT_TASK_OPTION = "Вариант {task_id}"
TEXT_TYPE_ONE = "Тип 1"
TEXT_TYPE_TWO = "Тип 2"
TEXT_TYPE_THREE = "Тип 3"


async def show_reading_task_types(callback: CallbackQuery):
    """Показывает типы заданий для части чтения."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=TEXT_TYPE_ONE, callback_data=CALLBACK_TYPE_ONE_TASKS),
        InlineKeyboardButton(text=TEXT_TYPE_TWO, callback_data=CALLBACK_TYPE_TWO_TASKS),
        InlineKeyboardButton(text=TEXT_TYPE_THREE, callback_data=CALLBACK_TYPE_THREE_TASKS)
    )
    builder.adjust(1)

    await callback.message.answer(TEXT_CHOOSE_TASK_TYPE, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


async def show_task_variants(callback: CallbackQuery, task_getter: callable, task_type: str):
    """Показывает варианты заданий для выбранного типа."""
    tasks = task_getter()
    builder = InlineKeyboardBuilder()

    for task in tasks:
        builder.button(
            text=TEXT_TASK_OPTION.format(task_id=task.id),
            callback_data=f"{CALLBACK_TASK_PREFIX}/{task_type}/{task.id}"
        )

    builder.adjust(1)
    await callback.message.answer(TEXT_TASK_VARIANTS, reply_markup=builder.as_markup())
    await callback.answer()


async def start_quiz_session(
        callback: CallbackQuery,
        state: FSMContext,
        task_getter: callable,
        task_type: str,
        session_data: dict
):
    """Начинает сессию вопросов для выбранного задания."""
    task_id = int(callback.data.split("/")[-1])
    task = task_getter(task_id=task_id)

    # Формируем текст задания
    task_text = task.description + "\n\n"
    for option in task.sentence_options:
        task_text += f"{option.letter} {option.text}\n"

    await callback.message.answer(task_text)

    # Сохраняем данные в состоянии
    await state.update_data(
        **session_data,
        options=[option.letter for option in task.sentence_options],
        current_index=0,  # Унифицированный ключ для индекса
        score=0
    )

    # Отправляем первый вопрос
    await send_next_question_or_task(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_question_or_task(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос или задание в зависимости от типа."""
    data = await state.get_data()

    if 'questions' in data:
        # Обработка типов 1 и 2
        questions = data['questions']
        current_index = data['current_index']

        if current_index < len(questions):
            question = questions[current_index]
            await bot.send_poll(
                chat_id=chat_id,
                question=f"{current_index + 1}. {question.text}",
                options=data['options'],
                type="quiz",
                correct_option_id=ord(question.correct_letter) - ord('A'),
                is_anonymous=False
            )
            await state.set_state(QuizStates.WAITING_FOR_ANSWER)
        else:
            await finish_quiz_session(bot, chat_id, state, data['score'], len(questions))
    elif 'tasks' in data:
        # Обработка типа 3
        await send_next_type_three_task(bot, chat_id, state)


async def send_next_type_three_task(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующее задание типа 3."""
    data = await state.get_data()
    current_index = data['current_index']
    tasks = data['tasks']

    if current_index >= len(tasks):
        await finish_quiz_session(bot, chat_id, state, data['score'], len(tasks))
        await get_back_to_types(bot, chat_id, section=Sections.reading)
        return

    task = tasks[current_index]

    # Формируем текст задания
    task_text = (
        f"Задание {current_index + 1}/{len(tasks)}\n\n"
        f"{task.description}\n\n"
        f"{task.text}\n"
        f"★ {task.question}"
    )

    await bot.send_message(chat_id, task_text)

    # Подготавливаем варианты для викторины
    options = [f"{opt.letter}. {opt.text}" for opt in task.options]
    correct_index = ord(task.correct_answer_letter) - ord("A")

    await bot.send_poll(
        chat_id=chat_id,
        question="Выберите правильный ответ:",
        options=options,
        type="quiz",
        correct_option_id=correct_index,
        is_anonymous=False,
    )
    await state.set_state(QuizStates.WAITING_FOR_ANSWER)


async def finish_quiz_session(bot: Bot, chat_id: int, state: FSMContext, score: int, total: int):
    """Завершает сессию вопросов и показывает результаты."""
    await bot.send_message(chat_id, TEXT_TEST_COMPLETED.format(score=score, total=total))
    await state.clear()


async def handle_quiz_answer(poll_answer: PollAnswer, state: FSMContext, bot: Bot):
    """Обрабатывает ответ пользователя на вопрос."""
    data = await state.get_data()
    current_index = data['current_index']
    is_correct = False

    if 'questions' in data:
        # Обработка типов 1 и 2
        current_question = data['questions'][current_index]
        is_correct = poll_answer.option_ids[0] == ord(current_question.correct_letter) - ord("A")
    elif 'tasks' in data:
        # Обработка типа 3
        current_task = data['tasks'][current_index]
        is_correct = poll_answer.option_ids[0] == ord(current_task.correct_answer_letter) - ord("A")

    await state.update_data(
        current_index=current_index + 1,
        score=data['score'] + int(is_correct)
    )

    await send_next_question_or_task(bot, poll_answer.user.id, state)


# Обработчики callback
@router.callback_query(F.data == CALLBACK_HSK3_READING)
async def handle_reading_callback(callback: CallbackQuery):
    await show_reading_task_types(callback)


@router.callback_query(F.data == CALLBACK_TYPE_ONE_TASKS)
async def handle_type_one_tasks(callback: CallbackQuery):
    await show_task_variants(
        callback,
        reading_service.get_type_one_tasks,
        "one"
    )


@router.callback_query(F.data.startswith(f"{CALLBACK_TASK_PREFIX}/one/"))
async def handle_type_one_quiz(callback: CallbackQuery, state: FSMContext):
    await start_quiz_session(
        callback,
        state,
        reading_service.get_type_one_task,
        "one",
        {"questions": reading_service.get_type_one_task(task_id=int(callback.data.split("/")[-1])).questions}
    )


@router.callback_query(F.data == CALLBACK_TYPE_TWO_TASKS)
async def handle_type_two_tasks(callback: CallbackQuery):
    await show_task_variants(
        callback,
        reading_service.get_type_two_tasks,
        "two"
    )


@router.callback_query(F.data.startswith(f"{CALLBACK_TASK_PREFIX}/two/"))
async def handle_type_two_quiz(callback: CallbackQuery, state: FSMContext):
    await start_quiz_session(
        callback,
        state,
        reading_service.get_type_two_task,
        "two",
        {"questions": reading_service.get_type_two_task(task_id=int(callback.data.split("/")[-1])).questions}
    )


@router.callback_query(F.data == CALLBACK_TYPE_THREE_TASKS)
async def handle_type_three_tasks(callback: CallbackQuery, state: FSMContext):
    tasks = reading_service.get_random_type_three_tasks()
    await state.update_data(
        tasks=tasks,
        current_index=0,  # Унифицированный ключ
        score=0
    )
    await send_next_type_three_task(callback.bot, callback.from_user.id, state)
    await callback.answer()


# Обработчик ответов на опросы
@router.poll_answer(QuizStates.WAITING_FOR_ANSWER)
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext, bot: Bot):
    await handle_quiz_answer(poll_answer, state, bot)