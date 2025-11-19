from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config import settings
from subscription.sub_repository import get_sub_repo
import asyncio


router = Router()
sub_repo = asyncio.run(get_sub_repo())

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    # Проверяем, что команда отправлена из админской беседы
    if message.chat.id != settings.FEEDBACK_PRIVATE_GROUP_ID:
        return
    
    # Получаем текст рассылки (всё после команды /broadcast)
    broadcast_text = message.text.replace('/broadcast', '').strip()
    
    if not broadcast_text:
        await message.answer("Использование: /broadcast ваш текст рассылки")
        return
    
    subs = await sub_repo.get_all_subs()

    for sub in subs:
        try:
            await message.bot.send_message(chat_id=sub.user_id, text=broadcast_text)
        except Exception as e:
            print(e)


class MSGStates(StatesGroup):
    text = State()

@router.message(Command("send_msg_to"))
async def msg_handler(message: Message, state: FSMContext):
    # Проверяем, что команда отправлена из админской беседы
    if message.chat.id != settings.FEEDBACK_PRIVATE_GROUP_ID:
        return
    
    broadcast_text = message.text.replace('/send_msg_to', '').strip()

    try:
        user_id = int(broadcast_text)
    except Exception as e:
        print(e)
        await message.answer("Использование: /send_msg_to id пользователя")
        return
    
    await state.update_data(
        user_id=user_id
    )

    await message.answer("Напишите сообщение пользователю")
    await state.set_state(MSGStates.text)

@router.message(MSGStates.text)
async def cmd_send_msg_to_user(message: Message, state: FSMContext):
    if message.chat.id != settings.FEEDBACK_PRIVATE_GROUP_ID:
        return
    
    data = await state.get_data()

    user_id = data["user_id"]

    if message.text:
        try:
            await message.bot.send_message(chat_id=user_id, text=message.text)
        except Exception as e:
            print(e)




    
    