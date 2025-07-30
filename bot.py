import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import BotCommand, Message, KeyboardButton

from config import settings
from hsk3 import routers as hsk3_routers

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Диспетчер
dp = Dispatcher()

WELCOME_TEXT = """
<b>Привет, {name}! Я - телеграмм бот Yulu.</b>

Я помогу вам подготовиться к экзамену HSK по китайскому языку.

📚 <b>Основные функции:</b>
- Выбор уровня HSK (1-6)
- Тренировка отдельных навыков:
  🔊 Аудирование
  📖 Чтение
  ✍️ Письмо
  📝 Лексика
- Полноценные пробные тесты
- Персональная статистика

🔹 Используйте команду /levels чтобы выбрать уровень HSK и начать подготовку!
🔹 Если вы нашли баг или ошибка, то пишите https://t.me/lavingham
    """


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT.format(name=(message.from_user.first_name + " " + message.from_user.last_name)))

@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT.format(name=(message.from_user.first_name + " " + message.from_user.last_name)))


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


# async def set_bot_commands(dp):
#     commands = [
#         BotCommand("start", "Запустить бота"),
#         BotCommand("help", "Помощь и функции"),
#         BotCommand("1", "1")
#     ]
#     await dp.bot.set_my_commands(commands)

@dp.message(Command("levels"))
async def get_levels(msg: Message):
    levels_kb = [
        [KeyboardButton(text="/hsk1"), KeyboardButton(text="/hsk2")],
        [KeyboardButton(text="/hsk3"), KeyboardButton(text="/hsk4")],
        [KeyboardButton(text="/hsk5"), KeyboardButton(text="/hsk6")]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=levels_kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите уровень HSK"
    )

    await msg.answer("Какой уровень хотите потренировать?", reply_markup=keyboard)

# Запуск процесса поллинга новых апдейтов
async def main():
    for router in hsk3_routers:
        dp.include_router(router)

    await dp.start_polling(bot, allowed_updates=["message", "callback_query", "poll_answer"])


if __name__ == "__main__":
    asyncio.run(main())
