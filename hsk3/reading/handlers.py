from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, PollAnswer, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.intro import Sections, get_back_to_types
from hsk3.reading.service import service
from .states import QuizStates

router = Router()

# Текстовые константы
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Часть 1 - Задания типа 1"
TEXT_PART_2 = "Часть 2 - Задания типа 2"
TEXT_PART_3 = "Часть 3 - Задания типа 3"
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉\nОбщий результат: <b>{total_score}</b>"
TEXT_FIRST_TASK_DESCRIPTION = "<b>Соотнесите реплики со следующими вопросами:</b>"
TEXT_SECOND_TASK_DESCRIPTION = "<b>Вставьте следующие иероглифы по смыслу в предложения:</b>"
TEXT_THIRD_TASK_DESCRIPTION = "<b>Выберите верное суждение из реплики:</b>"

# Callback значения
CALLBACK_HSK3_READING = "hsk3_reading"
CALLBACK_READING_VARIANT = "reading_variant"


@router.callback_query(F.data == Sections.reading)
async def show_reading_variants(callback: CallbackQuery):
    """Показывает доступные варианты reading заданий"""
    variants = service.get_reading_variants()
    if not variants:
        await callback.message.answer("Извините, варианты заданий временно недоступны.")
        await callback.answer()
        return

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
                callback_data="back_to_sections_hsk3"
            )
        )
    builder.adjust(1)

    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_READING_VARIANT))
async def start_reading_variant(callback: CallbackQuery, state: FSMContext):
    """Начинает прохождение выбранного варианта"""
    variant_id = int(callback.data.split("_")[-1])
    variant = service.get_reading_variant(variant_id)

    if not variant:
        await callback.message.answer("Вариант не найден.")
        await callback.answer()
        return

    # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=variant_id,
        total_score=0
    )

    # Запускаем первую часть
    await callback.message.answer(TEXT_PART_1)
    await start_part_1(callback, state, variant_id)
    await callback.answer()


# --- Первая часть (Задания типа 1) ---
async def start_part_1(callback: CallbackQuery, state: FSMContext, variant_id: int):
    """Запускает первую часть - задания типа 1"""
    first_tasks = service.get_first_tasks_by_variant(variant_id)

    if not first_tasks:
        await callback.message.answer("Задания первой части не найдены.")
        # Переход ко второй части, если первой нет
        await callback.message.answer(TEXT_PART_2)
        await start_part_2_direct(callback.bot, callback.message.chat.id, state)
        return

    # Сохраняем список заданий в состоянии
    await state.update_data(
        first_tasks=first_tasks,
        current_task_index=0,
        part_score=0
    )

    # Начинаем с первого задания
    await send_next_first_task(callback.bot, callback.message.chat.id, state)


