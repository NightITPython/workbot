from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery
from database.db import Database
from keyboards.inline import back


db = Database()


def profile_handler():
    router = Router()
    @router.callback_query(F.data == "profile")
    async def profile(
        c: CallbackQuery
    ):
        user_id = c.from_user.id
        username = c.from_user.username
        user_info = await db.get_user_info(user_id)
        created_links = len(await db.get_user_links(user_id))
        profit = user_info['profit']
        await c.message.edit_text(
            text=f"""🦣 <b>Ваш профиль:</b>
            
    <b>🌐 Айди:</b><code> {user_id}</code>
    <b>🌐 Никнейм:</b><code> {username}</code>
    
    <b>📥 Профит:</b><code> {profit}</code>
    <b>🟢 Количество созданных ссылок:</b><code> {created_links}</code>""",
            reply_markup=back()
        )

    return router