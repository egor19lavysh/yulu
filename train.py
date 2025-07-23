import random

from sqlalchemy import select

from database import get_db_session
from hsk3.listening_models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        for i in range(2, 6):
            options = [
                ThirdTaskOption(letter="A", text=f"Текст {i}"),
                ThirdTaskOption(letter="B", text=f"Текст {i}"),
                ThirdTaskOption(letter="C", text=f"Текст {i}"),
            ]

            letters = ["A", "B", "C"]

            task = ThirdTask(correct_letter=random.choice(letters))
            task.options = options

            session.add(task)
            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
