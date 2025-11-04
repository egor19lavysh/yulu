from aiogram.fsm.state import State, StatesGroup


class HSK5ReadingFirstTask(StatesGroup):
    answer = State()

class HSK5ReadingSecondTask(StatesGroup):
    answer = State()

class HSK5ReadingThirdTask(StatesGroup):
    answer = State()