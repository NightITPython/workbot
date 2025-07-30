from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import back_to
from config import bots as bots_data
from database.db import Database

from .states import BotDelete

router = Router()
db = Database()

@router.callback_query(F.data == "delete_bot")
async def delete_bot(
    c: CallbackQuery,
    state: FSMContext
):
    await state.set_state(BotDelete.answer)
    await state.update_data(msg_id=c.message.message_id)
    await c.message.edit_text(
        text="📥  <b>Введите айди бота</b>",
        reply_markup=back_to("cpanel")
    )


@router.message(F.text, BotDelete.answer)
async def answer(
    msg: Message,
    state: FSMContext,
    bot: Bot
):
    data = await state.get_data()
    msg_id = data['msg_id']
    await bot.delete_message(
        chat_id=msg.chat.id,
        message_id=msg_id
    )
    bot_id = msg.text
    if not bot_id.isdigit():
        await state.clear()
        return await msg.answer(
            text="🔴 <b>Введите корректный числовой айди</b>",
            reply_markup=back_to("delete_bot")
        )

    try:
        dp = bots_data[bot_id]
        bot_info = await db.get_bot_info(bot_id)
        token = bot_info['token']
        bot_for_stop = Bot(token)
        await dp.stop_polling(bot_for_stop)
        await msg.answer(
            text=f"✅ <b>Бот остановлен и удален из базы данных.</b>"
        )

    except KeyError:
        return await msg.answer(
            text="🔴 <b>Бот не найден</b>"
        )
    