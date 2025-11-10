from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.types import ContentType
from config import settings
from .sub_repository import get_sub_repo
import asyncio
from datetime import datetime, date


router = Router()
repo = asyncio.run(get_sub_repo())

@router.message(Command("subscribe"))
async def buy(message: Message):
    PRICE = LabeledPrice(label="Подписка на 1 месяц (тест)", amount=300*100)
    
    try:
        await message.bot.send_invoice(
            chat_id=message.chat.id,
            title="Тестовая подписка",
            description="Тестовая активация подписки на 1 месяц",
            provider_token=settings.PAYMENTS_TOKEN,
            currency="RUB",
            prices=[PRICE],
            start_parameter="test-subscription",
            payload=f"test_{message.from_user.id}",
        )
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("❌ Ошибка создания платежа")
    
@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    # Проверяем данные перед оплатой
    await pre_checkout_q.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payment = message.successful_payment


    await repo.extend_sub(message.from_user.id, start_date=date.today())
    
    await message.answer(
        f"✅ Платеж на сумму {payment.total_amount // 100} {payment.currency} прошел успешно!\n"
        f"Спасибо за покупку подписки!"
    )

@router.message(Command("status"))
async def show_subscription_status(message: Message):
    sub = await repo.get_by_user_id(user_id=message.from_user.id)
    await message.answer((f"Ваша подписка: {sub.sub_type}\n \
                         Начало: {sub.start_date}\n \
                         Конец: {sub.end_date}\n \
                         Статус: {'Истекла' if sub.is_expired else 'Активна'}"))
