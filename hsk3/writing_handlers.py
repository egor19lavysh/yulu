from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.services import writing_service
from hsk3.states import WritingStates
from hsk3.intro import get_back_to_types, Sections

router = Router()

# Константы для callback данных
CALLBACK_HSK3_WRITING = "hsk3_writing"
CALLBACK_TYPE_ONE_TASKS = "hsk_3_writing_type_one_tasks"
CALLBACK_TYPE_TWO_TASKS = "hsk_3_writing_type_two_tasks"

# Текстовые константы
TEXT_CHOOSE_TASK_TYPE = "Выберите тип задания:"
TEXT_TYPE_ONE = "Тип 1"
TEXT_TYPE_TWO = "Тип 2"
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: {score}/{total}"
TEXT_CORRECT_ANSWER = "Это правильный ответ! <b>+1 балл</b>"
TEXT_WRONG_ANSWER = "Это неправильный ответ.\nПравильно будет так: <b>{correct_answer}</b>"


async def show_task_types(callback: CallbackQuery):
    """Показывает типы заданий для письменной части."""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=TEXT_TYPE_ONE, callback_data=CALLBACK_TYPE_ONE_TASKS),
        InlineKeyboardButton(text=TEXT_TYPE_TWO, callback_data=CALLBACK_TYPE_TWO_TASKS)
    )
    builder.adjust(1)

    await callback.message.answer(TEXT_CHOOSE_TASK_TYPE, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


async def start_task_session(
        callback: CallbackQuery,
        state: FSMContext,
        task_getter: callable,
        task_handler: callable
):
    """Начинает сессию заданий."""
    tasks = task_getter()
    await state.update_data(tasks=tasks, index=0, score=0)
    await task_handler(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_task(
        bot: Bot,
        chat_id: int,
        state: FSMContext,
        task_formatter: callable,
        next_state: WritingStates
):
    """Отправляет следующее задание пользователю."""
    data = await state.get_data()
    index = data["index"]
    tasks = data["tasks"]
    score = data["score"]

    if index < len(tasks):
        current_task = tasks[index]
        text = task_formatter(current_task, index)
        await bot.send_message(chat_id, text=text)
        await state.set_state(next_state)
    else:
        await finish_task_session(bot, chat_id, state, score, len(tasks))


async def finish_task_session(bot: Bot, chat_id: int, state: FSMContext, score: int, total: int):
    """Завершает сессию заданий и показывает результаты."""
    await bot.send_message(chat_id, TEXT_TASK_COMPLETED.format(score=score, total=total))
    await state.clear()
    await get_back_to_types(bot, chat_id, section=Sections.writing)


async def handle_task_answer(
        msg: Message,
        state: FSMContext,
        correct_answer_extractor: callable,
        task_handler: callable
):
    """Обрабатывает ответ пользователя на задание."""
    data = await state.get_data()
    index = data["index"]
    tasks = data["tasks"]
    score = data["score"]

    current_task = tasks[index]
    correct_answer = correct_answer_extractor(current_task)

    if msg.text == correct_answer:
        score += 1
        await state.update_data(score=score)
        await msg.reply(TEXT_CORRECT_ANSWER)
    else:
        await msg.reply(TEXT_WRONG_ANSWER.format(correct_answer=correct_answer))

    index += 1
    await state.update_data(index=index)
    await task_handler(msg.bot, msg.chat.id, state)


# Форматтеры заданий
def format_type_one_task(task, index):
    return f"<b>{index + 1}. Составьте правильное предложение из следующих иероглифов:</b>\n\nИероглифы: {task.chars}\n\nНапишите предложение в чат."


def format_type_two_task(task, index):
    return f"<b>{index + 1}. Вставьте правильный иероглиф в предложение:</b>\n\nПредложение: {task.sentence}\n\nНапишите иероглиф в чат."


# Обработчики callback
@router.callback_query(F.data == CALLBACK_HSK3_WRITING)
async def handle_writing_callback(callback: CallbackQuery):
    await show_task_types(callback)


@router.callback_query(F.data == CALLBACK_TYPE_ONE_TASKS)
async def handle_type_one_tasks(callback: CallbackQuery, state: FSMContext):
    await start_task_session(
        callback,
        state,
        writing_service.get_type_one_tasks,
        lambda bot, chat_id, state: send_next_task(
            bot, chat_id, state, format_type_one_task, WritingStates.word
        )
    )


@router.callback_query(F.data == CALLBACK_TYPE_TWO_TASKS)
async def handle_type_two_tasks(callback: CallbackQuery, state: FSMContext):
    await start_task_session(
        callback,
        state,
        writing_service.get_type_two_tasks,
        lambda bot, chat_id, state: send_next_task(
            bot, chat_id, state, format_type_two_task, WritingStates.word
        )
    )


# Обработчики ответов
@router.message(WritingStates.word)
async def handle_word_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    tasks = data["tasks"]
    current_task = tasks[data["index"]]

    # Определяем тип задания по структуре задачи
    if hasattr(current_task, 'correct_sentence'):
        correct_answer_extractor = lambda task: task.correct_sentence
        task_handler = lambda bot, chat_id, state: send_next_task(
            bot, chat_id, state, format_type_one_task, WritingStates.word
        )
    else:
        correct_answer_extractor = lambda task: task.correct_char
        task_handler = lambda bot, chat_id, state: send_next_task(
            bot, chat_id, state, format_type_two_task, WritingStates.word
        )

    await handle_task_answer(
        msg,
        state,
        correct_answer_extractor,
        task_handler
    )
