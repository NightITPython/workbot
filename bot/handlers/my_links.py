from aiogram import F, Router
from aiogram.types import CallbackQuery
from keyboards.inline import links




def my_links_handler():
    router = Router()
    @router.callback_query(F.data == "links")
    async def show_links(
        c: CallbackQuery
    ):
        await c.message.edit_text(
            text="🟢 <b> Список созданных ссылок вами</b>",
            reply_markup=await links(
                user_id=c.from_user.id
            )
        )
    return router