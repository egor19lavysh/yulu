from aiogram.fsm.state import State, StatesGroup


class ListeningSecondStates(StatesGroup):
    poll_answer = State()


class ListeningThirdStates(StatesGroup):
    poll_answer = State()
