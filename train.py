import random

from sqlalchemy import select

from database import get_db_session
from hsk3.listening_models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        listening = Listening(audio_id="CQACAgIAAxkBAAIC-GiBIC7T-gJ__sO4Mn97GPHQ1EK5AAJEfAACa6QJSPZNA-lFMliwNgQ")

        first_task = FirstTask(picture_id="AgACAgIAAxkBAAIC9GiBH7zGyhQ_wVevqMmWH3Wwkk9wAAKe9TEba6QJSIQAAcQLuDo_lgEAAwIAA3gAAzYE")
        questions1 = [
            FirstTaskQuestion(correct_letter="C"),
            FirstTaskQuestion(correct_letter="F"),
            FirstTaskQuestion(correct_letter="E"),
            FirstTaskQuestion(correct_letter="A"),
            FirstTaskQuestion(correct_letter="B")
        ]

        first_task.questions = questions1

        first_task2 = FirstTask(picture_id="AgACAgIAAxkBAAIC9miBH9UpO02hqF6Ged5C-_c1EP2EAAKf9TEba6QJSLUtNL7E4WSbAQADAgADeAADNgQ")
        questions2 = [
            FirstTaskQuestion(correct_letter="E"),
            FirstTaskQuestion(correct_letter="B"),
            FirstTaskQuestion(correct_letter="A"),
            FirstTaskQuestion(correct_letter="D"),
            FirstTaskQuestion(correct_letter="C")
        ]

        first_task2.questions = questions2

        listening.first_type_tasks = [first_task, first_task2]

        second_tasks = [
            SecondTask(text="★ 他在请人回答问题", is_correct=True),
            SecondTask(text="★ 那位小姐要去8层", is_correct=False),
            SecondTask(text="★ 手表进水了", is_correct=True),
            SecondTask(text="★ ★ 他终于找到那 书了 (есть опечатка)", is_correct=True),
            SecondTask(text="★ 他在住在黄河附 ", is_correct=False),
            SecondTask(text="★ 他边跑步边音乐 ", is_correct=True),
            SecondTask(text="★ 冬鸟会飞到 方 (есть опечатка)", is_correct=False),
            SecondTask(text="★ 他买的东西没送到 ", is_correct=True),
            SecondTask(text="★ 他不认识那个女孩儿 ", is_correct=False),
            SecondTask(text="★ 他最爱吃那儿的面条儿 ", is_correct=False)
        ]

        listening.second_type_tasks = second_tasks

        third1 = ThirdTask()
        tq1 = ThirdTaskQuestion(correct_letter="B")
        tos1 = [
            ThirdTaskOption(letter="A", text="洗盘子"),
            ThirdTaskOption(letter="B", text="搬椅子"),
            ThirdTaskOption(letter="C", text="打扫间")

        ]

        tq1.options = tos1
        third1.questions = [tq1]

        third2 = ThirdTask()
        tq2 = ThirdTaskQuestion(correct_letter="B")
        tos2 = [
            ThirdTaskOption(letter="A", text="师生"),
            ThirdTaskOption(letter="B", text="правильный ответ)"),
            ThirdTaskOption(letter="C", text="妻子和")

        ]

        tq2.options = tos2
        third2.questions = [tq2]

        listening.third_type_tasks = [third1, third2]






        session.add(listening)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
