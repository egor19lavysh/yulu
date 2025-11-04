from aiogram import F, Router
from .intro import Sections, get_back_to_types
from aiogram.types import CallbackQuery

router = Router()

# ССЫЛКА-ЗАГЛУШКА
LINK = "Данный раздел в разработке.\nМожете перейти на quizlet:\nhttps://quizlet.com/ru/1090660528/hsk-5%E7%BA%A7-flash-cards/?i=4fixki&x=1jqt"


@router.callback_query(F.data == Sections.words)
async def get_quizlet_link(callback: CallbackQuery):
    await callback.message.answer(text=LINK)
    await get_back_to_types(callback.bot, callback.message.chat.id, Sections.words)
    await callback.answer()
