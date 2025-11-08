from aiogram.fsm.state import State, StatesGroup


class HSK4ReadingFirstTask(StatesGroup):
    answer = State()

class HSK4ReadingSecondTask(StatesGroup):
    answer = State()

class HSK4ReadingThirdTask(StatesGroup):
    answer = State()