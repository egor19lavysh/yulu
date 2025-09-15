from aiogram.fsm.state import State, StatesGroup


class FirstTask(StatesGroup):
    answer = State()


class SecondTask(StatesGroup):
    answer = State()