async def send_next_first_task(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующее задание типа 1"""
    data = await state.get_data()
    first_tasks = data["first_tasks"]
    current_task_index = data["current_task_index"]

    if current_task_index < len(first_tasks):
        current_task = first_tasks[current_task_index]

        # Формируем текст задания
        task_text = TEXT_FIRST_TASK_DESCRIPTION + "\n\n"
        for option in current_task.options:
            task_text += f"{option.letter}. {option.text}\n"

        # Сохраняем вопросы текущего задания в состоянии
        await state.update_data(
            current_question_index=0,
            questions=current_task.questions,
            options=[option.letter for option in current_task.options]
        )

        await bot.send_message(chat_id, task_text)
        await send_next_first_question(bot, chat_id, state)
    else:
        # Все задания типа 1 завершены
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score
        total_questions = sum(len(task.questions) for task in first_tasks)

        await state.update_data(total_score=total_score)
        await bot.send_message(
            chat_id,
            TEXT_TASK_COMPLETED.format(score=part_score, total=total_questions)
        )

        # Очистим данные первой части и переходим ко второй части
        new_data = {
            k: v for k, v in data.items()
            if k not in ["first_tasks", "current_task_index", "current_question_index", "questions", "options",
                         "part_score"]
        }
        new_data["total_score"] = total_score
        await state.set_data(new_data)

        # Переходим ко второй части
        await bot.send_message(chat_id, TEXT_PART_2)
        await start_part_2_direct(bot, chat_id, state)


async def send_next_first_question(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос в текущем задании типа 1"""
    data = await state.get_data()
    current_question_index = data["current_question_index"]
    questions = data["questions"]
    options = data["options"]
    current_task_index = data["current_task_index"]

    if current_question_index < len(questions):
        question = questions[current_question_index]

        await bot.send_poll(
            chat_id=chat_id,
            question=f"Вопрос {current_question_index + 1}\n{question.text}",
            options=options,
            type="quiz",
            correct_option_id=ord(question.correct_letter) - ord('A'),
            is_anonymous=False
        )
        await state.set_state(QuizStates.WAITING_FOR_ANSWER)
    else:
        # Все вопросы текущего задания завершены
        await state.update_data(current_task_index=data["current_task_index"] + 1)
        await send_next_first_task(bot, chat_id, state)


# --- Вторая часть (Задания типа 2) ---
async def start_part_2_direct(bot: Bot, chat_id: int, state: FSMContext):
    """Запускает вторую часть напрямую"""
    data = await state.get_data()
    variant_id = data["variant_id"]
    second_tasks = service.get_second_tasks_by_variant(variant_id)

    if not second_tasks:
        await bot.send_message(chat_id, "Задания второй части не найдены.")
        # Переход к третьей части, если второй нет
        await bot.send_message(chat_id, TEXT_PART_3)
        await start_part_3_direct(bot, chat_id, state)
        return

    await state.update_data(
        second_tasks=second_tasks,
        current_task_index=0,
        part_score=0
    )

    await send_next_second_task(bot, chat_id, state)


async def send_next_second_task(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующее задание типа 2"""
    data = await state.get_data()
    second_tasks = data["second_tasks"]
    current_task_index = data["current_task_index"]

    if current_task_index >= len(second_tasks):
        # Все задания типа 2 завершены
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score
        total_questions = sum(len(task.questions) for task in second_tasks)

        await state.update_data(total_score=total_score)
        await bot.send_message(
            chat_id,
            TEXT_TASK_COMPLETED.format(score=part_score, total=total_questions)
        )

        # Очистим данные второй части и переходим к третьей части
        new_data = {
            k: v for k, v in data.items()
            if k not in ["second_tasks", "current_task_index", "current_question_index", "questions", "options",
                         "part_score"]
        }
        new_data["total_score"] = total_score
        await state.set_data(new_data)

        # Переходим к третьей части
        await bot.send_message(chat_id, TEXT_PART_3)
        await start_part_3_direct(bot, chat_id, state)
        return

    current_task = second_tasks[current_task_index]

    # Формируем текст задания
    task_text = TEXT_SECOND_TASK_DESCRIPTION + "\n\n"
    for option in current_task.options:
        task_text += f"{option.letter}. {option.text}\n"

    # Сохраняем вопросы текущего задания в состоянии
    await state.update_data(
        current_question_index=0,
        questions=current_task.questions,
        options=[option.letter for option in current_task.options]
    )

    await bot.send_message(chat_id, task_text)
    await send_next_second_question(bot, chat_id, state)


async def send_next_second_question(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос в текущем задании типа 2"""
    data = await state.get_data()
    current_question_index = data["current_question_index"]
    questions = data["questions"]
    options = data["options"]

    if current_question_index < len(questions):
        question = questions[current_question_index]

        await bot.send_poll(
            chat_id=chat_id,
            question=f"Вопрос {current_question_index + 1}\n{question.text}",
            options=options,
            type="quiz",
            correct_option_id=ord(question.correct_letter) - ord('A'),
            is_anonymous=False
        )
        await state.set_state(QuizStates.WAITING_FOR_ANSWER)
    else:
        # Все вопросы текущего задания завершены, переходим к следующему заданию
        await state.update_data(current_task_index=data["current_task_index"] + 1)
        await send_next_second_task(bot, chat_id, state)


# --- Третья часть (Задания типа 3) ---
async def start_part_3_direct(bot: Bot, chat_id: int, state: FSMContext):
    """Запускает третью часть напрямую"""
    data = await state.get_data()
    variant_id = data["variant_id"]
    third_tasks = service.get_third_tasks_by_variant(variant_id)

    if not third_tasks:
        await bot.send_message(chat_id, "Задания третьей части не найдены.")
        # Завершаем тест, если третьей части нет
        total_score = data["total_score"]
        await bot.send_message(
            chat_id,
            TEXT_ALL_PARTS_COMPLETED.format(total_score=total_score)
        )
        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.reading)
        return

    await state.update_data(
        third_tasks=third_tasks,
        current_task_index=0,
        part_score=0
    )

    await send_next_third_task(bot, chat_id, state)


async def send_next_third_task(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующее задание типа 3"""
    data = await state.get_data()
    third_tasks = data["third_tasks"]
    current_task_index = data["current_task_index"]

    if current_task_index < len(third_tasks):
        task = third_tasks[current_task_index]

        # Формируем текст задания
        task_text = (
            f"Задание {current_task_index + 1}/{len(third_tasks)}\n\n"
            f"{TEXT_THIRD_TASK_DESCRIPTION}\n\n"
            f"{task.text}"  # Убрать строку с task.question
        )

        # Подготавливаем варианты ответов
        options = [f"{opt.letter}. {opt.text}" for opt in task.options]
        correct_index = ord(task.correct_letter) - ord('A')

        await bot.send_message(chat_id, task_text)
        await bot.send_poll(
            chat_id=chat_id,
            question="Выберите правильный ответ:",
            options=options,
            type="quiz",
            correct_option_id=correct_index,
            is_anonymous=False
        )

        await state.update_data(current_task_index=current_task_index + 1)
        await state.set_state(QuizStates.WAITING_FOR_ANSWER)
    else:
        # Все задания типа 3 завершены
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score

        await bot.send_message(
            chat_id,
            TEXT_TASK_COMPLETED.format(score=part_score, total=len(third_tasks))
        )

        # Проверяем, является ли это частью полного теста
        # Проверяем, является ли это частью полного теста
        if data.get("full_test_mode"):
            from hsk3.full_test import complete_reading_and_start_writing
            await complete_reading_and_start_writing(bot, chat_id, state, total_score, 0)  # total не используется
        else:
            await bot.send_message(
                chat_id,
                TEXT_ALL_PARTS_COMPLETED.format(total_score=total_score)
            )
            await state.clear()
            await get_back_to_types(bot, chat_id, Sections.reading)


# Общий обработчик ответов на все типы заданий
@router.poll_answer(QuizStates.WAITING_FOR_ANSWER)
async def handle_reading_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    """Обработчик ответов на все типы заданий чтения"""
    data = await state.get_data()

    # Определяем, какая часть сейчас активна по наличию ключей
    if "first_tasks" in data and "second_tasks" not in data and "third_tasks" not in data:
        # Обработка ответа для первой части
        current_question_index = data["current_question_index"]
        questions = data["questions"]

        is_correct = poll_answer.option_ids[0] == ord(questions[current_question_index].correct_letter) - ord('A')

        await state.update_data(
            current_question_index=current_question_index + 1,
            part_score=data["part_score"] + int(is_correct)
        )

        await send_next_first_question(poll_answer.bot, poll_answer.user.id, state)

    elif "second_tasks" in data and "third_tasks" not in data:
        # Обработка ответа для второй части
        current_question_index = data["current_question_index"]
        questions = data["questions"]

        is_correct = poll_answer.option_ids[0] == ord(questions[current_question_index].correct_letter) - ord('A')

        await state.update_data(
            current_question_index=current_question_index + 1,
            part_score=data["part_score"] + int(is_correct)
        )

        await send_next_second_question(poll_answer.bot, poll_answer.user.id, state)

    elif "third_tasks" in data:
        # Обработка ответа для третьей части
        current_task_index = data["current_task_index"] - 1  # Индекс уже увеличен в send_next_third_task
        if current_task_index >= 0 and current_task_index < len(data["third_tasks"]):
            task = data["third_tasks"][current_task_index]

            is_correct = poll_answer.option_ids[0] == ord(task.correct_letter) - ord('A')

            await state.update_data(
                part_score=data["part_score"] + int(is_correct)
            )

        await send_next_third_task(poll_answer.bot, poll_answer.user.id, state)
