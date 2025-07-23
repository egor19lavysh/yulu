import random

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.intro import Sections, get_back_to_types
from hsk3.services import listening_service
from hsk3.states import ListeningFirstStates, ListeningThirdStates

router = Router()

# Тексты
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Часть 1"
TEXT_PART_2 = "Часть 2"
TEXT_PART_3 = "Часть 3"
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_CONTINUE_TO_NEXT_PART = "Продолжить к следующей части"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"

# Callback значения
CALLBACK_HSK3_LISTENING = "hsk3_listening"
CALLBACK_LISTENING_VARIANT = "listening_variant"
CALLBACK_LISTENING_PART_1 = "listening_part_1"
CALLBACK_LISTENING_PART_2 = "listening_part_2"
CALLBACK_LISTENING_PART_3 = "listening_part_3"
CALLBACK_CONTINUE_PART = "continue_part"

# Тексты заданий
FIRST_TASK_TEXT = "<b>Сопоставьте картинки с репликами:</b>"
PICTURES_CHOICE = "<b>Варианты картинок</b>"
SECOND_TASK_TEXT = "<b>Прослушайте и определите, верны ли утверждения:</b>"
THIRD_TASK_TEXT = "<b>Прослушайте реплики и ответьте на вопрос, выбрав один из трех ответов:</b>"
TEXT_TRUE = "Правда"
TEXT_FALSE = "Ложь"


@router.callback_query(F.data == Sections.listening)
async def show_listening_variants(callback: CallbackQuery):
    """Показывает доступные варианты listening заданий"""
    variants = listening_service.get_listening_variants()  # Получаем все варианты

    if not variants:
        await callback.message.answer("Извините, варианты заданий временно недоступны.")
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()
    for variant in variants:
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {variant.id}",
                callback_data=f"{CALLBACK_LISTENING_VARIANT}_{variant.id}"
            )
        )
    builder.adjust(2)  # По 2 кнопки в ряд

    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


async def start_part_1(callback: CallbackQuery, state: FSMContext, variant_id: int):
    """Запускает первую часть - FirstTask"""
    first_tasks = listening_service.get_first_tasks_by_variant(variant_id)

    if not first_tasks:
        await callback.message.answer("Задания первой части не найдены.")
        return

    # Берем первую задачу (или можно рандомно)
    task = first_tasks[0]

    await callback.message.answer(text=FIRST_TASK_TEXT)
    await callback.bot.send_photo(
        chat_id=callback.message.chat.id,
        photo=task.picture_id,
        caption=PICTURES_CHOICE
    )

    await state.update_data(
        current_index=0,
        questions=task.questions,
        part_score=0,
        options=[q.correct_letter for q in task.questions]
    )

    await send_next_first_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_LISTENING_VARIANT))
async def start_listening_variant(callback: CallbackQuery, state: FSMContext):
    """Начинает прохождение выбранного варианта"""
    variant_id = int(callback.data.split("_")[-1])
    variant = listening_service.get_listening_variant(variant_id)

    if not variant:
        await callback.message.answer("Вариант не найден.")
        return

    # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=variant_id,
        current_part=1,
        total_score=0,
        part_1_completed=False,
        part_2_completed=False,
        part_3_completed=False
    )

    # Отправляем аудио по file_id (не пересылаем)
    try:
        await callback.bot.send_audio(
            chat_id=callback.message.chat.id,
            audio=variant.audio_id
        )
    except Exception as e:
        await callback.message.answer(f"Ошибка при отправке аудио: {e}")
        return

    # Запускаем первую часть
    await callback.message.answer(TEXT_PART_1)
    await start_part_1(callback, state, variant_id)

