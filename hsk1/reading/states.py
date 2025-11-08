from aiogram.fsm.state import State, StatesGroup


class HSK1ReadingFirstTask(StatesGroup):
    answer = State()

class HSK1ReadingSecondTask(StatesGroup):
    answer = State()

class HSK1ReadingThirdTask(StatesGroup):
    answer = State()

class HSK1ReadingFourthTask(StatesGroup):
    answer = State()