from aiogram.fsm.state import State, StatesGroup


class HSK2ReadingFirstTask(StatesGroup):
    answer = State()

class HSK2ReadingSecondTask(StatesGroup):
    answer = State()

class HSK2ReadingThirdTask(StatesGroup):
    answer = State()

class HSK2ReadingFourthTask(StatesGroup):
    answer = State()