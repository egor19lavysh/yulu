from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk5.intro import Sections, get_back_to_types
from .service import get_writing_service
from .states import *
import asyncio


router = Router()
service = asyncio.run(get_writing_service())

### Callback значения
CALLBACK_WRITING_VARIANT = "hsk5_writing_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_PART_3 = "Задание 3"

TEXT_TASK_1 = "Составьте правильные по грамматике предложения из следующих иероглифов"
TEXT_TASK_2 = "Напишите текст длиной около 80 иероглифов, используя предоставленные слова:"
TEXT_TASK_3 = "Напишите текст длиной около 80 иероглифов на основе данного изображения:"

TEXT_NO_TASKS = "Задания не найдены."
TASK_FIRST_WARNING = "\n\n* <i>Напишите ответ одним сообщением</i> без пробелов"
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_TASKS_COMPLETED = "Общий результат: <b>{score}/{total}</b>"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"


@router.callback_query(F.data == Sections.writing)
async def show_writing_variants(callback: CallbackQuery):
    variants = await service.get_writing_variants()
    builder = InlineKeyboardBuilder()
    for num, variant in enumerate(variants, start=1):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num}",
                callback_data=f"{CALLBACK_WRITING_VARIANT}_{variant.id}"
            )
        )
    builder.add(
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_to_sections_hsk5"
            )
        )
    builder.adjust(1)
    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_WRITING_VARIANT))
async def start_writing(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.answer()

    var_id = int(callback.data.split("_")[-1])

    await state.update_data(variant_id=var_id,
                            chat_id=callback.message.chat.id)
    
    await start_writing_variant(callback.bot, state)


async def start_writing_variant(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]

    if data.get("writing_variant_id", False):
        var_id = data["writing_variant_id"]
    else:
        var_id = data["variant_id"]

    await state.update_data(
        total_score=0,
        variant_id=var_id
    )

    await bot.send_message(chat_id, TEXT_PART_1)
    await start_part_1(bot, state)

async def start_part_1(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if first_tasks := await service.get_first_tasks_by_variant(var_id=variant_id):
        await state.update_data(
            first_tasks=first_tasks,
            index=0,
            score=0
        )

        await bot.send_message(chat_id, text=TEXT_TASK_1)
        await handle_first_tasks(bot=bot, state=state)

    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим ко второму заданию")
        await bot.send_message(chat_id, TEXT_PART_2)
        await start_part_2(bot=bot, state=state)


async def handle_first_tasks(bot: Bot, state: FSMContext):
    data = await state.get_data()
    tasks = data["first_tasks"]
    chat_id = data["chat_id"]
    index = data["index"]
    score = data["score"]
    total_score = data["total_score"]

    if index < len(tasks):
        curr_task = tasks[index]
        await bot.send_message(chat_id=chat_id,
                               text=f"{index + 1}/{10}. Иероглифы: <b>{curr_task.words}</b>" + TASK_FIRST_WARNING)
        await state.set_state(HSK5WritingFirstTask.answer)
    else:
        total_score += score
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=len(tasks)))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)

        await state.update_data(
            total_score=total_score
        )
        await start_part_2(bot=bot, state=state)


@router.message(HSK5WritingFirstTask.answer)
async def handle_first_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    tasks = data["first_tasks"]
    chat_id = data["chat_id"]
    index = data["index"]
    score = data["score"]

    curr_task = tasks[index]

    if msg.text:

        if curr_task.correct_sentence == msg.text:
            await msg.reply("Правильно!\n<b>+ 1 балл</b>")
            await state.update_data(
                score=score + 1
            )
        else:
            await msg.reply(f"Неправильно!\nПравильно будет так: <b>{curr_task.correct_sentence}</b>")
    else:
        await msg.reply("Ответьте текстом!")
        await state.set_state(HSK5WritingFirstTask.answer)
        return

    await state.update_data(index=index + 1)

    await handle_first_tasks(msg.bot, state)

async def start_part_2(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := await service.get_second_tasks_by_variant(var_id=variant_id):
        task = tasks[0]

        await bot.send_message(chat_id, TEXT_TASK_2)
        await bot.send_message(chat_id, task.text)

        await state.set_state(HSK5WritingSecondTask.answer)
    else:
        await bot.send_message(chat_id, "Задание на найдено... Переходим к третьему заданию")
        await bot.send_message(chat_id, TEXT_PART_3)
        await start_part_3(bot=bot, state=state)

@router.message(HSK5WritingSecondTask.answer)
async def handle_second_answer(msg: Message, state: FSMContext):

    if msg.text:
        await msg.answer("Это задание проверяется вручную, поэтому баллы за это задание выставлены не будут")
    else:
        await msg.reply("Ответьте текстом!")
        await state.set_state(HSK5WritingSecondTask.answer)
        return

    await msg.answer(TEXT_PART_3)
    await start_part_3(bot=msg.bot, state=state)

async def start_part_3(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := await service.get_third_tasks_by_variant(var_id=variant_id):
        task = tasks[0]

        await bot.send_message(chat_id, TEXT_TASK_3)
        await bot.send_photo(chat_id, task.picture_id)

        await state.set_state(HSK5WritingThirdTask.answer)
    else:
        await bot.send_message(chat_id, "Задание на найдено... Переходим к концу варианта")
        await finish_writing(bot=bot, state=state)

@router.message(HSK5WritingThirdTask.answer)
async def handle_second_answer(msg: Message, state: FSMContext):

    if msg.text:
        await msg.answer("Это задание проверяется вручную, поэтому баллы за это задание выставлены не будут")
    else:
        await msg.reply("Ответьте текстом!")
        await state.set_state(HSK5WritingSecondTask.answer)
        return

    await finish_writing(bot=msg.bot, state=state)

async def finish_writing(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    total_score = data["total_score"]

    await state.update_data(
        writing_score=total_score,
    )

    if data.get("is_full_test", False):
        from hsk5.full_test import finish_full_test
        await finish_full_test(bot=bot, state=state)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}/10 + 2 потенциальных балла</b>"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.writing)