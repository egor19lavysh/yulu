from aiogram.fsm.state import State, StatesGroup


class QuizStates(StatesGroup):
    WAITING_FOR_ANSWER = State()


class WritingStates(StatesGroup):
    word = State()


class ListeningStates(StatesGroup):
    answer = State()
