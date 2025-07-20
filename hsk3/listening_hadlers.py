from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.intro import Sections
from hsk3.services import listening_service

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
FIRST_TASK_TEXT = "Сопоставьте картинки с репликами:"

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
async def get_first_task(callback: CallbackQuery):
    task = listening_service.get_test_first_task()

    await callback.message.answer(text=FIRST_TASK_TEXT)
    for picture in task.pictures:
        await callback.bot.send_photo(chat_id=callback.message.chat.id, photo=picture.picture_id, caption=picture.letter)

    await callback.answer()
