import random

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.intro import Sections
from hsk3.services import listening_service
from hsk3.states import ListeningStates

router = Router()

# Тексты кнопок
TEXT_TYPE_ONE = "Тип 1"
TEXT_TYPE_TWO = "Тип 2"
TEXT_TYPE_THREE = "Тип 3"
TEXT_CHOOSE_TASK_TYPE = "Выберите тип задания"

# Callback значения
CALLBACK_HSK3_LISTENING = "hsk3_listening"
CALLBACK_TYPE_ONE_TASKS = "hsk_3_listening_type_one_tasks"
CALLBACK_TYPE_TWO_TASKS = "hsk_3_listening_type_two_tasks"
CALLBACK_TYPE_THREE_TASKS = "hsk_3_listening_type_three_tasks"

# Тексты заданий
FIRST_TASK_TEXT = "<b>Сопоставьте картинки с репликами:</b>"
PICTURES_CHOICE = "<b>Варианты картинок</b>"
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"

# Добавляем в начало файла
SECOND_TASK_TEXT = "<b>Прослушайте и определите, верны ли утверждения:</b>"
TEXT_TRUE = "Правда"
TEXT_FALSE = "Ложь"


@router.callback_query(F.data == Sections.listening)
async def show_task_types(callback: CallbackQuery):
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


@router.callback_query(F.data == CALLBACK_TYPE_ONE_TASKS)
async def get_first_task(callback: CallbackQuery, state: FSMContext):
    task = listening_service.get_test_first_task()

    await callback.message.answer(text=FIRST_TASK_TEXT)
    await callback.bot.send_photo(
        chat_id=callback.message.chat.id,
        photo=task.picture_id,
        caption=PICTURES_CHOICE
    )

    await state.update_data(
        current_index=0,  # Унифицированный ключ как в reading
        questions=task.questions,
        score=0,
        options=[q.correct_letter for q in task.questions]  # Сохраняем варианты ответов
    )

    await send_next_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_question(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос или завершает тест."""
    data = await state.get_data()

    current_index = data["current_index"]
    questions = data["questions"]
    options = data["options"]

    if current_index < len(questions):
        # Сортируем варианты ответов для единообразия
        sorted_options = sorted(options)

        next_question = questions[current_index]
        correct_answer = next_question.correct_letter

        # Находим правильный индекс в отсортированном списке
        correct_option_id = sorted_options.index(correct_answer)

        await bot.send_poll(
            chat_id=chat_id,
            question=f"Вопрос {current_index + 1}",
            options=sorted_options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False
        )

        # Устанавливаем состояние ожидания ответа
        await state.set_state(ListeningStates.answer)
    else:
        # Завершаем тест
        score = data["score"]
        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_TASK_COMPLETED.format(score=score, total=len(questions))
        )
        await state.clear()


async def handle_listening_answer(poll_answer: PollAnswer, state: FSMContext):
    """Обрабатывает ответ пользователя на вопрос аудирования."""
    data = await state.get_data()

    current_index = data["current_index"]
    questions = data["questions"]
    options = data["options"]

    # Получаем текущий вопрос
    current_question = questions[current_index]

    # Сортируем варианты так же, как при отправке
    sorted_options = sorted(options)
    correct_option_id = sorted_options.index(current_question.correct_letter)

    # Проверяем правильность ответа
    is_correct = poll_answer.option_ids[0] == correct_option_id

    # Обновляем данные состояния
    await state.update_data(
        current_index=current_index + 1,
        score=data["score"] + int(is_correct)
    )

    # Отправляем следующий вопрос
    await send_next_question(poll_answer.bot, poll_answer.user.id, state)


# Обработчик ответов на опросы - ключевая часть!
@router.poll_answer(ListeningStates.answer)
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    """Обработчик ответов на викторину аудирования."""
    await handle_listening_answer(poll_answer, state)


@router.callback_query(F.data == CALLBACK_TYPE_TWO_TASKS)
async def start_second_task(callback: CallbackQuery, state: FSMContext):
    tasks = listening_service.get_test_second_tasks()

    await callback.message.answer(text=SECOND_TASK_TEXT)

    await state.update_data(
        current_index=0,
        questions=[{"text": task.text, "is_correct": task.is_correct} for task in tasks],
        score=0,
        total=len(tasks)
    )

    await send_next_truefalse_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_truefalse_question(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    current_index = data["current_index"]
    questions = data["questions"]

    if current_index < len(questions):
        current_question = questions[current_index]

        # Создаем клавиатуру с вариантами Правда/Ложь
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=TEXT_TRUE,
                callback_data=f"true_{current_index}"
            ),
            InlineKeyboardButton(
                text=TEXT_FALSE,
                callback_data=f"false_{current_index}"
            )
        )

        await bot.send_message(
            chat_id=chat_id,
            text=f"Вопрос {current_index + 1}/{len(questions)}\n\n{current_question['text']}",
            reply_markup=builder.as_markup()
        )
    else:
        score = data["score"]
        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_TASK_COMPLETED.format(score=score, total=len(questions))
        )
        await state.clear()


@router.callback_query(F.data.startswith(("true_", "false_")))
async def handle_truefalse_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data["current_index"]
    questions = data["questions"]

    # Парсим ответ
    user_answer, question_idx = callback.data.split("_")
    question_idx = int(question_idx)

    # Проверяем что отвечают на текущий вопрос
    if question_idx != current_index:
        await callback.answer("Пожалуйста, отвечайте по порядку!", show_alert=True)
        return

    current_question = questions[current_index]
    is_correct = (user_answer == "true") == current_question["is_correct"]

    # Обновляем счет
    new_score = data["score"] + int(is_correct)
    new_index = current_index + 1

    await state.update_data(
        current_index=new_index,
        score=new_score
    )

    # Отправляем feedback
    feedback = "✅ Верно!" if is_correct else "❌ Неверно!"
    correct_answer = TEXT_TRUE if current_question["is_correct"] else TEXT_FALSE
    await callback.message.edit_text(
        f"{callback.message.text}\n\n{feedback}\nПравильный ответ: {correct_answer}"
    )

    # Отправляем следующий вопрос
    await send_next_truefalse_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()