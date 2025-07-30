from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
from database.db import Database


db = Database()


class isVbeaver(BaseFilter):

    async def __call__(
        self,
        msg: Message | CallbackQuery,
        bot: Bot
    ):

        bot_id = (await bot.me()).id
        bot_info = await db.get_bot_info(bot_id)
        chat_id = msg.chat.id
        vbeaver_chat_id = bot_info['vbeaver_chat']
        
        return vbeaver_chat_id == chat_id