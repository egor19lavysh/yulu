from aiogram.fsm.state import State, StatesGroup


class HSK4WritingFirstTask(StatesGroup):
    answer = State()


class HSK4WritingSecondTask(StatesGroup):
    answer = State()
