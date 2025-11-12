import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import BotCommand, Message, KeyboardButton, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import settings
from hsk1 import routers as hsk1_routers
from hsk2 import routers as hsk2_routers
from hsk3 import routers as hsk3_routers
from hsk4 import routers as hsk4_routers
from hsk5 import routers as hsk5_routers
from subscription import router as sub_router
from subscription.sub_repository import get_sub_repo
from subscription.models import Subscription, SubscriptionType
from datetime import date, timedelta
from middleware import SubscriptionMiddleware
from gsclient import GoogleSheetsClient
from datetime import datetime


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
gsclient = GoogleSheetsClient(credentials_file=settings.SERVICE_ACCOUNT_FILE, spreadsheet_id=settings.SPREADSHEET_ID)

# Диспетчер
dp = Dispatcher()

WELCOME_TEXT = """
<b>Привет, {name}! Я - телеграмм бот Yulu.</b>

Я помогу вам подготовиться к экзамену HSK по китайскому языку.

📚 <b>Основные функции:</b>
- Выбор уровня HSK (1-5)
- Тренировка отдельных навыков:
  🔊 Аудирование
  📖 Чтение
  ✍️ Письмо
  📝 Лексика
- Полноценные пробные тесты


🔹 Используйте команду /levels чтобы выбрать уровень HSK и начать подготовку!
🔹 Для оплаты оплаты подписки нажмите /subscribe, а для проверки статуса подписки /status
🔹 Если вы нашли баг или ошибку, хотите задать вопрос или просто поделиться своим мнением о боте, то можете оставить свой фидбэк /feedback
    """
 

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user = message.from_user

    repo = await get_sub_repo()

    if not await repo.get_by_user_id(message.from_user.id):
        sub = Subscription(
            user_id=message.from_user.id,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5)
        )

        await repo.create(subscription=sub)

    
    # Подготавливаем данные пользователя
    user_data = {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # Записываем в Google Sheets
    await gsclient.append_user(user_data)
    await message.answer(WELCOME_TEXT.format(name=message.from_user.username))


@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    TEXT = """
🔹 Используйте команду /levels чтобы выбрать уровень HSK и начать подготовку к экзамену
🔹 Для оплаты оплаты подписки нажмите /subscribe, а для проверки статуса подписки /status
🔹 Если вы нашли баг или ошибку, хотите задать вопрос или просто поделиться своим мнением о боте, то можете оставить свой фидбэк /feedback
"""
    await message.answer(TEXT)


@dp.message(F.audio | F.photo | F.video)
async def handle_media(message: types.Message):
    if message.chat.id == settings.PRIVATE_GROUP_ID:
        # Если это фото
        if message.photo:
            file_id = message.photo[-1].file_id  # Берем самое высокое качество
            await message.reply(f"📷 Photo file_id: <code>{file_id}</code>", parse_mode="HTML")

        # Если это видео
        elif message.video:
            file_id = message.video.file_id
            await message.reply(f"🎥 Video file_id: <code>{file_id}</code>", parse_mode="HTML")

        # Если это аудио
        elif message.audio:
            file_id = message.audio.file_id
            await message.reply(f"🔊 Audio file_id: <code>{file_id}</code>", parse_mode="HTML")


@dp.callback_query(F.data == "levels")
async def get_levels_callback(callback: CallbackQuery):
    await callback.message.delete()
    await get_levels(callback.message)

@dp.message(Command("levels"))
async def get_levels(msg: Message):
    levels_kb = [
        [KeyboardButton(text="/hsk1"), KeyboardButton(text="/hsk2")],
        [KeyboardButton(text="/hsk3"), KeyboardButton(text="/hsk4")],
        [KeyboardButton(text="/hsk5")]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=levels_kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите уровень HSK"
    )

    await msg.answer("Какой уровень хотите потренировать?", reply_markup=keyboard)

class FeedbackStates(StatesGroup):
    feedback = State()


@dp.message(Command("feedback"))
async def give_feedback(message: Message, state: FSMContext):
    TEXT = "Отправьте фидбэк нашим менеджерам в виде текста.\n\nВы можете оставить фидбэк по абсолютно разным причинам:\n- предложить улучшение\n- задать вопрос\n- написать о проблеме\n\nМы ответим вам в ближайшее время!"
    await message.answer(TEXT)
    await state.set_state(FeedbackStates.feedback)

@dp.message(FeedbackStates.feedback)
async def get_feedback(message: Message, state: FSMContext):

    await message.bot.send_message(
        chat_id=settings.FEEDBACK_PRIVATE_GROUP_ID,
        text=f"Пользователь {message.from_user.username} (id={message.from_user.id}) оставил фидбэк:"
    )

    await message.bot.forward_message(
        chat_id=settings.FEEDBACK_PRIVATE_GROUP_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    await message.answer("Спасибо за ваш фидбэк! Если возникла какая-то проблема, наши менеджеры с вами скоро свяжутся.")
    
    await state.clear()
    

# Запуск процесса поллинга новых апдейтов
async def main():
    for router in hsk1_routers:
        dp.include_router(router)

    for router in hsk2_routers:
        dp.include_router(router)

    for router in hsk3_routers:
        dp.include_router(router)

    for router in hsk4_routers:
        dp.include_router(router)

    for router in hsk5_routers:
        dp.include_router(router)

    dp.include_router(sub_router)

    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
