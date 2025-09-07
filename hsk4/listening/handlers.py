from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk4.intro import Sections, get_back_to_types
from .service import service
from .states import *

router = Router()

### Callback значения
CALLBACK_LISTENING_VARIANT = "listening_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_PART_3 = "Задание 3"
TEXT_NO_TASKS = "Задания не найдены."

TEXT_TASK_1 = "Прослушайте краткие отрывки, и выберите истинны ли утверждения к ним или нет:"

TEXT_TRUE = "Правда"
TEXT_FALSE = "Ложь"

ANSWER_RIGHT = "✅ Верно!"
ANSWER_FALSE = "❌ Неверно!"



@router.callback_query(F.data == Sections.listening)
async def show_listening_variants(callback: CallbackQuery):
    variants = service.get_listening_variants()
    builder = InlineKeyboardBuilder()
    for num, variant in enumerate(variants, start=1):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num}",
                callback_data=f"{CALLBACK_LISTENING_VARIANT}_{variant.id}"
            )
        )
    builder.adjust(1)
    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_LISTENING_VARIANT))
async def start_listening_variant(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])
    variant = service.get_listening_variant(variant_id=var_id)

    if not variant:
        await callback.message.answer("Вариант не найден.")
        await callback.answer()
        return

    # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=var_id,
        total_score=0
    )

    # Запускаем первую часть
    await callback.message.answer(TEXT_PART_1)
    await start_part_1(callback, state)
    await callback.answer()


async def start_part_1(callback: CallbackQuery, state: FSMContext):
    variant_id = int((await state.get_data())["variant_id"])
    if first_tasks := service.get_first_tasks_by_variant(variant_id=variant_id):
        await state.update_data(
            first_tasks=first_tasks,
            index=0,
            score=0
        )

        await callback.message.answer(text=TEXT_TASK_1)
        await handle_first_tasks(callback, state)

    else:
        await callback.message.answer(TEXT_NO_TASKS)
        await callback.answer()
        await callback.message.answer(TEXT_PART_2)
        await start_part_2(callback, state)

async def handle_first_tasks(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tasks = data["first_tasks"]
    index = data["index"]
    score = data["score"]
    total_score = data["total_score"]


    if index < len(tasks):
        current_task = tasks[index]

        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=TEXT_TRUE,
                callback_data=f"true_{index + 1}"
            ),
            InlineKeyboardButton(
                text=TEXT_FALSE,
                callback_data=f"false_{index + 1}"
            )
        )
        await callback.message.send_message(
            text=f"Вопрос {index + 1}/{len(tasks)}\n{current_task.text}",
            reply_markup=builder.as_markup()
        )
    else:
        total_score += score

        await state.update_data(
            total_score=total_score
        )

        await callback.message.answer(text=TEXT_PART_2)
        await start_part_2(callback, state)

@router.callback_query(F.data.startswith(("true_", "false_")))
async def handle_first_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tasks = data["first_tasks"]
    index = data["index"]
    score = data["score"]

    bool_dict = {
        "true": True,
        "false": False
    }

    curr_task = tasks[index]
    answer, task_id = callback.data.split("_")

    if bool_dict[answer] == curr_task.is_correct:
        score = score + 1
        await callback.message.edit_text(ANSWER_RIGHT)
    else:
        await callback.message.edit_text(ANSWER_FALSE)

    new_index = index + 1

    await state.update_data(
        index=new_index,
        score=score
    )

    await handle_first_tasks(callback, state)


async def start_part_2(callback: CallbackQuery, state: FSMContext):
    pass