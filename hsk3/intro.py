from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, Bot, F

router = Router()


class Sections:
    listening = "hsk3_listening"
    reading = "hsk3_reading"
    writing = "hsk3_writing"
    words = "hsk3_words"
    full_test = "hsk3_full_test"


async def show_sections_menu(chat_id: int, bot: Bot = None, msg: Message = None):
    text = "<b>Выберите, что вы хотите потренировать:</b>"
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text="🎧 Аудирование", callback_data=Sections.listening),
        InlineKeyboardButton(text="📖 Чтение", callback_data=Sections.reading),
        InlineKeyboardButton(text="✍️ Грамматика", callback_data=Sections.writing),
        InlineKeyboardButton(text="🔤 Лексика", callback_data=Sections.words),
        InlineKeyboardButton(text="🎯 Целый вариант", callback_data=Sections.full_test)
    ]

    builder.add(*buttons)
    builder.adjust(1)



    if bot and msg is None:
        await bot.send_message(chat_id, text, reply_markup=builder.as_markup())
    elif msg:
        await msg.answer(text, reply_markup=builder.as_markup())


@router.message(Command("hsk3"))
async def get_sections(msg: Message):
    level_text = "Вы выбрали 3 уровень экзамена HSK 3"
    await msg.answer(text=level_text, reply_markup=ReplyKeyboardRemove())
    await show_sections_menu(msg.chat.id, msg=msg)


async def get_back_to_types(bot: Bot, chat_id: int, section: str):
    builder = InlineKeyboardBuilder()

    tasks_btn = InlineKeyboardButton(text="ЗАДАНИЯ", callback_data=section)
    sections_btn = InlineKeyboardButton(text="РАЗДЕЛЫ", callback_data="back_to_sections")

    builder.add(tasks_btn, sections_btn)
    builder.adjust(1)

    await bot.send_message(chat_id=chat_id, text="Хотите вернуться?", reply_markup=builder.as_markup())


@router.callback_query(F.data == "back_to_sections")
async def back_to_sections_handler(callback: CallbackQuery):
    await callback.message.delete()  # удаляем предыдущее сообщение с кнопками
    await show_sections_menu(callback.message.chat.id, bot=callback.bot)