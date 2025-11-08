from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk4.intro import Sections, get_back_to_types
from .service import get_writing_service
from .states import *
import asyncio


router = Router()
service = asyncio.run(get_writing_service())

### Callback значения
CALLBACK_WRITING_VARIANT = "hsk4_writing_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"

TEXT_TASK_1 = "Составьте правильные по грамматике предложения из следующих иероглифов"
TEXT_TASK_2 = (
    "Вам даны картинки и слова к ним. Напишите предложения, связанные с этими картинками, использовав примеденные слова"
    "\n\n* <i>баллы за это задания считаться не будут, т.к. задание подразумевает разные ответы</i>")

TEXT_TASK_2_SAMPLE = "Напишите предложение к картинке {picture_num}\n\nИероглифы: <b>{word}</b>"

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
                callback_data="back_to_sections_hsk4"
            )
        )
    builder.adjust(1)
    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_WRITING_VARIANT))
async def start_writing(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])
    await state.update_data(variant_id=var_id)
    await start_writing_variant(callback, state)


async def start_writing_variant(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    var_id = data["variant_id"]

    await state.update_data(
        variant_id=var_id,
        total_score=0,
        chat_id=callback.message.chat.id
    )

    await callback.message.answer(TEXT_PART_1)
    await start_part_1(callback, state)
    await callback.answer()


async def start_part_1(callback: CallbackQuery, state: FSMContext):
    variant_id = (await state.get_data())["variant_id"]
    if first_tasks := await service.get_first_tasks_by_variant(var_id=variant_id):
        await state.update_data(
            first_tasks=first_tasks,
            index=0,
            score=0
        )

        await callback.message.answer(text=TEXT_TASK_1)
        await handle_first_tasks(bot=callback.bot, state=state)

    else:
        await callback.message.answer(TEXT_NO_TASKS)
        await callback.answer()
        await callback.message.answer(TEXT_PART_2)
        await start_part_2(bot=callback.bot, state=state)


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
        await state.set_state(HSK4WritingFirstTask.answer)
    else:
        total_score += score
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=10))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)

        await state.update_data(
            total_score=total_score
        )
        await start_part_2(bot=bot, state=state)


@router.message(HSK4WritingFirstTask.answer)
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
        await state.set_state(HSK4WritingFirstTask.answer)
        return

    await state.update_data(index=index + 1)

    await handle_first_tasks(msg.bot, state)


async def start_part_2(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if second_task := await service.get_second_task_by_variant(var_id=variant_id):
        await state.update_data(
            second_task_words=second_task.words,
            index=0,
            score=0
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_2)
        await bot.send_photo(chat_id=chat_id, photo=second_task.picture_id)
        await handle_second_task(bot=bot, state=state)

    else:
        await bot.send_message(chat_id=chat_id, text=TEXT_NO_TASKS)
        await finish_writing(bot=bot, state=state)


async def handle_second_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    words = data["second_task_words"]
    index = data["index"]
    score = data["score"]
    total_score = data["total_score"]

    if index < len(words):
        word = words[index]
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_2_SAMPLE.format(picture_num=96 + index, word=word.text))
        await state.set_state(HSK4WritingSecondTask.answer)
    else:
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))

        await finish_writing(bot=bot, state=state)


@router.message(HSK4WritingSecondTask.answer)
async def handle_second_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    words = data["second_task_words"]
    index = data["index"]

    word = words[index]

    if msg.text:
        await msg.reply(f"<b>Ответ принят!</b>\nВозможный ответ: {word.possible_answer}")
        await state.update_data(
            index=index + 1
        )
        await handle_second_task(msg.bot, state)

    else:
        await msg.reply("Ответьте текстом!")
        await state.set_state(HSK4WritingSecondTask.answer)
        return


async def finish_writing(bot: Bot, state: FSMContext):
    data = await state.get_data()
    total_score = data["total_score"]
    chat_id = data["chat_id"]

    if data.get("is_full_test", False):
        # Сохраняем результат письма и завершаем полный тест
        await state.update_data(
            writing_score=total_score
        )
        # Импортируем функцию из full_test
        from hsk4.full_test import finish_full_test
        await finish_full_test(bot, chat_id, state)
        return
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}/15 +5 возможных баллов</b>"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.writing)
