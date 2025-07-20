import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from config import settings
from hsk3 import routers as hsk3_routers

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Yulu - бот для подготовки к HSK!")

# @dp.message()
# async def handle_media(message: types.Message):
#     # Если это фото
#     if message.photo:
#         file_id = message.photo[-1].file_id  # Берем самое высокое качество
#         await message.reply(f"📷 Photo file_id: <code>{file_id}</code>", parse_mode="HTML")
#
#     # Если это видео
#     elif message.video:
#         file_id = message.video.file_id
#         await message.reply(f"🎥 Video file_id: <code>{file_id}</code>", parse_mode="HTML")
#
#     # Если это аудио
#     elif message.audio:
#         file_id = message.audio.file_id
#         await message.reply(f"🔊 Audio file_id: <code>{file_id}</code>", parse_mode="HTML")
#
#     # Если это документ (например, PDF)
#     elif message.document:
#         file_id = message.document.file_id
#         await message.reply(f"📄 Document file_id: <code>{file_id}</code>", parse_mode="HTML")
#
#     # Если это голосовое сообщение
#     elif message.voice:
#         file_id = message.voice.file_id
#         await message.reply(f"🎤 Voice file_id: <code>{file_id}</code>", parse_mode="HTML")
#
#     # Если это стикер
#     elif message.sticker:
#         file_id = message.sticker.file_id
#         await message.reply(f"😀 Sticker file_id: <code>{file_id}</code>", parse_mode="HTML")


# Запуск процесса поллинга новых апдейтов
async def main():
    for router in hsk3_routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
