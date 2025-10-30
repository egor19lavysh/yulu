from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command


router = Router()


@router.message(Command("subscribe"))
async def subscribe(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="💳 Оплатить подписку", callback_data="subscribe"))

    sub_text = """
                Оплачивая подписку, вы получаете:
                - Безлимитный доступ ко всем вариантам и заданиям
                - Эксклюзивные материалы для подготовки
                - Уникальные предложения для очных мероприятий

                Стоимость: 300 руб.
               """
    
    await message.answer(text=sub_text, reply_markup=builder.as_markup())

@router.callback_query(F.data == "subscribe")
async def pay_sub(callback: CallbackQuery):
    await callback.answer("Оплата...")