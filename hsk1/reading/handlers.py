from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk1.intro import Sections, get_back_to_types
from .service import service
from .states import *


router = Router()

### Callback значения
CALLBACK_READING_VARIANT = "hsk1_reading_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_PART_3 = "Задание 3"
TEXT_PART_4 = "Задание 4"

TEXT_TASK_1 = "Текст 1"
TEXT_TASK_2 = "Текст 2"
TEXT_TASK_3 = "Текст 3"
TEXT_TASK_4 = "Текст 4"

TEXT_TRUE = "Правда"
TEXT_FALSE = "Ложь"
ANSWER_RIGHT = "✅ Верно!"
ANSWER_FALSE = "❌ Неверно!"

TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"
TEXT_NO_TASKS = "Задания не найдены."
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_TASKS_COMPLETED = "Общий результат: <b>{score}/{total}</b>"

TEXT_NO_VARIANTS = "Нет вариантов"


@router.callback_query(F.data == Sections.reading)
async def show_reading_variants(callback: CallbackQuery):
    if variants := service.get_reading_variants():
        builder = InlineKeyboardBuilder()
        for num, variant in enumerate(variants, start=1):
            builder.add(
                InlineKeyboardButton(
                    text=f"Вариант {num}",
                    callback_data=f"{CALLBACK_READING_VARIANT}_{variant.id}"
                )
            )
        builder.adjust(1)
        await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    else:
        await callback.message.answer(TEXT_NO_VARIANTS)
        await get_back_to_types(callback.bot, callback.message.chat.id, Sections.listening)

    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data.startswith(CALLBACK_READING_VARIANT))
async def start_reading(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])
    await state.update_data(
        variant_id=var_id,
        chat_id=callback.message.chat.id
    )
    await start_reading_variant(callback=callback, state=state)


async def start_reading_variant(state: FSMContext, callback: CallbackQuery = None, bot: Bot = None):
    if bot is None:
        bot = callback.bot
    
    data = await state.get_data()

    if data.get("listening_variant_id", False):
        var_id = data["reading_variant_id"]
    else:
        var_id = data["variant_id"]

    chat_id = data["chat_id"]

    if callback:
        await callback.message.delete()
        await callback.answer()


    # Сохраняем данные варианта в состояние
    await state.update_data(
        variant_id=var_id,
        total_score=0,
    )

    # Запускаем первую часть
    await bot.send_message(chat_id, TEXT_PART_1)
    await start_part_1(bot, state)

async def start_part_1(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := service.get_first_tasks_by_variant(variant_id=variant_id):
        task = tasks[0]

        await bot.send_message(chat_id, TEXT_TASK_1)
        await bot.send_photo(chat_id, task.picture_id)

        await state.update_data(
            questions=task.options,
            index=0,
            score=0
        )

        await handle_first_task(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим ко второму заданию")
        await bot.send_message(chat_id, TEXT_PART_2)
        await start_part_2(bot, state)

async def handle_first_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    questions = data["questions"]
    index = data["index"]
    score = data["score"]

    if index < len(questions):
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=TEXT_TRUE,
                callback_data=f"hsk1_reading_true_{index + 1}"
            ),
            InlineKeyboardButton(
                text=TEXT_FALSE,
                callback_data=f"hsk1_reading_false_{index + 1}"
            )
        )

        await bot.send_message(
            chat_id=chat_id,
            text=f"Вопрос {index + 1}/{len(questions)}",
            reply_markup=builder.as_markup()
        )

        await state.set_state(ReadingFirstTask.answer)

    else:
        await state.update_data(
            total_score=data["total_score"] + score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)
        await start_part_2(bot, state)

@router.callback_query(F.data.startswith(("hsk1_reading_true_", "hsk1_reading_false_")))
async def handle_first_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    questions = data["questions"]
    index = data["index"]
    score = data["score"]

    bool_dict = {
        "true": True,
        "false": False
    }

    curr_task = questions[index]
    answer = callback.data.split("_")[2]

    if bool_dict[answer] == curr_task.is_correct:
        score = score + 1
        await callback.message.edit_text(
            f"{callback.message.text}\n{ANSWER_RIGHT}"
        )
    else:
        await callback.message.edit_text(f"{callback.message.text}\n{ANSWER_FALSE}")

    new_index = index + 1

    await state.update_data(
        index=new_index,
        score=score
    )

    await handle_first_task(callback.bot, state)


