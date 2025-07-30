from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F, Router, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from asyncio import sleep

from filters.creator import IsCreator
from keyboards.inline import CreatorPanel, back_to
from database.db import Database
from utils import validate_token, check_pattern_token, validate_chat
from start import start_bot
from config import bots as bots_data

from .__init__ import routers
from .states import Data

db = Database()
router = Router()

data = {}




@router.callback_query(F.data == "create_bot", IsCreator())
async def create_bot(
    c: CallbackQuery,
    state: FSMContext
):
    panel = CreatorPanel()
    token = data.get("token", "Пусто")
    chat = data.get("chat", "Пусто")
    creator = data.get("creator", "Пусто")
    
    await state.clear()
    await c.message.edit_text(
        text=f"""🛠️<b> Создание бота в один клик</b>

<b>🔑 Токен</b> - <blockquote>API Token из BotFather</blockquote>


<b>💬 Чат-лог </b>- <blockquote>ID чата, куда будут приходить все логи ( это не общий чат ) </blockquote>


<b>🦣 TC </b>- <blockquote>Айди главного администратора бота</blockquote>

<blockquote>Нынешние данные:
TOKEN: {token} - Айди токена в базе данных
CHAT: {chat} - Айди чата
CREATOR: {creator} - Айди Т/С
</blockquote>

""",
        reply_markup=panel.create_bot(data)
    )


@router.callback_query(F.data.startswith("create_bot/token:"))
@router.callback_query(F.data.startswith("create_bot/chat:"))
@router.callback_query(F.data.startswith("create_bot/creator:"))
async def insert(
    c: CallbackQuery,
    state: FSMContext
):
    payload = c.data.split("/")[1].split(":")[0]
    texts = {
        "token": "🔑 <i>Вставьте TOKEN-бота из BotFather</i>",
        "chat": "💬 <i>Вставьте айди чата с логами</i>",
        "creator": "🦣 <i>Вставьте айди ТС</i>"
    }
    states = {
        "token": Data.token,
        "chat": Data.chat,
        "creator": Data.creator
    }
    if payload == "chat" and not "token" in data:
        return await c.answer(
            text="🔑 Сначало добавьте TOKEN"
        )
    await c.message.edit_text(
        text=texts[payload],
        reply_markup=back_to("create_bot")
    )

    await state.set_state(states[payload])
    await state.update_data(msg_id=c.message.message_id)

@router.message(F.text, Data.token)
async def get_token(
    msg: Message,
    state: FSMContext,
    bot: Bot
):
    token = msg.text
    state_data = await state.get_data()
    await msg.delete()
    await bot.delete_message(
        chat_id=msg.chat.id,
        message_id=state_data['msg_id']
    )
    for_edit = await msg.answer(
        text="🔑 <b> Найден токен, проверяем токен на паттерн..</b>"
    )
    await sleep(1)
    check = check_pattern_token(token)
    if not check:
        return await for_edit.edit_text(
            text="🔴 <b> Токен не подходит по паттерну</b>"
        )
    else:
        await for_edit.edit_text(
            text="🔑<b> Токен подходит по паттерну, валидируем токен..</b>"
        )

    valid = await validate_token(token)
    if not valid:
        return await for_edit.edit_text(
            text="🔴 <b>Токен недействительный!</b>"
        )

    else:
        await for_edit.edit_text(
            text="🔑 <b>Токен валидный, сохраняем..</b>"
        )
        id_token = await db.add_token(token)
        data['token'] = id_token
        await for_edit.edit_text(
            text="✅ <b>Токен добавлен!</b>",
            reply_markup=back_to("create_bot")
        )
        await state.clear()



