from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from filters.tc import isTc
from database.db import Database
from keyboards.inline import back
from utils import validate_chat

from .states import EditBot

db = Database()
router = Router()

def add_vbeaver_chat_handler():
    router = Router()
    @router.callback_query(F.data == "edit_bot:add_vbeaver_chat", isTc())
    async def add_vbeaver_chat(
        c: CallbackQuery,
        state: FSMContext
    ):
    
        await c.message.edit_text(
            text="💬 <b>Введите айди чата, убедитесь, что вы добавили бота в чат и дали ему права администратора.</b>",
            reply_markup=back()
        )
        await state.set_state(EditBot.add_vbeaver_chat)
    
    
    @router.message(F.text, EditBot.add_vbeaver_chat)
    async def answer(
        msg: Message,
        state: FSMContext,
        bot: Bot
    ):
        chat_id = msg.text
        token = bot.token
        bot_id = (await bot.me()).id
        try:
            chat_id = int(chat_id)
    
        except:
            return await msg.answer(
                text="❌ <b>Введите корректный айди</b>",
                reply_markup=back()
            )
    
    
        valid = await validate_chat(chat_id, token=token)
        if not valid:
            return await msg.answer(
                text="<b>❌ Чат не найден, возможно вы не добавили бота в чат или не дали ему права администратора</b>",
                reply_markup=back()
            )
    
        await db.edit_bot(
            bot_id,
            column="vbeaver_chat",
            value=chat_id
        )
        await msg.answer(
            text="<b>✅ Чат добавлен!</b>"
        )
        await state.clear()

    return router