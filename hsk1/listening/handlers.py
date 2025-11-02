from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, PollAnswer
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk1.intro import Sections, get_back_to_types
from .service import service
from .states import *


router = Router()

### Callback значения
CALLBACK_LISTENING_VARIANT = "hsk1_listening_variant"

### Текстовые значения
TEXT_CHOOSE_VARIANT = "Выберите вариант для прохождения:"
TEXT_NO_VARIANTS = "Нет вариантов"
TEXT_PART_1 = "Задание 1"
TEXT_PART_2 = "Задание 2"
TEXT_PART_3 = "Задание 3"
TEXT_PART_4 = "Задание 4"
TEXT_TASK_1 = "Прослушайте 5 фраз и ответьте, соответствуют ли картинки на изображении этим фразам:"
TEXT_TASK_2 = "Прослушайте 5 предложений и выберите картинку, соответствующую каждой реплике:"
TEXT_TASK_3 = "Прослушайте 5 диалогов и выберите картинку, соответствующую каждому диалогу:"
TEXT_TASK_4 = "Прослушайте 5 предложений и ответьте на соответствующие к ним вопросы, выбрав один из трех ответов:"
TEXT_TRUE = "Правда"
TEXT_FALSE = "Ложь"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉"
TEXT_NO_TASKS = "Задания не найдены."
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_TASKS_COMPLETED = "Общий результат: <b>{score}/{total}</b>"
ANSWER_RIGHT = "✅ Верно!"
ANSWER_FALSE = "❌ Неверно!"



@router.callback_query(F.data == Sections.listening)
async def show_listening_variants(callback: CallbackQuery):
    if variants := service.get_listening_variants():
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
    else:
        await callback.message.answer(TEXT_NO_VARIANTS)
        await get_back_to_types(callback.bot, callback.message.chat.id, Sections.listening)

    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_LISTENING_VARIANT))
async def start_listening(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])
    await state.update_data(variant_id=var_id)
    await start_listening_variant(callback, state)


async def start_listening_variant(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get("listening_variant_id", False):
        var_id = data["listening_variant_id"]
    else:
        var_id = data["variant_id"]

    variant = service.get_listening_variant(variant_id=var_id)

    await callback.answer()
    await callback.message.delete()

    if not variant:
        await callback.message.answer("Вариант не найден.")
        await callback.answer()
        return

    # Сохраняем данные варианта в состояние
    await state.update_data(
        chat_id=callback.message.chat.id,
        variant_id=var_id,
        total_score=0
    )

    await callback.bot.send_audio(callback.message.chat.id, variant.audio_id)
    await callback.message.answer(TEXT_PART_1)
    await start_part_1(callback, state)
    

async def start_part_1(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    variant_id = data["variant_id"]
    if first_tasks := service.get_first_tasks_by_variant(variant_id=variant_id):
        first_task = first_tasks[0]

        await callback.message.answer(TEXT_TASK_1)
        await callback.bot.send_photo(callback.message.chat.id, first_task.picture_id)

        await state.update_data(
            questions=first_task.questions,
            index=0,
            score=0
        )

        await handle_first_task(callback.bot, state)
    
    else:
        await callback.message.answer("Первое задание не найдено... Переходим ко второму заданию")
        await state.update_data(
            first_task_score=0
        )
        await callback.message.answer(text=TEXT_PART_2)
        await start_part_2(callback.bot, state)

async def handle_first_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    index = data["index"]
    score = data["score"]
    questions = data["questions"]

    if index < len(questions):
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text=TEXT_TRUE,
                callback_data=f"hsk1_true_{index + 1}"
            ),
            InlineKeyboardButton(
                text=TEXT_FALSE,
                callback_data=f"hsk1_false_{index + 1}"
            )
        )

        await bot.send_message(
            chat_id=chat_id,
            text=f"Вопрос {index + 1}/{len(questions)}",
            reply_markup=builder.as_markup()
        )

        await state.set_state(ListeningFirstStates.answer)

    else:
        await state.update_data(
            total_score=data["total_score"] + score,
            first_task_score=score
        )
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_2)
        await start_part_2(bot, state)

@router.callback_query(F.data.startswith(("hsk1_true_", "hsk1_false_")))
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
    answer = callback.data.split("_")[1]

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

        if second_tasks := service.get_second_tasks_by_variant(variant_id=variant_id):
            second_task = second_tasks[0]

            await bot.send_message(chat_id, TEXT_TASK_2)
            await bot.send_photo(chat_id, second_task.picture_id)

            await state.update_data(
                questions=second_task.questions,
                index=0,
                score=0
            )

            await handle_second_task(bot, state)
        
        else:
            await bot.send_message(chat_id, "Второе задание не найдено... Переходим к третьему заданию")
            await state.update_data(
                second_task_score=0
            )
            await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
            await start_part_3(bot, state)