@router.message(F.text, Data.chat)
async def get_chat(
    msg: Message,
    state: FSMContext, 
    bot: Bot
):
    chat = msg.text
    state_data = await state.get_data()
    await msg.delete()
    await bot.delete_message(
        chat_id=msg.chat.id,
        message_id=state_data['msg_id']
    )

    for_edit = await msg.answer(
        text="💬 <b>Обнаружен айди, проверяем по паттерну..</b>"
    )

    await sleep(1)
    token = await db.get_token(data['token'])
    await for_edit.edit_text(
        text="💬 <b>Айди подходит по паттерну, валидируем айди..</b>"
    )
    valid = await validate_chat(chat, token)
    if not valid:
        return await for_edit.edit_text(
            text="🔴 <b>Чат не найден, проверьте, добавили ли вы бота в чат и дали ему права администратора!</b>",
            reply_markup=back_to("create_bot")
        )

    data["chat"] = int(chat)
    await for_edit.edit_text(
        text="✅ <b>Айди добавлен!</b>",
        reply_markup=back_to("create_bot")
    )
    await state.clear()



@router.message(F.text, Data.creator)
async def get_creator(
    msg: Message,
    state: FSMContext,
    bot: Bot
):
    creator = msg.text
    state_data = await state.get_data()
    await msg.delete()
    await bot.delete_message(
        chat_id=msg.chat.id,
        message_id=state_data['msg_id']
    )

    for_edit = await msg.answer(
        text="🦣 <b>Обнаружен айди, проверяем по паттерну..</b>"
    )
    if not creator.isdigit():
        return await for_edit.edit_text(
            text="🔴 <b>Айди недействителен, введите числовой айди</b>",
            reply_markup=back_to("create_bot")
        )
    await sleep(1)

    await for_edit.edit_text(
        text="🦣 <b>Айди подходит по паттерну, валидируем айди..</b>"
    )
    valid = await db.user_exists(int(creator))
    if not valid:
        return await for_edit.edit_text(
            text="🔴 <b>Юзер не найден в базе данных.</b>",
            reply_markup=back_to("create_bot")
        )

    data["creator"] = int(creator)
    await for_edit.edit_text(
        text="✅ <b>Айди добавлен!</b>",
        reply_markup=back_to("create_bot")
    )
    await state.clear()


@router.callback_query(F.data == "create_bot/clear")
async def bot_clear(
    c: CallbackQuery
):
    data.clear()
    panel = CreatorPanel()
    token = data.get("token", "Пусто")
    chat = data.get("chat", "Пусто")
    creator = data.get("creator", "Пусто")
    await c.answer(
        text="✅ Данные очищены"
    )
    await c.message.edit_text(
        text=f"""🛠️<b> Создание бота в один клик</b>

<b>🔑 Токен</b> - <blockquote>API Token из BotFather</blockquote>


<b>💬 Чат-лог </b>- <blockquote>ID чата, куда будут приходить все логи ( это не общий чат ) </blockquote>


<b>🦣 TC </b>- <blockquote>Айди главного администратора бота</blockquote>

<blockquote>Нынешние данные:
TOKEN: {token} - Айди токена в базе данных
CHAT: {chat} - Айди чата
CREATOR: {creator} - Айди Т/С
</blockquote>

""",
        reply_markup=panel.create_bot(data)
    )

@router.callback_query(F.data.startswith("create_bot:"))
async def done(c: CallbackQuery):
    data = c.data.split(":")[1].split("_")
    if "empty" in data:
        return await c.answer(
            text="🔴 Заполните все поля",
            show_alert=True
        )

    token, chat, creator = await db.get_token(int(data[0])), int(data[1]), int(data[2])
    me = await Bot(token).me()
    
    bot_id = me.id
    username = me.username
    await db.add_bot(
        token=token,
        bot_id=bot_id,
        chat=chat,
        creator=creator
    )

    await c.message.delete()
    await c.message.answer(
        text=f"🟢 <b>Бот @{username} добавлен в БД и запущен!</b>",
        reply_markup=back_to("cpanel")
    )
    data.clear()
    dp = Dispatcher()
    bots_data[bot_id] = dp

    await start_bot(
        token=token,
        routers=routers,
        dp=dp
    )
