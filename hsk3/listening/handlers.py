from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.intro import Sections, get_back_to_types
from .service import service  # Убедитесь, что сервис корректно получает данные из репозиториев
from .states import ListeningFirstStates, ListeningSecondStates, ListeningThirdStates

router = Router()

# Тексты
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Часть 1"
TEXT_PART_2 = "Часть 2"
TEXT_PART_3 = "Часть 3"
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"

# Callback значения
CALLBACK_HSK3_LISTENING = "hsk3_listening"
CALLBACK_LISTENING_VARIANT = "listening_variant"

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
    variants = service.get_listening_variants()
    if not variants:
        await callback.message.answer("Извините, варианты заданий временно недоступны.")
        await callback.answer()
        return
    builder = InlineKeyboardBuilder()
    for num, variant in enumerate(variants, start=1):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num}",
                callback_data=f"{CALLBACK_LISTENING_VARIANT}_{variant.id}"
            )
        )
    builder.adjust(1)
    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_LISTENING_VARIANT))
async def start_listening_variant(callback: CallbackQuery, state: FSMContext):
    """Начинает прохождение выбранного варианта"""
    variant_id = int(callback.data.split("_")[-1])
    variant = service.get_listening_variant(variant_id)
    if not variant:
        await callback.message.answer("Вариант не найден.")
        await callback.answer()
        return

    # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=variant_id,
        total_score=0
    )

    # Отправляем аудио
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
    await callback.answer()


# --- Первая часть ---
async def start_part_1(callback: CallbackQuery, state: FSMContext, variant_id: int):
    """Запускает первую часть - FirstTask. Задания идут строго последовательно."""
    first_tasks = service.get_first_tasks_by_variant(variant_id)
    if not first_tasks:
        await callback.message.answer("Задания первой части не найдены.")
        await callback.answer()
        # Переход ко второй части, если первой нет
        await callback.message.answer(TEXT_PART_2)
        await start_part_2_direct(callback.bot, callback.message.chat.id, state)
        return

    # Сохраняем список заданий (FirstTask) в состоянии
    await state.update_data(
        first_tasks=[task for task in first_tasks],  # Сохраняем сами объекты FirstTask
        current_task_index=0,  # Индекс текущего FirstTask
        part_score=0
    )

    # Начинаем с первого задания
    await send_next_first_task(callback.bot, callback.message.chat.id, state)


async def send_next_first_task(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующее FirstTask (картинка + вопросы)"""
    data = await state.get_data()
    first_tasks = data["first_tasks"]
    current_task_index = data["current_task_index"]

    if current_task_index < len(first_tasks):
        current_task = first_tasks[current_task_index]

        # Отправляем картинку для текущего задания
        await bot.send_photo(
            chat_id=chat_id,
            photo=current_task.picture_id,
            caption=f"{PICTURES_CHOICE} - Задание {current_task_index + 1}"
        )

        # Подготавливаем вопросы для текущего задания
        questions = current_task.questions  # Это список FirstTaskQuestion

        # Создаем список всех возможных вариантов ответов (A, B, C, D, etc.) для этого конкретного задания
        # Предполагаем, что все вопросы в рамках одного FirstTask используют одинаковый набор букв
        if questions:
            options = list(set([q.correct_letter for q in questions]))
            options.sort()
        else:
            options = []

        # Обновляем состояние для текущего задания
        await state.update_data(
            current_question_index=0,  # Индекс текущего вопроса внутри текущего FirstTask
            questions=questions,  # Список вопросов текущего FirstTask
            options=options,  # Варианты ответов для текущего FirstTask
            total_questions=len(questions)  # Общее кол-во вопросов в текущем FirstTask
        )

        # Отправляем первый вопрос текущего задания
        await send_next_first_question_in_task(bot, chat_id, state)

    else:
        # Все FirstTask завершены
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score
        await state.update_data(total_score=total_score)
        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_TASK_COMPLETED.format(score=part_score, total=sum(len(task.questions) for task in first_tasks))
        )
        # Переходим ко второй части
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)
        await start_part_2_direct(bot, chat_id, state)


async def send_next_first_question_in_task(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос в рамках текущего FirstTask"""
    data = await state.get_data()
    current_question_index = data["current_question_index"]
    questions = data["questions"]  # Вопросы текущего FirstTask
    options = data["options"]  # Варианты текущего FirstTask
    total_questions = data["total_questions"]  # Всего вопросов в текущем FirstTask
    current_task_index = data["current_task_index"]  # Для отображения номера задания

    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        correct_answer = next_question.correct_letter
        try:
            correct_option_id = options.index(correct_answer)
        except ValueError:
            await bot.send_message(chat_id,
                                   f"Ошибка: правильный ответ '{correct_answer}' не найден в списке опций {options} для вопроса {next_question.id}.")
            return

        await bot.send_poll(
            chat_id=chat_id,
            question=f"Задание {current_task_index + 1}, Вопрос {current_question_index + 1} из {total_questions}",
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False
        )
        await state.set_state(ListeningFirstStates.answer)
    else:
        # Все вопросы текущего FirstTask завершены
        # Переходим к следующему FirstTask
        await state.update_data(current_task_index=data["current_task_index"] + 1)
        await send_next_first_task(bot, chat_id, state)


@router.poll_answer(ListeningFirstStates.answer)
async def handle_first_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    """Обработчик ответов первой части"""
    data = await state.get_data()
    current_question_index = data["current_question_index"]
    questions = data["questions"]  # Вопросы текущего FirstTask
    options = data["options"]  # Варианты текущего FirstTask

    if current_question_index >= len(questions):
        # Неожиданный ответ, вопросы закончились
        return

    current_question = questions[current_question_index]
    correct_option_id = options.index(current_question.correct_letter)
    is_correct = poll_answer.option_ids[0] == correct_option_id

    # Обновляем счетчики
    await state.update_data(
        current_question_index=current_question_index + 1,
        part_score=data["part_score"] + int(is_correct)
    )

    # Отправляем следующий вопрос или переходим к следующему заданию
    await send_next_first_question_in_task(poll_answer.bot, poll_answer.user.id, state)


# --- Вторая часть ---
async def start_part_2_direct(bot: Bot, chat_id: int, state: FSMContext):
    """Запускает вторую часть напрямую"""
    data = await state.get_data()
    variant_id = data["variant_id"]
    second_tasks = service.get_second_tasks_by_variant(variant_id)
    if not second_tasks:
        await bot.send_message(chat_id, "Задания второй части не найдены.")
        # Переход к третьей части, если второй нет
        await bot.send_message(chat_id, text=TEXT_PART_3)
        await start_part_3_direct(bot, chat_id, state)
        return

    await bot.send_message(chat_id, text=SECOND_TASK_TEXT)
    await state.update_data(
        current_index=0,
        questions=[{"id": task.id, "text": task.text, "is_correct": task.is_correct} for task in second_tasks],
        part_score=0
    )
    await send_next_second_question(bot, chat_id, state)


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
            text=f"Вопрос {current_index + 1}/{len(questions)}\n{current_question['text']}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(ListeningSecondStates.answer)
    else:
        # Завершаем вторую часть и переходим к третьей
        part_score = data["part_score"]
        total_score = data["total_score"] + part_score
        await state.update_data(total_score=total_score)
        await bot.send_message(
            chat_id=chat_id,
            text=TEXT_TASK_COMPLETED.format(score=part_score, total=len(questions))
        )
        # Автоматически переходим к третьей части
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
        await start_part_3_direct(bot, chat_id, state)


@router.callback_query(F.data.startswith(("true_", "false_")))
async def handle_second_answer(callback: CallbackQuery, state: FSMContext):
    """Обработчик ответов второй части"""
    data = await state.get_data()
    current_index = data["current_index"]
    questions = data["questions"]

    try:
        user_answer, question_idx_str = callback.data.split("_")
        question_idx = int(question_idx_str)
    except ValueError:
        await callback.answer("Ошибка в данных ответа.", show_alert=True)
        return

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
        f"{callback.message.text}\n{feedback}\nПравильный ответ: {correct_answer}"
    )

    # Отправляем следующий вопрос или завершаем часть
    await send_next_second_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


