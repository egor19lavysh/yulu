from sqlalchemy import select

from database import get_db_session
from hsk3.listening_models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        tasks = [SecondTask(text="Текст 2", is_correct=True),
                 SecondTask(text="Текст 3", is_correct=True),
                 SecondTask(text="Текст 4", is_correct=False),
                 SecondTask(text="Текст 5", is_correct=True),
                 SecondTask(text="Текст 6", is_correct=False)
                 ]


        session.add_all(tasks)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