async def start_part_2(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := service.get_second_tasks_by_variant(variant_id=variant_id):
        task = tasks[0]

        await bot.send_message(chat_id, TEXT_TASK_2)
        await bot.send_photo(chat_id, task.picture_id)

        await state.update_data(
            sentences=task.sentences,
            index=0,
            score=0
        )

        await handle_second_task(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим к третьему заданию")
        await bot.send_message(chat_id, TEXT_PART_3)
        await start_part_3(bot, state)

async def handle_second_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    sentences = data["sentences"]
    index = data["index"]
    score = data["score"]
    chat_id = data["chat_id"]

    if index < len(sentences):
        curr_sentence = sentences[index]
        await bot.send_poll(
            chat_id, 
            f"{index + 1}. {curr_sentence.text}",
            options=["A", "B", "C", "D", "E", "F"],
            is_anonymous=False,
            correct_option_id=ord(curr_sentence.correct_letter) - ord("A"),
            type="quiz"
        )

        await state.set_state(ReadingSecondTask.answer)
    else:
        await state.update_data(
            total_score=data["total_score"] + score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
        await start_part_3(bot, state)

@router.poll_answer(ReadingSecondTask.answer)
async def handle_second_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    sentences = data["sentences"]
    index = data["index"]
    curr_sentence = sentences[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_sentence.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_second_task(bot=poll_answer.bot, state=state)

async def start_part_3(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := service.get_third_tasks_by_variant(variant_id=variant_id):
        task = tasks[0]

        await bot.send_message(chat_id, TEXT_TASK_3)
        options = "\n".join(f"<b>{op.letter}</b>. {op.text}" for op in task.options)
        
        await bot.send_message(chat_id, options)
        
        await state.update_data(
            sentences=task.sentences,
            index=0,
            score=0
        )

        await handle_third_task(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим к четвертому заданию")
        await bot.send_message(chat_id, TEXT_PART_4)
        await start_part_4(bot, state)

async def handle_third_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    sentences = data["sentences"]
    index = data["index"]
    score = data["score"]
    chat_id = data["chat_id"]

    if index < len(sentences):
        curr_sentence = sentences[index]
        await bot.send_poll(
            chat_id, 
            f"{index + 1}. {curr_sentence.text}",
            options=["A", "B", "C", "D", "E", "F"],
            is_anonymous=False,
            correct_option_id=ord(curr_sentence.correct_letter) - ord("A"),
            type="quiz"
        )

        await state.set_state(ReadingThirdTask.answer)
    else:
        await state.update_data(
            total_score=data["total_score"] + score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await start_part_4(bot, state)

@router.poll_answer(ReadingThirdTask.answer)
async def handle_third_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    sentences = data["sentences"]
    index = data["index"]
    curr_sentence = sentences[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_sentence.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_third_task(bot=poll_answer.bot, state=state)

async def start_part_4(bot: Bot, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    chat_id = data["chat_id"]

    if tasks := service.get_fourth_tasks_by_variant(variant_id=variant_id):
        task = tasks[0]

        await bot.send_message(chat_id, TEXT_TASK_4)
        options = "\n".join(f"<b>{op.letter}</b>. {op.text}" for op in task.options)
        
        await bot.send_message(chat_id, options)
        
        await state.update_data(
            sentences=task.sentences,
            index=0,
            score=0
        )

        await handle_fourth_task(bot, state)
    else:
        await bot.send_message(chat_id, "Задание не найдено... Переходим к концу варианта")
        await bot.send_message(chat_id, TEXT_PART_4)
        await finish_reading(bot, state)

async def handle_fourth_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    sentences = data["sentences"]
    index = data["index"]
    score = data["score"]
    chat_id = data["chat_id"]

    if index < len(sentences):
        curr_sentence = sentences[index]
        await bot.send_poll(
            chat_id, 
            f"{index + 1}. {curr_sentence.text}",
            options=["A", "B", "C", "D", "E", "F"],
            is_anonymous=False,
            correct_option_id=ord(curr_sentence.correct_letter) - ord("A"),
            type="quiz"
        )

        await state.set_state(ReadingFourthTask.answer)
    else:
        await state.update_data(
            total_score=data["total_score"] + score
        )

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await finish_reading(bot, state)

@router.poll_answer(ReadingFourthTask.answer)
async def handle_fourth_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    sentences = data["sentences"]
    index = data["index"]
    curr_sentence = sentences[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_sentence.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_fourth_task(bot=poll_answer.bot, state=state)

async def finish_reading(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    total_score = data["total_score"]

    await state.update_data(
        reading_score=total_score,
    )
    if data.get("is_full_test", False):
        from hsk1.full_test import finish_full_test
        await finish_full_test(bot=bot, state=state)
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}/20</b>"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.reading)