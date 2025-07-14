from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.services import writing_service
from hsk3.states import WritingStates

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
    await callback.answer()

@router.callback_query(F.data == "hsk_3_writing_type_one_tasks")
async def get_writing_type_one_tasks(callback: CallbackQuery, state: FSMContext):
    tasks = writing_service.get_type_one_tasks()

    await state.update_data(
        tasks=tasks,
        current_task=0,
        score=0
    )

    ...

