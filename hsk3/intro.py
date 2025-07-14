from aiogram.filters import Command
from aiogram.types import Message, PollAnswer, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, Bot, F

router = Router()


@router.message(Command("hsk3"))
async def get_sections(msg: Message):
    text = "<b>Выберите, что вы хотите потренировать:</b>"
    builder = InlineKeyboardBuilder()

    listening = InlineKeyboardButton(text="Аудирование", callback_data="hsk3_reading")
    reading = InlineKeyboardButton(text="Чтение", callback_data="hsk3_reading")
    writing = InlineKeyboardButton(text="Грамматика", callback_data="hsk3_writing")
    words = InlineKeyboardButton(text="Лексика", callback_data="hsk3_words")

    builder.add(listening, reading, writing, words)
    builder.adjust(1)

    await msg.answer(text, reply_markup=builder.as_markup())
