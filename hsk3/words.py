from aiogram import F, Router
from .intro import Sections, get_back_to_types
from aiogram.types import CallbackQuery

router = Router()

# ССЫЛКА-ЗАГЛУШКА
LINK = "Данный раздел в разработке.\nМожете перейти на quizlet:\nhttps://quizlet.com/ru/1028103886/%E7%AC%AC%E5%8D%81%E4%B8%83%E8%AF%BE-flash-cards/?x=1jqU&i=5bbjpn"


@router.callback_query(F.data == Sections.words)
async def get_quizlet_link(callback: CallbackQuery):
    await callback.message.answer(text=LINK)
    await get_back_to_types(callback.bot, callback.message.chat.id, Sections.words)
    await callback.answer()
