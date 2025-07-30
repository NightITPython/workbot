from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config import ADMIN_ID


class IsCreator(BaseFilter):

    async def __call__(
        self,
        msg: Message | CallbackQuery
    ):
        return msg.from_user.id in ADMIN_ID