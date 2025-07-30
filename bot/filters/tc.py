from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from aiogram.filters import BaseFilter
from database.db import Database


db = Database()


class isTc(BaseFilter):

    async def __call__(
        self,
        msg: Message | CallbackQuery,
        bot: Bot
    ):

        bot_id = (await bot.me()).id
        data_bot = await db.get_bot_info(bot_id)
        user_id = msg.from_user.id

        return user_id == data_bot['creator']