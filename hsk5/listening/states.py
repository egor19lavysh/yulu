from aiogram.fsm.state import State, StatesGroup


class HSK5ListeningStates(StatesGroup):
    answer = State()