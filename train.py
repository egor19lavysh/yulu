from database import get_db_session
from hsk3.listening.models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        l = Listening(audio_id="CQACAgIAAxkBAAIC-GiBIC7T-gJ__sO4Mn97GPHQ1EK5AAJEfAACa6QJSPZNA-lFMliwNgQ")

        ft1 = FirstTask(picture_id="AgACAgIAAxkBAAIC9GiBH7zGyhQ_wVevqMmWH3Wwkk9wAAKe9TEba6QJSIQAAcQLuDo_lgEAAwIAA3gAAzYE")

        ft1q = [
            FirstTaskQuestion(correct_letter="C"),
            FirstTaskQuestion(correct_letter="F"),
            FirstTaskQuestion(correct_letter="E"),
            FirstTaskQuestion(correct_letter="A"),
            FirstTaskQuestion(correct_letter="B")
        ]

        ft1.questions = ft1q

        ft2 = FirstTask(
            picture_id="AgACAgIAAxkBAAIC9miBH9UpO02hqF6Ged5C-_c1EP2EAAKf9TEba6QJSLUtNL7E4WSbAQADAgADeAADNgQ")

        ft2q = [
            FirstTaskQuestion(correct_letter="E"),
            FirstTaskQuestion(correct_letter="B"),
            FirstTaskQuestion(correct_letter="A"),
            FirstTaskQuestion(correct_letter="D"),
            FirstTaskQuestion(correct_letter="C")
        ]

        ft2.questions = ft2q

        l.first_type_tasks = [ft1, ft2]

        second_tasks = [
            SecondTask(text="★ 他在请人回答问题。", is_correct=True),  # 11. √
            SecondTask(text="★ 那位小姐要去8层。", is_correct=False),  # 12. ×
            SecondTask(text="★ 手表进水了。", is_correct=True),  # 13. √
            SecondTask(text="★ 他终于找到那本书了。", is_correct=True),  # 14. √
            SecondTask(text="★ 他现在住在黄河附近。", is_correct=False),  # 15. ×
            SecondTask(text="★ 他喜欢边跑步边听音乐。", is_correct=True),  # 16. √
            SecondTask(text="★ 冬天鸟会飞到北方。", is_correct=False),  # 17. ×
            SecondTask(text="★ 他买的东西还没送到。", is_correct=True),  # 18. √
            SecondTask(text="★ 他不认识那个女孩儿。", is_correct=False),  # 19. ×
            SecondTask(text="★ 他最爱吃那儿的面条儿。", is_correct=False)  # 20. ×
        ]

        l.second_type_tasks = second_tasks

        third_task1 = ThirdTask()

        # Добавляем вопросы с вариантами ответов
        third_task1.questions = [
            ThirdTaskQuestion(
                correct_letter="B",
                options=[
                    ThirdTaskOption(letter="A", text="洗盘子"),
                    ThirdTaskOption(letter="B", text="搬椅子"),
                    ThirdTaskOption(letter="C", text="打扫房间")
                ]
            ),  # 21. B
            ThirdTaskQuestion(
                correct_letter="B",
                options=[
                    ThirdTaskOption(letter="A", text="师生"),
                    ThirdTaskOption(letter="B", text="同事"),
                    ThirdTaskOption(letter="C", text="妻子和丈夫")
                ]
            ),  # 22. B
            ThirdTaskQuestion(
                correct_letter="A",
                options=[
                    ThirdTaskOption(letter="A", text="刷牙了"),
                    ThirdTaskOption(letter="B", text="吃得太饱"),
                    ThirdTaskOption(letter="C", text="不吃甜的")
                ]
            ),  # 23. A
            ThirdTaskQuestion(
                correct_letter="A",
                options=[
                    ThirdTaskOption(letter="A", text="嘴"),
                    ThirdTaskOption(letter="B", text="鼻子"),
                    ThirdTaskOption(letter="C", text="耳朵")
                ]
            ),  # 24. A
            ThirdTaskQuestion(
                correct_letter="B",
                options=[
                    ThirdTaskOption(letter="A", text="去运动"),
                    ThirdTaskOption(letter="B", text="还相机"),
                    ThirdTaskOption(letter="C", text="买笔记本")
                ]
            ),  # 25. B
            ThirdTaskQuestion(
                correct_letter="A",
                options=[
                    ThirdTaskOption(letter="A", text="出了新菜"),
                    ThirdTaskOption(letter="B", text="客人不满意"),
                    ThirdTaskOption(letter="C", text="菜单不好懂")
                ]
            ),  # 26. A
            ThirdTaskQuestion(
                correct_letter="C",
                options=[
                    ThirdTaskOption(letter="A", text="睡得早"),
                    ThirdTaskOption(letter="B", text="在写作业"),
                    ThirdTaskOption(letter="C", text="明天有比赛")
                ]
            ),  # 27. C
            ThirdTaskQuestion(
                correct_letter="A",
                options=[
                    ThirdTaskOption(letter="A", text="很好看"),
                    ThirdTaskOption(letter="B", text="很干净"),
                    ThirdTaskOption(letter="C", text="比较少见")
                ]
            ),  # 28. A
            ThirdTaskQuestion(
                correct_letter="B",
                options=[
                    ThirdTaskOption(letter="A", text="叔叔"),
                    ThirdTaskOption(letter="B", text="弟弟"),
                    ThirdTaskOption(letter="C", text="哥哥")
                ]
            ),  # 29. B
            ThirdTaskQuestion(
                correct_letter="C",
                options=[
                    ThirdTaskOption(letter="A", text="宾馆门口"),
                    ThirdTaskOption(letter="B", text="公园北门"),
                    ThirdTaskOption(letter="C", text="学校东门")
                ]
            )  # 30. C
        ]

        fourth_task = ThirdTask()  # Используем ту же модель, что и для третьей части

        # Добавляем вопросы с вариантами ответов
        fourth_task.questions = [
            ThirdTaskQuestion(
                correct_letter="A",
                options=[
                    ThirdTaskOption(letter="A", text="问路"),
                    ThirdTaskOption(letter="B", text="写字"),
                    ThirdTaskOption(letter="C", text="买地图")
                ]
            ),  # 31. A
            ThirdTaskQuestion(
                correct_letter="B",
                options=[
                    ThirdTaskOption(letter="A", text="晴天"),
                    ThirdTaskOption(letter="B", text="阴天"),
                    ThirdTaskOption(letter="C", text="下雪了")
                ]
            ),  # 32. B
            ThirdTaskQuestion(
                correct_letter="C",
                options=[
                    ThirdTaskOption(letter="A", text="节日"),
                    ThirdTaskOption(letter="B", text="朋友的姓"),
                    ThirdTaskOption(letter="C", text="孩子的名字")
                ]
            ),  # 33. C
            ThirdTaskQuestion(
                correct_letter="B",
                options=[
                    ThirdTaskOption(letter="A", text="爱读书"),
                    ThirdTaskOption(letter="B", text="在学画"),
                    ThirdTaskOption(letter="C", text="不太努力")
                ]
            ),  # 34. B
            ThirdTaskQuestion(
                correct_letter="A",
                options=[
                    ThirdTaskOption(letter="A", text="出国了"),
                    ThirdTaskOption(letter="B", text="去办护照了"),
                    ThirdTaskOption(letter="C", text="请假回家了")
                ]
            ),  # 35. A
            ThirdTaskQuestion(
                correct_letter="C",
                options=[
                    ThirdTaskOption(letter="A", text="饿了"),
                    ThirdTaskOption(letter="B", text="行李箱坏了"),
                    ThirdTaskOption(letter="C", text="钱包不见了")
                ]
            ),  # 36. C
            ThirdTaskQuestion(
                correct_letter="C",
                options=[
                    ThirdTaskOption(letter="A", text="是司机"),
                    ThirdTaskOption(letter="B", text="数学差"),
                    ThirdTaskOption(letter="C", text="需要两辆车")
                ]
            ),  # 37. C
            ThirdTaskQuestion(
                correct_letter="C",
                options=[
                    ThirdTaskOption(letter="A", text="没关灯"),
                    ThirdTaskOption(letter="B", text="在找词典"),
                    ThirdTaskOption(letter="C", text="没做完题")
                ]
            ),  # 38. C
            ThirdTaskQuestion(
                correct_letter="A",
                options=[
                    ThirdTaskOption(letter="A", text="新开不久"),
                    ThirdTaskOption(letter="B", text="环境一般"),
                    ThirdTaskOption(letter="C", text="在医院旁边")
                ]
            ),  # 39. A
            ThirdTaskQuestion(
                correct_letter="B",
                options=[
                    ThirdTaskOption(letter="A", text="瘦了"),
                    ThirdTaskOption(letter="B", text="不发烧了"),
                    ThirdTaskOption(letter="C", text="腿还很疼")
                ]
            )  # 40. B
        ]

        l.third_type_tasks = [third_task1, fourth_task]

        session.add(l)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
