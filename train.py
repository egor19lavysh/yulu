from database import get_db_session
from hsk3.reading.models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        r = Reading()

        ft1 = ReadingFirstTask()

        ops1 = [
            ReadingFirstTaskOption(letter="A", text=" 说她很聪明，每考试都是第一 "),
            ReadingFirstTaskOption(letter="B", text=" 跳了两个小时的舞，真累啊！"),
            ReadingFirstTaskOption(letter="C", text="你该多花点儿时间跟儿子在一起，多跟他聊聊儿")
        ]

        q1 = [
            ReadingFirstTaskQuestion(text="姐，你要看的那个电视节目经开始了 ", correct_letter="B"),
            ReadingFirstTaskQuestion(text="．孩子在不愿意跟说话，怎么办？ ", correct_letter="A"),
            ReadingFirstTaskQuestion(text="穿绿裙子的那个小朋真可爱", correct_letter="C"),
        ]

        ft1.options = ops1
        ft1.questions = q1

        ft2 = ReadingFirstTask()

        ops2 = [
            ReadingFirstTaskOption(letter="A", text=" 是昨去商店给妹妹买的生日礼物"),
            ReadingFirstTaskOption(letter="B", text="妈妈，你给讲个故吧？"),
            ReadingFirstTaskOption(letter="C", text=" 大家离得一点儿，个子的学站前面")
        ]

        q2 = [
            ReadingFirstTaskQuestion(text="．准备好了吗？笑一笑， 要开始照了 ", correct_letter="B"),
            ReadingFirstTaskQuestion(text="．．好，但完了就要睡觉啊 ", correct_letter="A"),
            ReadingFirstTaskQuestion(text="．王阿姨每都很 ", correct_letter="C"),
        ]

        ft2.options = ops2
        ft2.questions = q2

        r.first_tasks = [ft1, ft2]

        st1 = ReadingSecondTask()

        ops1 = [
            ReadingSecondTaskOption(letter="A", text=" 是昨去商店给妹妹买的生日礼物"),
            ReadingSecondTaskOption(letter="B", text="妈妈，你给讲个故吧？"),
            ReadingSecondTaskOption(letter="C", text=" 大家离得一点儿，个子的学站前面")
        ]

        q1 = [
            ReadingSecondTaskQuestion(text="．准备好了吗？笑一笑， 要开始照了 ", correct_letter="B"),
            ReadingSecondTaskQuestion(text="．．好，但完了就要睡觉啊 ", correct_letter="A"),
            ReadingSecondTaskQuestion(text="．王阿姨每都很 ", correct_letter="C"),
        ]

        st1.options = ops1
        st1.questions = q1

        st2 = ReadingSecondTask()

        ops2 = [
            ReadingSecondTaskOption(letter="A", text=" 是昨去商店给妹妹买的生日礼物"),
            ReadingSecondTaskOption(letter="B", text="妈妈，你给讲个故吧？"),
            ReadingSecondTaskOption(letter="C", text=" 大家离得一点儿，个子的学站前面")
        ]

        q2 = [
            ReadingSecondTaskQuestion(text="．准备好了吗？笑一笑， 要开始照了 ", correct_letter="B"),
            ReadingSecondTaskQuestion(text="．．好，但完了就要睡觉啊 ", correct_letter="A"),
            ReadingSecondTaskQuestion(text="．王阿姨每都很 ", correct_letter="C"),
        ]

        st2.options = ops2
        st2.questions = q2

        r.second_tasks = [st1, st2]


        tt1 = ReadingThirdTask(text="：您是来参今 会议的吗？您来早了一点儿，在才8点半 您先进来\n吧\n ★ 会议最可能几点开始？", correct_letter="B")
        ops1 = [
            ReadingThirdTaskOption(letter="A", text="8点"),
            ReadingThirdTaskOption(letter="B", text="8点半"),
            ReadingThirdTaskOption(letter="C", text="9点"),
        ]

        tt1.options = ops1

        r.third_tasks = [tt1]

        session.add(r)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
