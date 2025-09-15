from aiogram.fsm.state import State, StatesGroup


class ReadingFirstTask(StatesGroup):
    answer = State()

class ReadingSecondTask(StatesGroup):
    answer = State()

class ReadingThirdTask(StatesGroup):
    answer = State()