from aiogram.fsm.state import State, StatesGroup


class ListeningFirstStates(StatesGroup):
    answer = State()