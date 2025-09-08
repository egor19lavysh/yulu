from database import get_db_session
from hsk4.listening.models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        listening_task = ListeningHSK4(
            audio_id="CQACAgIAAxkBAAIKdWi_ItjPWsP6uZbUiLsjy05vj8U2AALXfgAChEH4SUgbFQt-VlN3NgQ"
        )

        ### 1 part

        # Создаем задачи первого типа (1-10)
        first_tasks = [
            FirstTaskHSK4(text="飞机还没起飞。", is_correct=True),  # 1.√
            FirstTaskHSK4(text="不饿就不要吃早饭。", is_correct=False),  # 2.X
            FirstTaskHSK4(text="经理发现了小王的一些缺点。", is_correct=False),  # 3.X
            FirstTaskHSK4(text="女朋友听过这个笑话。", is_correct=True),  # 4.√
            FirstTaskHSK4(text="他没有翻译第二部分。", is_correct=False),  # 5.X
            FirstTaskHSK4(text="服务员的京剧唱得很好。", is_correct=True),  # 6.√
            FirstTaskHSK4(text="王老师现在是教授了。", is_correct=True),  # 7.√
            FirstTaskHSK4(text="他想买个大房子。", is_correct=False),  # 8.X
            FirstTaskHSK4(text="他在理发店。", is_correct=True),  # 9.√
            FirstTaskHSK4(text="这个咖啡馆儿很热闹。", is_correct=False)  # 10.X
        ]

        # Добавляем задачи первого типа
        listening_task.first_type_tasks = first_tasks

        ### 2 part

        second_tasks_data = [
            # Задача 11 - A没纸了
            {
                "correct": "A",
                "options": {
                    "A": "没纸了",
                    "B": "男的没发",
                    "C": "打印机坏了",
                    "D": "传真机坏了"
                }
            },
            # Задача 12 - C小说
            {
                "correct": "C",
                "options": {
                    "A": "将来",
                    "B": "理想",
                    "C": "小说",
                    "D": "职业"
                }
            },
            # Задача 13 - C打网球
            {
                "correct": "C",
                "options": {
                    "A": "办签证",
                    "B": "去学校",
                    "C": "打网球",
                    "D": "打羽毛球"
                }
            },
            # Задача 14 - B换个箱子
            {
                "correct": "B",
                "options": {
                    "A": "不想出国",
                    "B": "换个箱子",
                    "C": "不符合规定",
                    "D": "早点儿回来"
                }
            },
            # Задача 15 - C正在减肥
            {
                "correct": "C",
                "options": {
                    "A": "变胖了",
                    "B": "很难受",
                    "C": "正在减肥",
                    "D": "工作很辛苦"
                }
            },
            # Задача 16 - D在准备考试
            {
                "correct": "D",
                "options": {
                    "A": "是研究生",
                    "B": "参加工作了",
                    "C": "已经毕业了",
                    "D": "在准备考试"
                }
            },
            # Задача 17 - C爬山
            {
                "correct": "C",
                "options": {
                    "A": "打扫",
                    "B": "等人",
                    "C": "爬山",
                    "D": "购物"
                }
            },
            # Задача 18 - A幽默
            {
                "correct": "A",
                "options": {
                    "A": "幽默",
                    "B": "很难过",
                    "C": "很粗心",
                    "D": "没有耐心"
                }
            },
            # Задача 19 - C很咸
            {
                "correct": "C",
                "options": {
                    "A": "很酸",
                    "B": "很甜",
                    "C": "很咸",
                    "D": "很辣"
                }
            },
            # Задача 20 - A他们输了
            {
                "correct": "A",
                "options": {
                    "A": "他们输了",
                    "B": "他们赢了",
                    "C": "他们放弃了",
                    "D": "他们很愉快"
                }
            },
            # Задача 21 - B去旅游
            {
                "correct": "B",
                "options": {
                    "A": "学钢琴",
                    "B": "去旅游",
                    "C": "做生意",
                    "D": "锻炼身体"
                }
            },
            # Задача 22 - B感冒了
            {
                "correct": "B",
                "options": {
                    "A": "肚子疼",
                    "B": "感冒了",
                    "C": "觉得热",
                    "D": "穿得太少"
                }
            },
            # Задача 23 - A周末
            {
                "correct": "A",
                "options": {
                    "A": "周末",
                    "B": "下周",
                    "C": "两周后",
                    "D": "下个月"
                }
            },
            # Задача 24 - C卖家具的
            {
                "correct": "C",
                "options": {
                    "A": "医生",
                    "B": "导游",
                    "C": "卖家具的",
                    "D": "开出租车的"
                }
            },
            # Задача 25 - B马上来
            {
                "correct": "B",
                "options": {
                    "A": "我不会",
                    "B": "马上来",
                    "C": "没法解释",
                    "D": "解决不了"
                }
            }
        ]

        second_tasks = []
        for i, task_data in enumerate(second_tasks_data, 11):
            task = SecondTaskHSK4(
                correct_letter=task_data["correct"],
            )

            options = []
            for letter, text in task_data["options"].items():
                options.append(SecondTaskHSK4Option(
                    letter=letter,
                    text=text
                ))

            task.options = options
            second_tasks.append(task)

        listening_task.second_type_tasks = second_tasks

        ### 3 part

        third_tasks_data = [
            # Задача 26 - A医院
            {
                "correct": "A",
                "options": {
                    "A": "医院",
                    "B": "宾馆",
                    "C": "图书馆",
                    "D": "体育场"
                }
            },
            # Задача 27 - D很正式
            {
                "correct": "D",
                "options": {
                    "A": "很奇怪",
                    "B": "很随便",
                    "C": "很一般",
                    "D": "很正式"
                }
            },
            # Задача 28 - D女的很小心
            {
                "correct": "D",
                "options": {
                    "A": "撞车了",
                    "B": "车速太慢",
                    "C": "他们是记者",
                    "D": "女的很小心"
                }
            },
            # Задача 29 - C忘了密码
            {
                "correct": "C",
                "options": {
                    "A": "生病了",
                    "B": "丢了电脑",
                    "C": "忘了密码",
                    "D": "弄坏镜子了"
                }
            },
            # Задача 30 - C明天
            {
                "correct": "C",
                "options": {
                    "A": "5点",
                    "B": "下班以后",
                    "C": "明天",
                    "D": "下个星期"
                }
            },
            # Задача 31 - B3元5角
            {
                "correct": "B",
                "options": {
                    "A": "两元",
                    "B": "3元5角",
                    "C": "7元",
                    "D": "9元"
                }
            },
            # Задача 32 - D找李大夫
            {
                "correct": "D",
                "options": {
                    "A": "买手机",
                    "B": "去亲戚家",
                    "C": "交电话费",
                    "D": "找李大夫"
                }
            },
            # Задача 33 - C钥匙
            {
                "correct": "C",
                "options": {
                    "A": "毛巾",
                    "B": "帽子",
                    "C": "钥匙",
                    "D": "笔记本"
                }
            },
            # Задача 34 - A车上
            {
                "correct": "A",
                "options": {
                    "A": "车上",
                    "B": "火车站",
                    "C": "电梯里",
                    "D": "地铁上"
                }
            },
            # Задача 35 - B商店
            {
                "correct": "B",
                "options": {
                    "A": "公园",
                    "B": "商店",
                    "C": "洗手间",
                    "D": "公共汽车"
                }
            },
            # Задача 36 - B散散步
            {
                "correct": "B",
                "options": {
                    "A": "睡觉",
                    "B": "散散步",
                    "C": "洗个澡",
                    "D": "回忆过去"
                }
            },
            # Задача 37 - D怎样改变心情
            {
                "correct": "D",
                "options": {
                    "A": "要互相关心",
                    "B": "做事要冷静",
                    "C": "运动很重要",
                    "D": "怎样改变心情"
                }
            },
            # Задача 38 - D工作压力大
            {
                "correct": "D",
                "options": {
                    "A": "脾气好",
                    "B": "爱做梦",
                    "C": "很成功",
                    "D": "工作压力大"
                }
            },
            # Задача 39 - B抽烟
            {
                "correct": "B",
                "options": {
                    "A": "喝酒",
                    "B": "抽烟",
                    "C": "踢足球",
                    "D": "说假话"
                }
            },
            # Задача 40 - D家长
            {
                "correct": "D",
                "options": {
                    "A": "警察",
                    "B": "司机",
                    "C": "学生",
                    "D": "家长"
                }
            },
            # Задача 41 - A变宽了
            {
                "correct": "A",
                "options": {
                    "A": "变宽了",
                    "B": "比较窄",
                    "C": "禁止停车",
                    "D": "没有红绿灯"
                }
            },
            # Задача 42 - D激动
            {
                "correct": "D",
                "options": {
                    "A": "失望",
                    "B": "羡慕",
                    "C": "后悔",
                    "D": "激动"
                }
            },
            # Задача 43 - B结婚了
            {
                "correct": "B",
                "options": {
                    "A": "是演员",
                    "B": "结婚了",
                    "C": "很年轻",
                    "D": "没有得奖"
                }
            },
            # Задача 44 - D会议室
            {
                "correct": "D",
                "options": {
                    "A": "家里",
                    "B": "厨房",
                    "C": "教室",
                    "D": "会议室"
                }
            },
            # Задача 45 - A开会
            {
                "correct": "A",
                "options": {
                    "A": "开会",
                    "B": "参观",
                    "C": "听广播",
                    "D": "看电视"
                }
            }
        ]

        third_tasks = []
        for i, task_data in enumerate(third_tasks_data, 26):
            task = ThirdTaskHSK4(
                correct_letter=task_data["correct"],
            )

            options = []
            for letter, text in task_data["options"].items():
                options.append(ThirdTaskHSK4Option(
                    letter=letter,
                    text=text
                ))

            task.options = options
            third_tasks.append(task)

        listening_task.third_type_tasks = third_tasks

        session.add(listening_task)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
