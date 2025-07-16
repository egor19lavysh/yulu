from database import get_db_session
from hsk3.writing_models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        task = WritingTaskTypeOne(chars="Би Бек Айл", correct_sentence="Айл Би Бек")

        session.add(task)
        session.commit()


    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
