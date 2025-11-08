from aiogram.fsm.state import State, StatesGroup


class HSK1ListeningFirstStates(StatesGroup):
    answer = State()

class HSK1ListeningSecondStates(StatesGroup):
    answer = State()

class HSK1ListeningThirdStates(StatesGroup):
    answer = State()

class HSK1ListeningFourthStates(StatesGroup):
    answer = State()