async def handle_second_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    index = data["index"]
    score = data["score"]
    questions = data["questions"]

    if index < len(questions):
        curr_question = questions[index]
        options = [
           "A", "B", "C"
        ]

        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            correct_option_id=ord(curr_question.correct_letter) - ord("A"),
            is_anonymous=False,
            question=f"Вопрос {index + 1}/{len(questions)}",
            type="quiz"
        )

        await state.set_state(ListeningSecondStates.answer)

    else:
        await state.update_data(
            total_score=data["total_score"] + score,
            second_task_score=score
        )
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_3)
        await start_part_3(bot, state)


@router.poll_answer(ListeningSecondStates.answer)
async def handle_second_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    questions = data["questions"]
    index = data["index"]
    curr_question = questions[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_question.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_second_task(bot=poll_answer.bot, state=state)


async def start_part_3(bot: Bot, state: FSMContext):
        data = await state.get_data()
        variant_id = data["variant_id"]
        chat_id = data["chat_id"]

        if third_tasks := service.get_third_tasks_by_variant(variant_id=variant_id):
            third_task = third_tasks[0]

            await bot.send_message(chat_id, TEXT_TASK_3)
            await bot.send_photo(chat_id, third_task.picture_id)

            await state.update_data(
                questions=third_task.questions,
                index=0,
                score=0
            )

            await handle_third_task(bot, state)
        
        else:
            await bot.send_message(chat_id, "Третье задание не найдено... Переходим к четвертому заданию")
            await state.update_data(
                third_task_score=0
            )
            await bot.send_message(chat_id, TEXT_PART_4)
            await start_part_4(bot, state)

async def handle_third_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    index = data["index"]
    score = data["score"]
    questions = data["questions"]

    if index < len(questions):
        curr_question = questions[index]
        options = [
           "A", "B", "C", "D", "E", "F"
        ]

        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            correct_option_id=ord(curr_question.correct_letter) - ord("A"),
            is_anonymous=False,
            question=f"Вопрос {index + 1}/{len(questions)}",
            type="quiz"
        )

        await state.set_state(ListeningThirdStates.answer)

    else:
        await state.update_data(
            total_score=data["total_score"] + score,
            third_task_score=score
        )
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await bot.send_message(chat_id=chat_id, text=TEXT_PART_4)
        await start_part_4(bot, state)


@router.poll_answer(ListeningThirdStates.answer)
async def handle_third_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    questions = data["questions"]
    index = data["index"]
    curr_question = questions[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_question.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_third_task(bot=poll_answer.bot, state=state)

 
async def start_part_4(bot: Bot, state: FSMContext):
        data = await state.get_data()
        variant_id = data["variant_id"]
        chat_id = data["chat_id"]

        if fourth_tasks := service.get_fourth_tasks_by_variant(variant_id=variant_id):
            fourth_task = fourth_tasks[0]

            await bot.send_message(chat_id, TEXT_TASK_4)

            await state.update_data(
                questions=fourth_task.questions,
                index=0,
                score=0
            )

            await handle_fourth_task(bot, state)
        
        else:
            await bot.send_message(chat_id, "Четвертое задание не найдено... Переходим к концу варианта")
            await state.update_data(
                fourth_task_score=0
            )
            await finish_listening(bot, state)

async def handle_fourth_task(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    index = data["index"]
    score = data["score"]
    questions = data["questions"]

    if index < len(questions):
        curr_question = questions[index]
        options = [
           f"{op.letter}. {op.text}" for op in curr_question.options
        ]

        await bot.send_poll(
            chat_id=chat_id,
            options=options,
            correct_option_id=ord(curr_question.correct_letter) - ord("A"),
            is_anonymous=False,
            question=f"Вопрос {index + 1}/{len(questions)}",
            type="quiz"
        )

        await state.set_state(ListeningFourthStates.answer)

    else:
        await state.update_data(
            total_score=data["total_score"] + score,
            fourth_task_score=score
        )
        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(score=score, total=5))
        await finish_listening(bot, state)


@router.poll_answer(ListeningFourthStates.answer)
async def handle_fourth_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    score = data["score"]
    questions = data["questions"]
    index = data["index"]
    curr_question = questions[index]

    if poll_answer.option_ids:
        is_correct = ord(curr_question.correct_letter) - ord("A") == poll_answer.option_ids[0]
        await state.update_data(
            score=score + (1 if is_correct else 0),
            index=index + 1
        )

    await handle_fourth_task(bot=poll_answer.bot, state=state)

async def finish_listening(bot: Bot, state: FSMContext):
    data = await state.get_data()
    chat_id = data["chat_id"]
    total_score = data["total_score"]

    if data.get("is_full_test", False):
        await state.update_data(
            listening_score=total_score
        )
        await bot.send_message(
            chat_id=chat_id,
            text=f"Аудирование заврешено!\nПереходим к чтению."
        )

        from hsk1.reading.handlers import start_reading_variant
        await start_reading_variant(bot=bot, state=state)
    else:

        await bot.send_message(
            chat_id=chat_id,
            text=f"{TEXT_ALL_PARTS_COMPLETED}\nОбщий результат: <b>{total_score}/20</b>"
        )

        await state.clear()
        await get_back_to_types(bot, chat_id, Sections.listening)

