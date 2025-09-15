from database import get_db_session
from hsk4.reading.models import *


def create_sample_task():
    session = next(get_db_session())

    try:
        reading_var = ReadingHSK4()

        # Первое задание (46-50)
        first_task1 = ReadingFirstTaskHSK4()

        # Опции для первого задания
        options1 = [
            ReadingFirstTaskOptionHSK4(letter="A", text="随着", task=first_task1),
            ReadingFirstTaskOptionHSK4(letter="B", text="尝", task=first_task1),
            ReadingFirstTaskOptionHSK4(letter="C", text="春节", task=first_task1),
            ReadingFirstTaskOptionHSK4(letter="D", text="坚持", task=first_task1),
            ReadingFirstTaskOptionHSK4(letter="E", text="收拾", task=first_task1),
            ReadingFirstTaskOptionHSK4(letter="F", text="提醒", task=first_task1)
        ]

        # Предложения для первого задания
        sentences1 = [
            ReadingFirstTaskSentenceHSK4(text="虽然现在离（ ）还有段时间，但是不少人已经开始准备过年的东西了。",
                                         correct_letter="C", task=first_task1),
            ReadingFirstTaskSentenceHSK4(text="研究证明，人们的心情会（ ）天气的变化而变化。", correct_letter="A",
                                         task=first_task1),
            ReadingFirstTaskSentenceHSK4(text="明天可能下雨，你记得（ ）儿子带雨伞。", correct_letter="F",
                                         task=first_task1),
            ReadingFirstTaskSentenceHSK4(text="这是你做的饺子？真香！我先（ ）一个。", correct_letter="B", task=first_task1),
            ReadingFirstTaskSentenceHSK4(text="快把房间（ ）一下，准备一些水果，一会儿有客人要来。", correct_letter="E",
                                         task=first_task1)
        ]

        first_task1.options = options1
        first_task1.sentences = sentences1
        # Второе задание (51-55)
        first_task2 = ReadingFirstTaskHSK4()

        # Опции для второго задания
        options2 = [
            ReadingFirstTaskOptionHSK4(letter="A", text="反映", task=first_task2),
            ReadingFirstTaskOptionHSK4(letter="B", text="陪", task=first_task2),
            ReadingFirstTaskOptionHSK4(letter="C", text="温度", task=first_task2),
            ReadingFirstTaskOptionHSK4(letter="D", text="堵车", task=first_task2),
            ReadingFirstTaskOptionHSK4(letter="E", text="来得及", task=first_task2),
            ReadingFirstTaskOptionHSK4(letter="F", text="肯定", task=first_task2)
        ]

        # Предложения для второго задания
        sentences2 = [
            ReadingFirstTaskSentenceHSK4(text="A：这些瓶子的数量对吧？\nB：我都仔细检查过了，（ ）没问题。",
                                         correct_letter="F", task=first_task2),
            ReadingFirstTaskSentenceHSK4(
                text="A：讨论会开得顺利吗？\nB：顺利，大家（ ）了不少管理过程中出现的问题，对下一步工作很有帮助。",
                correct_letter="A", task=first_task2),
            ReadingFirstTaskSentenceHSK4(
                text="A：火车快开了，他怎么还没来？\nB：他一般很准时的，可能是路上（ ），别着急，再等等。", correct_letter="D",
                task=first_task2),
            ReadingFirstTaskSentenceHSK4(text="A：快点儿，今天千万不能迟到。\nB：还有10分钟呢，（ ）", correct_letter="E",
                                         task=first_task2),
            ReadingFirstTaskSentenceHSK4(text="A：我（ ）你一起去吧，可以顺便活动活动。\nB：太好了，我们现在就出发。",
                                         correct_letter="B", task=first_task2)
        ]

        first_task2.options = options2
        first_task2.sentences = sentences2

        reading_var.first_type_tasks = [first_task1, first_task2]

        ### 2

        second_tasks = []

        # Задание 56
        task_56 = ReadingSecondTaskHSK4(
            correct_sequence="CAB"
        )
        options_56 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="她就给我留下了极深的印象", task=task_56),
            ReadingSecondTaskOptionHSK4(letter="B", text="那就是她特别热情、特别友好", task=task_56),
            ReadingSecondTaskOptionHSK4(letter="C", text="第一次和王小姐见面", task=task_56)
        ]
        task_56.options = options_56

        second_tasks.append(task_56)

        # Задание 57
        task_57 = ReadingSecondTaskHSK4(
            correct_sequence="ACB"
        )
        options_57 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="茶不仅仅是一种饮料", task=task_57),
            ReadingSecondTaskOptionHSK4(letter="B", text="它在中国有着几千年的历史", task=task_57),
            ReadingSecondTaskOptionHSK4(letter="C", text="而且还是一种文化", task=task_57)
        ]
        task_57.options = options_57

        second_tasks.append(task_57)

        # Задание 58
        task_58 = ReadingSecondTaskHSK4(
            correct_sequence="ACB"
        )
        options_58 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="昨天我和同事去逛街", task=task_58),
            ReadingSecondTaskOptionHSK4(letter="B", text="可惜没有我穿的号了", task=task_58),
            ReadingSecondTaskOptionHSK4(letter="C", text="我看上了一双挺漂亮的鞋，还打折", task=task_58)
        ]
        task_58.options = options_58

        second_tasks.append(task_58)

        # Задание 59
        task_59 = ReadingSecondTaskHSK4(
            correct_sequence="BAC"
        )
        options_59 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="所以你喜欢哪种颜色", task=task_59),
            ReadingSecondTaskOptionHSK4(letter="B", text="因为不同的颜色表示不同的性格", task=task_59),
            ReadingSecondTaskOptionHSK4(letter="C", text="就说明你是哪种性格的人", task=task_59)
        ]
        task_59.options = options_59

        second_tasks.append(task_59)

        # Задание 60
        task_60 = ReadingSecondTaskHSK4(
            correct_sequence="ABC"
        )
        options_60 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="因为工作的需要", task=task_60),
            ReadingSecondTaskOptionHSK4(letter="B", text="所以我去过那里几次", task=task_60),
            ReadingSecondTaskOptionHSK4(letter="C", text="对当地的文化有一些简单的了解", task=task_60)
        ]
        task_60.options = options_60

        second_tasks.append(task_60)

        # Задание 61
        task_61 = ReadingSecondTaskHSK4(
            correct_sequence="BCA"
        )
        options_61 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="被大家普遍使用的是汉语普通话", task=task_61),
            ReadingSecondTaskOptionHSK4(letter="B", text="中国是一个多民族的国家", task=task_61),
            ReadingSecondTaskOptionHSK4(letter="C", text="很多民族都有自己的语言", task=task_61)
        ]
        task_61.options = options_61

        second_tasks.append(task_61)

        # Задание 62
        task_62 = ReadingSecondTaskHSK4(
            correct_sequence="BAC"
        )
        options_62 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="还是从材料的质量上看", task=task_62),
            ReadingSecondTaskOptionHSK4(letter="B", text="无论从价格方面看", task=task_62),
            ReadingSecondTaskOptionHSK4(letter="C", text="这种盒子都是值得考虑的", task=task_62)
        ]
        task_62.options = options_62

        second_tasks.append(task_62)

        # Задание 63
        task_63 = ReadingSecondTaskHSK4(
            correct_sequence="ACB"
        )
        options_63 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="这种鱼生活在深海中", task=task_63),
            ReadingSecondTaskOptionHSK4(letter="B", text="看起来像一个个会游泳的小电灯", task=task_63),
            ReadingSecondTaskOptionHSK4(letter="C", text="它们的身体能发出美丽的亮光", task=task_63)
        ]
        task_63.options = options_63

        second_tasks.append(task_63)

        # Задание 64
        task_64 = ReadingSecondTaskHSK4(
            correct_sequence="BAC"
        )
        options_64 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="是父母的鼓励给了她信心", task=task_64),
            ReadingSecondTaskOptionHSK4(letter="B", text="其实她小时候很普通", task=task_64),
            ReadingSecondTaskOptionHSK4(letter="C", text="让她后来终于成为一位优秀的演员", task=task_64)
        ]
        task_64.options = options_64

        second_tasks.append(task_64)

        # Задание 65
        task_65 = ReadingSecondTaskHSK4(
            correct_sequence="CBA"
        )
        options_65 = [
            ReadingSecondTaskOptionHSK4(letter="A", text="我们还是经常打电话联系", task=task_65),
            ReadingSecondTaskOptionHSK4(letter="B", text="尽管已经毕业那么多年", task=task_65),
            ReadingSecondTaskOptionHSK4(letter="C", text="他是我大学时最好的同学", task=task_65)
        ]
        task_65.options = options_65

        second_tasks.append(task_65)

        # Добавляем все задания второго типа в reading_var
        reading_var.second_type_tasks = second_tasks

        ### 3

        # Третий тип заданий (66-85)
        third_tasks = []

        # Задание 66
        task_66 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="小时候弟弟比我矮，现在却超过我了，看着他一米八二的个子，我真是羡慕极了。"
        )
        questions_66 = [
            ReadingThirdTaskQuestionHSK4(
                text="根据这句话，可以知道现在：",
                correct_letter="B",
                task=task_66,
                options=[
                    QuestionOptionHSK4(letter="A", text="我一米八"),
                    QuestionOptionHSK4(letter="B", text="我比弟弟矮"),
                    QuestionOptionHSK4(letter="C", text="弟弟个子矮"),
                    QuestionOptionHSK4(letter="D", text="我同情弟弟")
                ]
            )
        ]

        third_tasks.append(task_66)

        # Задание 67
        task_67 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="我是前天到北京的，想借这次机会去长城看看，可是公司的事情很多，时间安排得很紧张。"
        )
        questions_67 = [
            ReadingThirdTaskQuestionHSK4(
                text="我最可能来北京：",
                correct_letter="C",
                task=task_67,
                options=[
                    QuestionOptionHSK4(letter="A", text="旅游"),
                    QuestionOptionHSK4(letter="B", text="休息"),
                    QuestionOptionHSK4(letter="C", text="出差"),
                    QuestionOptionHSK4(letter="D", text="请假")
                ]
            )
        ]

        third_tasks.append(task_67)

        # Задание 68
        task_68 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="地球是我们共同的家，保护环境就是保护我们自己，为减少污染，我们应该养成节约的习惯，节约用水、节约用纸等等。"
        )
        questions_68 = [
            ReadingThirdTaskQuestionHSK4(
                text="节约用纸主要是为了：",
                correct_letter="A",
                task=task_68,
                options=[
                    QuestionOptionHSK4(letter="A", text="保护环境"),
                    QuestionOptionHSK4(letter="B", text="限制用水"),
                    QuestionOptionHSK4(letter="C", text="改变地球"),
                    QuestionOptionHSK4(letter="D", text="发展经济")
                ]
            )
        ]

        third_tasks.append(task_68)

        # Задание 69
        task_69 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="一些电影院拒绝观众带任何食品、饮料，人们不得不买电影院卖的东西。很多观众批评这个做法，因为电影院的东西特别贵，大约比超市贵三倍。"
        )
        questions_69 = [
            ReadingThirdTaskQuestionHSK4(
                text="观众对什么不满意？",
                correct_letter="C",
                task=task_69,
                options=[
                    QuestionOptionHSK4(letter="A", text="票价高"),
                    QuestionOptionHSK4(letter="B", text="座位少"),
                    QuestionOptionHSK4(letter="C", text="东西太贵"),
                    QuestionOptionHSK4(letter="D", text="电影不精彩")
                ]
            )
        ]

        third_tasks.append(task_69)

        # Задание 70
        task_70 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="进入21世纪，随着科学技术的发展，人与人的联系越来越方便，上网发电子邮件的人越来越多，写信的人越来越少。"
        )
        questions_70 = [
            ReadingThirdTaskQuestionHSK4(
                text="根据这段话，人们更喜欢怎么交流？",
                correct_letter="D",
                task=task_70,
                options=[
                    QuestionOptionHSK4(letter="A", text="寄信"),
                    QuestionOptionHSK4(letter="B", text="谈话"),
                    QuestionOptionHSK4(letter="C", text="打电话"),
                    QuestionOptionHSK4(letter="D", text="写电子邮件")
                ]
            )
        ]

        third_tasks.append(task_70)

        # Задание 71
        task_71 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="长江是中国也是亚洲最长的河，全长6397公里，它由西向东，流经十几个省市，最后由上海市流入东海。"
        )
        questions_71 = [
            ReadingThirdTaskQuestionHSK4(
                text="长江：",
                correct_letter="C",
                task=task_71,
                options=[
                    QuestionOptionHSK4(letter="A", text="世界最长"),
                    QuestionOptionHSK4(letter="B", text="是黄色的"),
                    QuestionOptionHSK4(letter="C", text="流向东部"),
                    QuestionOptionHSK4(letter="D", text="近1万公里")
                ]
            )
        ]

        third_tasks.append(task_71)

        # Задание 72
        task_72 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="兴趣是最好的老师，如果孩子对一件事情感兴趣，那他一定会主动、努力地去学习，效果也会更好。"
        )
        questions_72 = [
            ReadingThirdTaskQuestionHSK4(
                text="为了提高学习效果，应该让孩子：",
                correct_letter="C",
                task=task_72,
                options=[
                    QuestionOptionHSK4(letter="A", text="积累经验"),
                    QuestionOptionHSK4(letter="B", text="努力学习"),
                    QuestionOptionHSK4(letter="C", text="产生兴趣"),
                    QuestionOptionHSK4(letter="D", text="相信自己")
                ]
            )
        ]

        third_tasks.append(task_72)

        # Задание 73
        task_73 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="有的时候，我们要学会拒绝别人。拒绝别人，要找到合适、礼貌的方法，否则，如果表达不合适，就会引起误会。"
        )
        questions_73 = [
            ReadingThirdTaskQuestionHSK4(
                text="这段话主要说怎样：",
                correct_letter="A",
                task=task_73,
                options=[
                    QuestionOptionHSK4(letter="A", text="拒绝别人"),
                    QuestionOptionHSK4(letter="B", text="获得尊重"),
                    QuestionOptionHSK4(letter="C", text="减少误会"),
                    QuestionOptionHSK4(letter="D", text="获得原谅")
                ]
            )
        ]

        third_tasks.append(task_73)

        # Задание 74
        task_74 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="以前，日记是写给自己看的，然而现在更多的年轻人喜欢把自己的日记放到网站上，希望和更多的人交流。"
        )
        questions_74 = [
            ReadingThirdTaskQuestionHSK4(
                text="现在许多年轻人写日记：",
                correct_letter="D",
                task=task_74,
                options=[
                    QuestionOptionHSK4(letter="A", text="写得很短"),
                    QuestionOptionHSK4(letter="B", text="代替交流"),
                    QuestionOptionHSK4(letter="C", text="只在网上写"),
                    QuestionOptionHSK4(letter="D", text="允许别人看")
                ]
            )
        ]

        third_tasks.append(task_74)

        # Задание 75
        task_75 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="一个不喜欢开玩笑的人，不一定让人讨厌。但是一个会开玩笑的人，往往让人觉得很可爱。"
        )
        questions_75 = [
            ReadingThirdTaskQuestionHSK4(
                text="会开玩笑的人：",
                correct_letter="C",
                task=task_75,
                options=[
                    QuestionOptionHSK4(letter="A", text="更聪明"),
                    QuestionOptionHSK4(letter="B", text="很成熟"),
                    QuestionOptionHSK4(letter="C", text="让人喜欢"),
                    QuestionOptionHSK4(letter="D", text="比较无聊")
                ]
            )
        ]

        third_tasks.append(task_75)

        # Задание 76
        task_76 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="怎样才能说一口流利的外语呢？如果你有一定的语言基础和经济条件，那么出国是最好的选择。因为语言环境对学习语言有重要的作用。"
        )
        questions_76 = [
            ReadingThirdTaskQuestionHSK4(
                text="去国外学习外语是因为：",
                correct_letter="A",
                task=task_76,
                options=[
                    QuestionOptionHSK4(letter="A", text="语言环境好"),
                    QuestionOptionHSK4(letter="B", text="经济条件好"),
                    QuestionOptionHSK4(letter="C", text="有语言基础"),
                    QuestionOptionHSK4(letter="D", text="学习更认真")
                ]
            )
        ]

        third_tasks.append(task_76)

        # Задание 77
        task_77 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="「生日快乐！」「祝爸爸生日快乐！」晚上我刚回到家，妻子和儿子就一起祝我生日快乐，并送给我生日礼物。这时我才明白过来，今天是我的生日。"
        )
        questions_77 = [
            ReadingThirdTaskQuestionHSK4(
                text="根据这段话，可以知道我：",
                correct_letter="D",
                task=task_77,
                options=[
                    QuestionOptionHSK4(letter="A", text="加班了"),
                    QuestionOptionHSK4(letter="B", text="身体不舒服"),
                    QuestionOptionHSK4(letter="C", text="没按时回家"),
                    QuestionOptionHSK4(letter="D", text="忘记了生日")
                ]
            )
        ]

        third_tasks.append(task_77)

        # Задание 78
        task_78 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="我对现在的这份工作还比较满意。首先，我学的就是这个专业：其次，同事们都很喜欢我；另外，工资也还算可以，还有奖金，收入不错。"
        )
        questions_78 = [
            ReadingThirdTaskQuestionHSK4(
                text="根据这段话，可以知道我：",
                correct_letter="B",
                task=task_78,
                options=[
                    QuestionOptionHSK4(letter="A", text="工作累"),
                    QuestionOptionHSK4(letter="B", text="受欢迎"),
                    QuestionOptionHSK4(letter="C", text="奖金很少"),
                    QuestionOptionHSK4(letter="D", text="收入很低")
                ]
            )
        ]

        third_tasks.append(task_78)

        # Задание 79
        task_79 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="交通工具是现代生活中不可缺少的一部分。常见的交通工具包括汽车、飞机、船等，这一切拉近了人与人之间的距离，并且扩大了人们的活动范围。"
        )
        questions_79 = [
            ReadingThirdTaskQuestionHSK4(
                text="这段话主要谈：",
                correct_letter="B",
                task=task_79,
                options=[
                    QuestionOptionHSK4(letter="A", text="生活经历"),
                    QuestionOptionHSK4(letter="B", text="交通工具"),
                    QuestionOptionHSK4(letter="C", text="社会责任"),
                    QuestionOptionHSK4(letter="D", text="夫妻感情")
                ]
            )
        ]

        third_tasks.append(task_79)

        # Задание 80-81 (общий текст)
        task_80_81 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="森林里，动物们决定举办一个晚会，这次演出吸引了几乎所有的动物。他们都很积极，准备的节目各有特点，小鸟要给大家唱歌，老虎要跳舞，小猫要画画儿，猴子要讲故事，狮子说他给大家照相，熊猫说：「我不会表演，但是我可以当观众，为大家鼓掌。」最后只剩下小牛了，她想了好久，忽然得意地说：「我负责为大家送免费的牛奶！」"
        )
        questions_80_81 = [
            ReadingThirdTaskQuestionHSK4(
                text="谁打算为大家讲故事？",
                correct_letter="C",
                task=task_80_81,
                options=[
                    QuestionOptionHSK4(letter="A", text="狗"),
                    QuestionOptionHSK4(letter="B", text="马"),
                    QuestionOptionHSK4(letter="C", text="猴子"),
                    QuestionOptionHSK4(letter="D", text="小猪")
                ]
            ),
            ReadingThirdTaskQuestionHSK4(
                text="小牛负责为大家：",
                correct_letter="B",
                task=task_80_81,
                options=[
                    QuestionOptionHSK4(letter="A", text="报名"),
                    QuestionOptionHSK4(letter="B", text="送牛奶"),
                    QuestionOptionHSK4(letter="C", text="填写地址"),
                    QuestionOptionHSK4(letter="D", text="做巧克力")
                ]
            )
        ]
        third_tasks.append(task_80_81)

        # Задание 82-83 (общий текст)
        task_82_83 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="什么是真正的朋友？不同的人会有不同的理解，而我的理解是：在你遇到困难的时候，朋友会勇敢地站出来，及时给你帮助；在你孤单或者伤心流泪的时候，朋友会陪在你身边，想办法让你感到幸福；无论你是穷人还是富人，真正的朋友永远值得你信任。"
        )
        questions_82_83 = [
            ReadingThirdTaskQuestionHSK4(
                text="根据这段话，朋友可以帮你：",
                correct_letter="D",
                task=task_82_83,
                options=[
                    QuestionOptionHSK4(letter="A", text="总结经验"),
                    QuestionOptionHSK4(letter="B", text="照顾家人"),
                    QuestionOptionHSK4(letter="C", text="远离危险"),
                    QuestionOptionHSK4(letter="D", text="解决难题")
                ]
            ),
            ReadingThirdTaskQuestionHSK4(
                text="这段话主要介绍的是：",
                correct_letter="D",
                task=task_82_83,
                options=[
                    QuestionOptionHSK4(letter="A", text="精神"),
                    QuestionOptionHSK4(letter="B", text="爱情"),
                    QuestionOptionHSK4(letter="C", text="态度"),
                    QuestionOptionHSK4(letter="D", text="友谊")
                ]
            )
        ]
        third_tasks.append(task_82_83)

        # Задание 84-85 (общий текст)
        task_84_85 = ReadingThirdTaskHSK4(
            reading_var=reading_var,
            text="南半球和北半球的季节正好相反。当北半球到处春暖花开的时候，南半球已经进入凉快的秋天，树叶也开始慢慢地变黄了；当北半球的气温逐渐降低的时候，南半球的天气却开始热起来，人们已经脱掉了厚厚的大衣。"
        )
        questions_84_85 = [
            ReadingThirdTaskQuestionHSK4(
                text="南半球是秋天的时候，北半球是：",
                correct_letter="A",
                task=task_84_85,
                options=[
                    QuestionOptionHSK4(letter="A", text="春天"),
                    QuestionOptionHSK4(letter="B", text="夏天"),
                    QuestionOptionHSK4(letter="C", text="秋天"),
                    QuestionOptionHSK4(letter="D", text="冬天")
                ]
            ),
            ReadingThirdTaskQuestionHSK4(
                text="关于南北半球，可以知道：",
                correct_letter="A",
                task=task_84_85,
                options=[
                    QuestionOptionHSK4(letter="A", text="季节不同"),
                    QuestionOptionHSK4(letter="B", text="南半球更热"),
                    QuestionOptionHSK4(letter="C", text="北半球植物多"),
                    QuestionOptionHSK4(letter="D", text="秋天都很干燥")
                ]
            )
        ]
        third_tasks.append(task_84_85)

        # Добавляем все задания третьего типа в reading_var
        reading_var.third_type_tasks = third_tasks

        session.add(reading_var)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
    finally:
        session.close()


create_sample_task()