async def send_next_first_question(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос первой части"""
    data = await state.get_data()
    current_index = data["current_index"]
    questions = data["questions"]
    options = data["options"]

    if current_index < len(questions):
        sorted_options = sorted(options)
        next_question = questions[current_index]
        correct_answer = next_question.correct_letter
        correct_option_id = sorted_options.index(correct_answer)

        await bot.send_poll(
            chat_id=chat_id,
            question=f"Вопрос {current_index + 1}",
            options=sorted_options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False
        )

        await state.set_state(ListeningFirstStates.answer)
    else:
        # Завершаем первую часть
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score

        await state.update_data(
            part_1_completed=True,
            total_score=total_score
        )

        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_TASK_COMPLETED.format(score=part_score, total=len(questions))
        )

        # Показываем кнопку для перехода ко второй части
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=TEXT_CONTINUE_TO_NEXT_PART,
                callback_data=CALLBACK_LISTENING_PART_2
            )
        )

        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_PART_2,
            reply_markup=builder.as_markup()
        )


@router.poll_answer(ListeningFirstStates.answer)
async def handle_first_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    """Обработчик ответов первой части"""
    data = await state.get_data()
    current_index = data["current_index"]
    questions = data["questions"]
    options = data["options"]

    current_question = questions[current_index]
    sorted_options = sorted(options)
    correct_option_id = sorted_options.index(current_question.correct_letter)
    is_correct = poll_answer.option_ids[0] == correct_option_id

    await state.update_data(
        current_index=current_index + 1,
        part_score=data["part_score"] + int(is_correct)
    )

    await send_next_first_question(poll_answer.bot, poll_answer.user.id, state)


@router.callback_query(F.data == CALLBACK_LISTENING_PART_2)
async def start_part_2(callback: CallbackQuery, state: FSMContext):
    """Запускает вторую часть - SecondTask"""
    data = await state.get_data()
    variant_id = data["variant_id"]

    second_tasks = listening_service.get_second_tasks_by_variant(variant_id)

    if not second_tasks:
        await callback.message.answer("Задания второй части не найдены.")
        return

    await callback.message.answer(text=SECOND_TASK_TEXT)

    await state.update_data(
        current_index=0,
        questions=[{"text": task.text, "is_correct": task.is_correct} for task in second_tasks],
        part_score=0
    )

    await send_next_second_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_second_question(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос второй части"""
    data = await state.get_data()
    current_index = data["current_index"]
    questions = data["questions"]

    if current_index < len(questions):
        current_question = questions[current_index]

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
        # Завершаем вторую часть
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score

        await state.update_data(
            part_2_completed=True,
            total_score=total_score
        )

        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_TASK_COMPLETED.format(score=part_score, total=len(questions))
        )

        # Показываем кнопку для перехода к третьей части
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=TEXT_CONTINUE_TO_NEXT_PART,
                callback_data=CALLBACK_LISTENING_PART_3
            )
        )

        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_PART_3,
            reply_markup=builder.as_markup()
        )


@router.callback_query(F.data.startswith(("true_", "false_")))
async def handle_second_answer(callback: CallbackQuery, state: FSMContext):
    """Обработчик ответов второй части"""
    data = await state.get_data()
    current_index = data["current_index"]
    questions = data["questions"]

    user_answer, question_idx = callback.data.split("_")
    question_idx = int(question_idx)

    if question_idx != current_index:
        await callback.answer("Пожалуйста, отвечайте по порядку!", show_alert=True)
        return

    current_question = questions[current_index]
    is_correct = (user_answer == "true") == current_question["is_correct"]

    new_score = data["part_score"] + int(is_correct)
    new_index = current_index + 1

    await state.update_data(
        current_index=new_index,
        part_score=new_score
    )

    feedback = "✅ Верно!" if is_correct else "❌ Неверно!"
    correct_answer = TEXT_TRUE if current_question["is_correct"] else TEXT_FALSE
    await callback.message.edit_text(
        f"{callback.message.text}\n\n{feedback}\nПравильный ответ: {correct_answer}"
    )

    await send_next_second_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data == CALLBACK_LISTENING_PART_3)
async def start_part_3(callback: CallbackQuery, state: FSMContext):
    """Запускает третью часть - ThirdTask"""
    data = await state.get_data()
    variant_id = data["variant_id"]

    third_tasks = listening_service.get_third_tasks_by_variant(variant_id)

    if not third_tasks:
        await callback.message.answer("Задания третьей части не найдены.")
        return

    tasks_data = []
    for task in third_tasks:
        options = {opt.letter: opt.text for opt in task.options}
        tasks_data.append({
            'task_id': task.id,
            'correct_letter': task.correct_letter,
            'options': options
        })

    await callback.message.answer(text=THIRD_TASK_TEXT)

    await state.update_data(
        current_index=0,
        tasks=tasks_data,
        part_score=0,
        total_questions=len(tasks_data)
    )

    await send_next_third_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_third_question(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос третьей части"""
    data = await state.get_data()
    current_index = data["current_index"]
    tasks = data["tasks"]
    total_questions = data["total_questions"]

    if current_index < total_questions:
        current_task = tasks[current_index]

        options_list = [f"{letter}. {text}"
                        for letter, text in current_task['options'].items()]
        sorted_options = sorted(options_list)

        correct_option_text = f"{current_task['correct_letter']}. {current_task['options'][current_task['correct_letter']]}"
        correct_option_id = sorted_options.index(correct_option_text)

        await bot.send_poll(
            chat_id=chat_id,
            question=f"Вопрос {current_index + 1} из {total_questions}",
            options=sorted_options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False
        )

        await state.update_data(correct_option_id=correct_option_id)
        await state.set_state(ListeningThirdStates.answer)
    else:
        # Завершаем третью часть и весь тест
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score

        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_TASK_COMPLETED.format(score=part_score, total=total_questions)
        )

        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}</b>"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.listening)


@router.poll_answer(ListeningThirdStates.answer)
async def handle_third_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    """Обработчик ответов третьей части"""
    data = await state.get_data()

    is_correct = poll_answer.option_ids[0] == data["correct_option_id"]

    await state.update_data(
        current_index=data["current_index"] + 1,
        part_score=data["part_score"] + int(is_correct)
    )

    await send_next_third_question(poll_answer.bot, poll_answer.user.id, state)