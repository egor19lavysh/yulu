from aiogram.fsm.state import State, StatesGroup


class FirstTaskStates(StatesGroup):
    sentence = State()


class SecondTaskStates(StatesGroup):
    char = State()
