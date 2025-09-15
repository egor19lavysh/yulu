from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hsk3.intro import Sections, get_back_to_types

# Импорты сервисов всех разделов
from hsk3.listening.service import service as listening_service
from hsk3.reading.service import service as reading_service
from hsk3.writing.service import service as writing_service

# Импорты функций для запуска разделов
from hsk3.listening.handlers import start_listening_variant
from hsk3.reading.handlers import start_reading_variant
from hsk3.writing.handlers import start_first_tasks

router = Router()

# Константы
TEXT_CHOOSE_FULL_VARIANT = "Выберите вариант для полного прохождения HSK 3:"
TEXT_STARTING_LISTENING = "🎧 <b>Раздел 1: Аудирование</b>"
TEXT_STARTING_READING = "📖 <b>Раздел 2: Чтение</b>"
TEXT_STARTING_WRITING = "✍️ <b>Раздел 3: Письмо</b>"
TEXT_FULL_TEST_COMPLETED = """
🎉 <b>Полный тест HSK 3 завершен!</b>

📊 <b>Итоговые результаты:</b>
🎧 Аудирование: {listening_score}
📖 Чтение: {reading_score}
✍️ Письмо: {writing_score}

<b>Общий результат: {total_score} из {total_possible}</b>
"""

CALLBACK_FULL_VARIANT = "full_variant"


@router.callback_query(F.data == "hsk3_full_test")
async def show_full_variants(callback: CallbackQuery):
    """Показывает варианты для полного прохождения"""
    # Получаем варианты из всех разделов
    listening_variants = listening_service.get_listening_variants()
    reading_variants = reading_service.get_reading_variants()
    writing_variants = writing_service.get_reading_variants()

    # Находим минимальное количество вариантов среди всех разделов
    min_variants_count = min(len(listening_variants), len(reading_variants), len(writing_variants))

    if min_variants_count == 0:
        await callback.message.answer("Извините, полные варианты временно недоступны.")
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()
    for i in range(min_variants_count):
        builder.add(
            InlineKeyboardButton(
                text=f"Полный вариант {i + 1}",
                callback_data=f"{CALLBACK_FULL_VARIANT}_{i}"
            )
        )
    builder.adjust(1)

    await callback.message.answer(TEXT_CHOOSE_FULL_VARIANT, reply_markup=builder.as_markup())
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data.startswith(CALLBACK_FULL_VARIANT))
async def start_full_variant(callback: CallbackQuery, state: FSMContext):
    """Начинает полное прохождение варианта"""
    variant_index = int(callback.data.split("_")[-1])

    # Получаем варианты всех разделов
    listening_variants = listening_service.get_listening_variants()
    reading_variants = reading_service.get_reading_variants()
    writing_variants = writing_service.get_reading_variants()

    # Получаем конкретные варианты по индексу
    listening_variant = listening_variants[variant_index]
    reading_variant = reading_variants[variant_index]
    writing_variant_list = writing_variants[variant_index]

    # Получаем полные объекты вариантов с задачами
    listening_full = listening_service.get_listening_variant(listening_variant.id)
    reading_full = reading_service.get_reading_variant(reading_variant.id)
    writing_full = writing_service.get_variant_by_id(writing_variant_list.id)

    # Подсчитываем общее количество вопросов для каждого раздела
    # Аудирование
    listening_first_tasks = listening_service.get_first_tasks_by_variant(listening_variant.id)
    listening_second_tasks = listening_service.get_second_tasks_by_variant(listening_variant.id)
    listening_third_tasks = listening_service.get_third_tasks_by_variant(listening_variant.id)

    listening_total = (
            sum(len(task.questions) for task in listening_first_tasks) +
            len(listening_second_tasks) +
            sum(len(task.questions) for task in listening_third_tasks)
    )

    # Чтение
    reading_first_tasks = reading_service.get_first_tasks_by_variant(reading_variant.id)
    reading_second_tasks = reading_service.get_second_tasks_by_variant(reading_variant.id)
    reading_third_tasks = reading_service.get_third_tasks_by_variant(reading_variant.id)

    reading_total = (
            sum(len(task.questions) for task in reading_first_tasks) +
            sum(len(task.questions) for task in reading_second_tasks) +
            len(reading_third_tasks)
    )

    # Письмо - используем полный объект
    writing_total = len(writing_full.first_tasks) + len(writing_full.second_tasks)

    # Инициализируем состояние для полного теста
    await state.update_data(
        full_test_mode=True,
        full_test_variant_index=variant_index,
        variant_ids={
            "listening": listening_variant.id,
            "reading": reading_variant.id,
            "writing": writing_variant_list.id
        },
        current_section="listening",
        section_results={
            "listening": {"score": 0, "total": listening_total},
            "reading": {"score": 0, "total": reading_total},
            "writing": {"score": 0, "total": writing_total}
        }
    )

    # Начинаем с аудирования
    await callback.message.answer(TEXT_STARTING_LISTENING)
    await start_listening_section(callback, state, listening_variant.id)
    await callback.answer()


