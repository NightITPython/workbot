from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database.db import Database
from keyboards.inline import menu


from .states import Application

db = Database()


def start_handler():
    router = Router()
    @router.message(CommandStart())
    @router.callback_query(F.data == "back_to_menu")
    async def start(
        msg: Message | CallbackQuery,
        state: FSMContext,
        bot: Bot

    ):
        await state.clear()
        me = await bot.get_me()
        bot_id = me.id
        referal = 0
        if isinstance(msg, Message):
            if " " in msg.text:
                referal_id = msg.text.split(" ")[1]
                if not referal_id.isdigit():
                    pass

                elif int(referal_id) == msg.from_user.id:
                    pass

                elif not await db.user_exists(int(referal_id)):
                    pass

                elif await db.user_exists(msg.from_user.id):
                    pass
                referal = int(referal_id)

        #if not await db.user_exists(msg.from_user.id):
            #await state.set_state(Application.answer)
            #return await msg.answer(
                #text="""<b>📥 Добро пожаловать, для регистрации в боте подайте заявку по анкете</b><blockquote><code>Расскажите о вашем предыдущем опыте работы, какие были профиты, достижения и так далее. (фотографии отправлять ссылкой imgur)</code></blockquote><i>Ваша заявка будет просмотрена в течение 24 часов</i>"""
            #)

        if isinstance(msg, CallbackQuery):
            await msg.message.delete()

        await db.add_user(
            user_id=msg.from_user.id,
            username=msg.from_user.username,
            referal=None
        )
        user_id = msg.from_user.id
        username = msg.from_user.username

        bot_info = await db.get_bot_info(bot_id)
        status = bot_info['status']
        msg = msg.message if isinstance(msg, CallbackQuery) else msg

        user_info = await db.get_user_info(user_id)
        created_links = len(await db.get_user_links(user_id))
        profit = user_info['profit']
        await msg.answer(
            text=f"""🦣 <b>Ваш профиль:</b>
            
<b>🌐 Айди:</b><code> {user_id}</code>
<b>🌐 Никнейм:</b><code> {username}</code>
    
<b>📥 Профит:</b><code> {profit}</code>
<b>🟢 Количество созданных ссылок:</b><code> {created_links}</code>""",
            reply_markup=menu()
        )

        # Добавить логику уведомления о реферале
        # Добавить логику добавления в базу данных реферала
    return router
