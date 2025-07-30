from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router

from keyboards.inline import CreatorPanel
from filters.creator import IsCreator



def cpanel_handler():
    router = Router()
    @router.callback_query(F.data == "cpanel")
    @router.message(F.text, Command("cpanel"), IsCreator())
    async def cpanel(
        msg: Message | CallbackQuery
    ):
        panel = CreatorPanel()
        msg = msg.message if isinstance(msg, CallbackQuery) else msg
        await msg.answer(
            text="🛠️ <b>Добро пожаловать в систему администрирования</b>",
            reply_markup=panel.panel()
        )

    return router