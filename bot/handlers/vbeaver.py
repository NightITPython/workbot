from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from filters.vbeaver import isVbeaver
from aiogram import Router, F, Bot
from keyboards import inline
from database.db import Database


db = Database()
router = Router()


@router.message(F.text, Command("menu"), isVbeaver())
async def vbeaver_menu(
    msg: Message
):
    await msg.answer(
        text=f"❗️ <b>Панель вбивера @{msg.from_user.username}</b>",
        reply_markup=inline.vbeaver_menu(msg.from_user.id)
    )


@router.callback_query(F.data.startswith("start_work"))
@router.callback_query(F.data.startswith("stop_work"))
async def manage(
    c: CallbackQuery,
    bot: Bot
):
    user_id = int(c.data.split(":")[1])
    if not user_id == c.from_user.id:
        return await c.answer(
            text="📛 Не трогай чужое!"
        )

    bot_id = (await bot.me()).id
    bot_info = await db.get_bot_info(bot_id)
    main_chat = bot_info['main_chat']
    work_info_text = None
    if "start_work" in c.data:
        work_info_text = f"❗️ <b>Вбивер {c.from_user.username} начал работу</b>"
    else:
        work_info_text = f"❗️ <b>Вбивер {c.from_user.username} закончил работу</b>"
    await bot.send_message(
        chat_id=main_chat,
        text=work_info_text
    )
