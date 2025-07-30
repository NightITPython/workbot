from aiogram import Bot
from asyncio import run

async def validate_chat(
    chat_id: int,
    token: str
) -> bool:
    bot = Bot(token)
    try:
        await bot.get_chat_administrators(chat_id)
        return True

    except Exception as e:
        print(e)
        return False


