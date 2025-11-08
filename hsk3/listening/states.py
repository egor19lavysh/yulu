from aiogram.fsm.state import State, StatesGroup


class HSK3ListeningFirstStates(StatesGroup):
    answer = State()


class HSK3ListeningSecondStates(StatesGroup):
    answer = State()


class HSK3ListeningThirdStates(StatesGroup):
    answer = State()
