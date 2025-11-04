from aiogram.fsm.state import State, StatesGroup


class HSK5WritingFirstTask(StatesGroup):
    answer = State()

class HSK5WritingSecondTask(StatesGroup):
    answer = State()

class HSK5WritingThirdTask(StatesGroup):
    answer = State()
