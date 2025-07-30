from aiogram.fsm.state import StatesGroup, State



class Application(StatesGroup):
    answer = State()