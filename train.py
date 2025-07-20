from sqlalchemy import select

from database import get_db_session
from hsk3.listening_models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        print("h")
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
