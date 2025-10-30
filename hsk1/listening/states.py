from aiogram.fsm.state import State, StatesGroup


class ListeningFirstStates(StatesGroup):
    answer = State()

class ListeningSecondStates(StatesGroup):
    answer = State()

class ListeningThirdStates(StatesGroup):
    answer = State()

class ListeningFourthStates(StatesGroup):
    answer = State()