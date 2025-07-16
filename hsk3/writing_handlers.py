from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.services import writing_service
from hsk3.states import WritingStates
from hsk3.intro import get_back_to_types, Sections

router = Router()


@router.callback_query(F.data == "hsk3_writing")
async def get_writing(callback: CallbackQuery):
    text = "Выберите тип задания:"
    type_one = InlineKeyboardButton(text="Тип 1", callback_data="hsk_3_writing_type_one_tasks")
    type_two = InlineKeyboardButton(text="Тип 2", callback_data="hsk_3_writing_type_two_tasks")

    builder = InlineKeyboardBuilder()
    builder.add(type_one, type_two)
    builder.adjust(1)

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == "hsk_3_writing_type_one_tasks")
async def get_writing_type_one_tasks(callback: CallbackQuery, state: FSMContext):
    tasks = writing_service.get_type_one_tasks()

    await state.update_data(
        tasks=tasks,
        index=0,
        score=0
    )
    await send_next_task(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def send_next_task(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    tasks = data["tasks"]
    score = data["score"]

    if index < len(tasks):
        current_task = tasks[index]
        text = f"<b>{index + 1}. Составьте правильное предложение из следующих иероглифов:</b>\n\nИероглифы: {current_task.chars}\n\nНапишите предложение в чат."

        await bot.send_message(chat_id, text=text)
        await state.set_state(WritingStates.word)
    else:
        text = f"Задание выполнено!🎉\nРезультат: {score}/{len(tasks)}"
        await bot.send_message(chat_id, text)
        await state.clear()
        await get_back_to_types(bot, chat_id, section=Sections.writing)


@router.message(WritingStates.word)
async def handle_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    tasks = data["tasks"]
    score = data["score"]

    current_task = tasks[index]

    if msg.text == current_task.correct_sentence:
        score += 1
        await state.update_data(score=score)
        await msg.reply("Это правильный ответ! <b>+1 балл</b>")
    else:
        await msg.reply(f"Это неправильный ответ.\nПравильно будет так: <b>{current_task.correct_sentence}</b>")

    index += 1
    await state.update_data(index=index)

    await send_next_task(msg.bot, msg.chat.id, state)
