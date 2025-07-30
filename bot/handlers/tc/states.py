from aiogram.fsm.state import State, StatesGroup


class EditBot(StatesGroup):
    add_main_chat = State()
    add_vbeaver_chat = State()