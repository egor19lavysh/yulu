from database import get_db_session
from hsk3.writing.models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        w = Writing()

        first = [
            WritingFirstTask(chars="特别  力  他学", correct_answer="他学习特别努力"),
            WritingFirstTask(chars="你    面包    想    吃哪种", correct_answer="你想吃哪种面包？"),
            WritingFirstTask(chars="你的脸    净    没   洗", correct_answer='你的脸还没洗干净'),
            WritingFirstTask(chars="他的绩    最好的    一直    是们班 ", correct_answer="他的៤绩一直是៥们班最好的Ǆ"),
            WritingFirstTask(chars="老人    那位    107岁    经    了", correct_answer="那位老人已经 107 岁了"),
        ]

        w.first_tasks = first

        second = [
            WritingSecondTask(text=" 个季 (jié) 的西瓜最好吃了", correct_answer=""),
            WritingSecondTask(text="奶奶，是不是    山了，(yuè) 亮就出来了？", correct_answer=""),
            WritingSecondTask(text=" 是 (zhǎo) 您的6角5分钱，迎再来！", correct_answer=""),
            WritingSecondTask(text="快看，那 (zhī) 大熊猫爬到树去了", correct_answer=""),
            WritingSecondTask(text="．做选择时，最要的是知道 (zì) 想要什么.", correct_answer=""),
        ]

        w.second_tasks = second

        session.add(w)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
