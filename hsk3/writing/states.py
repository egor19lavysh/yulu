from aiogram.fsm.state import State, StatesGroup


class HSK3FirstTaskStates(StatesGroup):
    sentence = State()


class HSK3SecondTaskStates(StatesGroup):
    char = State()
