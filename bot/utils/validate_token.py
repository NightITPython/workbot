from aiogram import Bot
import re


def check_pattern_token(
    token: str
) -> bool:
    pattern = re.compile(r'^\d{6,12}:[a-zA-Z0-9_-]{35,40}$')
    return bool(pattern.fullmatch(token))


async def validate_token(
    token: str
) -> bool:
    bot = Bot(token)
    try:
        await bot.me()
        return True
    except:
        return False

