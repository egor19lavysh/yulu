from aiogram.fsm.state import State, StatesGroup


class HSK2ListeningFirstStates(StatesGroup):
    answer = State()

class HSK2ListeningSecondStates(StatesGroup):
    answer = State()

class HSK2ListeningThirdStates(StatesGroup):
    answer = State()