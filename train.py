from database import get_db_session
from hsk4.writing.models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        writing_hsk4 = WritingHSK4()

        # Парсим задания первого типа (86-95)
        first_tasks_data = [
            {
                "words": "音乐 喜欢 流行 他 听",
                "correct_sentence": "他喜欢听流行音乐。"
            },
            {
                "words": "有效 这种药 对 头疼 很",
                "correct_sentence": "这种药对头疼很有效。"
            },
            {
                "words": "更 南方 的 湿润 气候",
                "correct_sentence": "南方的气候更湿润。"
            },
            {
                "words": "自己的 每个人 优点和缺点 都 有",
                "correct_sentence": "每个人都有自己的优点和缺点。"
            },
            {
                "words": "公司 机会 提供了 一些 学习的",
                "correct_sentence": "公司提供了一些学习的机会。"
            },
            {
                "words": "看懂 能 他 中文 说明书",
                "correct_sentence": "他能看懂中文说明书。"
            },
            {
                "words": "菜 的 怎么样 这个 味道",
                "correct_sentence": "这个菜的味道怎么样？"
            },
            {
                "words": "内容 那本杂志 的 十分 丰富",
                "correct_sentence": "那本杂志的内容十分丰富。"
            },
            {
                "words": "区别 发现 你 这两张照片的 吗 了",
                "correct_sentence": "你发现这两张照片的区别了吗？"
            },
            {
                "words": "符合 太 他的看法 不 实际",
                "correct_sentence": "他的看法不太符合实际。"
            }
        ]

        first_tasks = []
        for task_data in first_tasks_data:
            first_task = WritingFirstTaskHSK4(
                words=task_data["words"],
                correct_sentence=task_data["correct_sentence"]
            )
            first_tasks.append(first_task)

        writing_hsk4.first_type_tasks = first_tasks

        session.add(writing_hsk4)
        session.commit()


        second_task = WritingSecondTaskHSK4(
            writing_var_id=writing_hsk4.id,
            picture_id="AgACAgIAAxkBAAIM1GjK_nzafH5AkYmSn4ZkR2nXYa0zAAKtJTIbxytYSh7p0ViLS0ejAQADAgADeAADNgQ"
        )

        words = [
            WritingSecondTaskWord(
                text="试",
                possible_answer="你要不要试试这条裙子？"
            ),
            WritingSecondTaskWord(
                text="答案",
                possible_answer="他不知道答案是什么。"
            ),
            WritingSecondTaskWord(
                text="风景",
                possible_answer="这儿的风景真漂亮。"
            ),
            WritingSecondTaskWord(
                text="醒",
                possible_answer="她还没睡醒吗？"
            ),
            WritingSecondTaskWord(
                text="脏",
                possible_answer="她把脸弄脏了。"
            ),
        ]

        second_task.words = words



        session.add(second_task)
        session.commit()

        # session.add(reading_var)
        # session.commit()

    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
