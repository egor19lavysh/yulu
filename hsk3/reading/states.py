from aiogram.fsm.state import State, StatesGroup


class HSK3QuizStates(StatesGroup):
    WAITING_FOR_ANSWER = State()