from aiogram.fsm.state import State, StatesGroup


class Data(StatesGroup):
    token = State()
    chat = State()
    creator = State()


class BotDelete(StatesGroup):
    answer = State()