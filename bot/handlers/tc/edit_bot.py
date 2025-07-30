from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from filters.tc import isTc
from keyboards.inline import edit_bot




def tc_menu_handler():
    router = Router()
    @router.message(F.text, Command("tc"), isTc())
    async def tc_menu(
        msg: Message
    ):
        await msg.delete()
        await msg.answer(
            text="<b>🛠️ Вы вошли в панель для редактирования бота</b>",
            reply_markup=edit_bot()
        )
    return router