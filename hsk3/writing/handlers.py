from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .service import service
from .schemas import *
from .states import *
from aiogram.fsm.context import FSMContext
from hsk3.intro import Sections, get_back_to_types

router = Router()

# CALLBACK КОНСТАНТЫ
CALLBACK_WRITING_VARIANT = "writing_variant"

# ТЕКСТОВЫЕ КОНСТАНТЫ
TEXT_CHOOSE_VARIANT = "<b>Выберите вариант для прохождения:</b>"
TEXT_TASK_COMPLETED = "Задание выполнено!🎉\nРезультат: <b>{score}/{total}</b>"
TEXT_ALL_PARTS_COMPLETED = "Все части пройдены! 🎉\nОбщий результат: <b>{score}/{total}</b>"
TEXT_FIRST_TASK = "<b>Составьте из иероглифов правильные предложения:</b>"
TEXT_FIRST_TASK_SAMPLE = "<b>Задание {index}/{total}</b>\n\nИероглифы: <b>{chars}</b>\n\nНапишите предложение в чат."
TEXT_SECOND_TASK = "<b>Вставьте нужные иероглифы в предложения:</b>"
TEXT_SECOND_TASK_SAMPLE = "<b>Задание {index}/{total}</b>\n\nПредложение: <b>{text}</b>\n\nНапишите иероглиф в чат."
CORRECT_ANSWER = "Это правильно!\n<b>+1 балл</b>"
WRONG_ANSWER = "Это неправильно. Правильно будет: <b>{correct_answer}</b>"


@router.callback_query(F.data == Sections.writing)
async def show_writing_variants(callback: CallbackQuery):
    variants = service.get_variants()
    if not variants:
        await callback.message.answer("Извините, варианты заданий временно недоступны.")
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()
    for num, variant in enumerate(variants, start=1):
        builder.add(
            InlineKeyboardButton(
                text=f"Вариант {num}",
                callback_data=f"{CALLBACK_WRITING_VARIANT}_{variant.id}"
            )
        )
    builder.adjust(1)

    await callback.message.answer(TEXT_CHOOSE_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_WRITING_VARIANT))
async def start_variant(callback: CallbackQuery, state: FSMContext):
    var_id = int(callback.data.split("_")[-1])
    var = service.get_variant_by_id(variant_id=var_id)

    # Сохраняем все данные варианта в state
    await state.update_data(
        variant=var,
        first_tasks=var.first_tasks,
        second_tasks=var.second_tasks,
        total_score=0,
        current_part="first"  # Отслеживаем текущую часть
    )

    await start_first_tasks(callback.bot, callback.message.chat.id, state)
    await callback.answer()


async def start_first_tasks(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    first_tasks = data['first_tasks']

    await bot.send_message(chat_id=chat_id, text=TEXT_FIRST_TASK)
    await state.update_data(
        index=0,
        tasks=first_tasks,
        score=0
    )

    await send_next_task(bot, chat_id, state, is_first=True)


async def start_second_tasks(bot: Bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    second_tasks = data['second_tasks']

    await bot.send_message(chat_id=chat_id, text=TEXT_SECOND_TASK)
    await state.update_data(
        index=0,
        tasks=second_tasks,
        score=0,
        current_part="second"
    )

    await send_next_task(bot, chat_id, state, is_first=False)


async def send_next_task(bot: Bot, chat_id: int, state: FSMContext, is_first=True):
    data = await state.get_data()
    index = data['index']
    tasks = data['tasks']
    score = data.get('score', 0)

    if index < len(tasks):
        curr_task = tasks[index]
        if is_first:
            await bot.send_message(chat_id=chat_id, text=TEXT_FIRST_TASK_SAMPLE.format(
                index=index + 1,
                total=len(tasks),
                chars=curr_task.chars
            ))
            await state.set_state(FirstTaskStates.sentence)
        else:
            await bot.send_message(chat_id=chat_id, text=TEXT_SECOND_TASK_SAMPLE.format(
                index=index + 1,
                total=len(tasks),
                text=curr_task.text
            ))
            await state.set_state(SecondTaskStates.char)
    else:
        # Задания текущей части завершены
        data = await state.get_data()
        current_part = data.get('current_part', 'first')
        total_score = data.get('total_score', 0)

        await bot.send_message(chat_id=chat_id, text=TEXT_TASK_COMPLETED.format(
            score=score,
            total=len(tasks)
        ))

        if current_part == "first":
            # Переходим ко второй части
            await state.update_data(total_score=total_score + score)
            await start_second_tasks(bot, chat_id, state)
        else:
            # Все части завершены
            final_score = total_score + score
            first_tasks = data['first_tasks']
            second_tasks = data['second_tasks']
            total_tasks = len(first_tasks) + len(second_tasks)

            # Проверяем, является ли это частью полного теста
            if data.get("full_test_mode"):
                from hsk3.full_test import complete_full_test
                await complete_full_test(bot, chat_id, state, final_score, total_tasks)
            else:
                await bot.send_message(chat_id=chat_id, text=TEXT_ALL_PARTS_COMPLETED.format(
                    score=final_score,
                    total=total_tasks
                ))
                await state.clear()


@router.message(FirstTaskStates.sentence)
async def handle_next_first_task(msg: Message, state: FSMContext):
    data = await state.get_data()
    index = data['index']
    tasks = data['tasks']
    score = data.get("score", 0)

    curr_task = tasks[index]

    if msg.text == curr_task.correct_answer:
        score += 1
        await msg.reply(text=CORRECT_ANSWER)
    else:
        await msg.reply(text=WRONG_ANSWER.format(correct_answer=curr_task.correct_answer))

    index += 1

    await state.update_data(
        index=index,
        score=score
    )

    await send_next_task(msg.bot, msg.chat.id, state, is_first=True)


@router.message(SecondTaskStates.char)
async def handle_next_second_task(msg: Message, state: FSMContext):
    data = await state.get_data()
    index = data['index']
    tasks = data['tasks']
    score = data.get("score", 0)

    curr_task = tasks[index]

    if msg.text == curr_task.correct_answer:
        score += 1
        await msg.reply(text=CORRECT_ANSWER)
    else:
        print(curr_task.correct_answer)
        await msg.reply(text=WRONG_ANSWER.format(correct_answer=curr_task.correct_answer))

    index += 1

    await state.update_data(
        index=index,
        score=score
    )

    await send_next_task(msg.bot, msg.chat.id, state, is_first=False)