# --- Третья часть ---
async def start_part_3_direct(bot: Bot, chat_id: int, state: FSMContext):
    """Запускает третью часть напрямую"""
    data = await state.get_data()
    variant_id = data["variant_id"]
    # Используем правильный метод из сервиса, который должен получать ThirdTask
    # со всеми связанными ThirdTaskQuestion и ThirdTaskOption
    third_tasks = service.get_third_tasks_by_variant(variant_id)
    if not third_tasks:
        await bot.send_message(chat_id, "Задания третьей части не найдены.")
        # Завершаем тест, если третьей части нет
        total_score = data["total_score"]
        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}</b>"
        )
        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.listening)
        return

    await bot.send_message(chat_id, text=THIRD_TASK_TEXT)

    # Подготавливаем список всех вопросов с опциями
    all_questions_data = []
    for task in third_tasks:
        for question in task.questions:  # ThirdTaskQuestion
            # Собираем опции для этого конкретного вопроса
            options_dict = {opt.letter: opt.text for opt in question.options}  # ThirdTaskOption
            all_questions_data.append({
                'question_id': question.id,
                'correct_letter': question.correct_letter,
                'options': options_dict  # {'A': 'Текст A', 'B': 'Текст B', ...}
            })

    await state.update_data(
        current_index=0,
        questions=all_questions_data,  # Список подготовленных данных вопросов
        part_score=0,
        total_questions=len(all_questions_data)
    )
    await send_next_third_question(bot, chat_id, state)


async def send_next_third_question(bot: Bot, chat_id: int, state: FSMContext):
    """Отправляет следующий вопрос третьей части"""
    data = await state.get_data()
    current_index = data["current_index"]
    questions_data = data["questions"]  # Список подготовленных данных вопросов
    total_questions = data["total_questions"]

    if current_index < total_questions:
        current_question_data = questions_data[current_index]

        # Формируем список опций в формате ["A. Текст A", "B. Текст B", ...]
        options_list = [f"{letter}. {text}" for letter, text in current_question_data['options'].items()]
        options_list.sort()  # Сортируем по буквам

        # Находим ID правильного варианта для Poll
        correct_option_text = f"{current_question_data['correct_letter']}. {current_question_data['options'][current_question_data['correct_letter']]}"
        try:
            correct_option_id = options_list.index(correct_option_text)
        except ValueError:
            await bot.send_message(chat_id,
                                   f"Ошибка: правильный ответ '{correct_option_text}' не найден в списке опций {options_list} для вопроса {current_question_data['question_id']}.")
            return

        await bot.send_poll(
            chat_id=chat_id,
            question=f"Вопрос {current_index + 1} из {total_questions}",
            options=options_list,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=False
        )
        # Сохраняем ID правильного варианта для проверки
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

    # Проверяем, что данные существуют
    if "correct_option_id" not in data:
        # Возможно, состояние было потеряно или ответ пришел несвоевременно
        return

    is_correct = poll_answer.option_ids[0] == data["correct_option_id"]

    # Обновляем счетчики
    await state.update_data(
        current_index=data["current_index"] + 1,
        part_score=data["part_score"] + int(is_correct)
    )

    # Отправляем следующий вопрос или завершаем часть
    await send_next_third_question(poll_answer.bot, poll_answer.user.id, state)
