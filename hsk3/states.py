from aiogram.fsm.state import State, StatesGroup


class QuizStates(StatesGroup):
    WAITING_FOR_ANSWER = State()


class WritingStates(StatesGroup):
    word = State()


class ListeningFirstStates(StatesGroup):
    answer = State()

class ListeningSecondStates(StatesGroup):
    answer = State()

class ListeningThirdStates(StatesGroup):
    answer = State()
