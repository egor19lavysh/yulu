from database import get_db_session
from hsk3.reading_models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        for i in range(10):
            task = ReadingTaskTypeThree(text=f"Текст {i}", question=f"Вопрос {i}", correct_answer_letter="A")
            session.add(task)
            session.flush()  # Получаем ID задания

            # 2. Создаем варианты ответов с ЯВНЫМ указанием task_one_id
            options = [
                SentenceOption(letter="A", text="Текст варианта A", task_three_id=task.id),
                SentenceOption(letter="B", text="Текст варианта B", task_three_id=task.id),
                SentenceOption(letter="C", text="Текст варианта C", task_three_id=task.id)
            ]

            # 4. Добавляем все объекты
            session.add_all(options)
            session.commit()


    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()

create_sample_task()