async def start_listening_section(callback: CallbackQuery, state: FSMContext, variant_id: int):
    """Запускает раздел аудирования"""
    # Создаем новый объект CallbackQuery с нужными данными
    from types import SimpleNamespace

    # Создаем имитацию CallbackQuery для передачи в существующую функцию
    fake_callback = SimpleNamespace()
    fake_callback.data = f"listening_variant_{variant_id}"
    fake_callback.bot = callback.bot
    fake_callback.message = callback.message
    fake_callback.answer = callback.answer

    # Вызываем существующую функцию
    await start_listening_variant(fake_callback, state)


async def complete_listening_and_start_reading(bot: Bot, chat_id: int, state: FSMContext, score: int, total: int):
    """Завершает аудирование и начинает чтение"""
    data = await state.get_data()
    section_results = data["section_results"]
    # Используем предварительно подсчитанное значение, но обновляем score
    section_results["listening"]["score"] = score

    await state.update_data(
        current_section="reading",
        section_results=section_results
    )

    await bot.send_message(chat_id, TEXT_STARTING_READING)

    # Создаем имитацию CallbackQuery для запуска чтения
    from types import SimpleNamespace

    fake_callback = SimpleNamespace()
    fake_callback.data = f"reading_variant_{data['variant_ids']['reading']}"
    fake_callback.bot = bot
    fake_callback.message = SimpleNamespace()
    fake_callback.message.chat = SimpleNamespace()
    fake_callback.message.chat.id = chat_id
    fake_callback.message.answer = lambda text, reply_markup=None: bot.send_message(chat_id, text,
                                                                                    reply_markup=reply_markup)
    fake_callback.message.delete = lambda: None
    fake_callback.answer = lambda: None

    await start_reading_variant(fake_callback, state)


async def complete_reading_and_start_writing(bot: Bot, chat_id: int, state: FSMContext, score: int, total: int):
    """Завершает чтение и начинает письмо"""
    data = await state.get_data()
    section_results = data["section_results"]
    # Используем предварительно подсчитанное значение, но обновляем score
    section_results["reading"]["score"] = score

    await state.update_data(
        current_section="writing",
        section_results=section_results
    )

    await bot.send_message(chat_id, TEXT_STARTING_WRITING)

    # Получаем вариант письма и запускаем его
    variant_id = data['variant_ids']['writing']
    var = writing_service.get_variant_by_id(variant_id=variant_id)

    await state.update_data(
        variant=var,
        first_tasks=var.first_tasks,
        second_tasks=var.second_tasks,
        total_score=0,
        current_part="first"
    )

    await start_first_tasks(bot, chat_id, state)


async def complete_full_test(bot: Bot, chat_id: int, state: FSMContext, writing_score: int, writing_total: int):
    """Завершает полный тест"""
    data = await state.get_data()
    section_results = data["section_results"]
    # Используем предварительно подсчитанное значение, но обновляем score
    section_results["writing"]["score"] = writing_score

    total_score = sum(result["score"] for result in section_results.values())
    total_possible = sum(result["total"] for result in section_results.values())

    await bot.send_message(
        chat_id,
        TEXT_FULL_TEST_COMPLETED.format(
            listening_score=f"{section_results['listening']['score']}/{section_results['listening']['total']}",
            reading_score=f"{section_results['reading']['score']}/{section_results['reading']['total']}",
            writing_score=f"{section_results['writing']['score']}/{section_results['writing']['total']}",
            total_score=total_score,
            total_possible=total_possible
        )
    )

    await state.clear()
    await get_back_to_types(bot, chat_id, Sections.full_test)
