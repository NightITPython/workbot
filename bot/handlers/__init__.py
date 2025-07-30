from . import (
    start,
    profile,
    create_link,
    my_links,
    cpanel,
    profile,
    vbeaver,
    take_for_vbeav
)

from .creator import (
    create_bot,
    delete_bot
)
from .tc import (
    edit_bot,
    add_main_chat,
    add_vbeaver_chat
)
__all__ = "routers"

routers = [
    start.start_handler(),
    profile.profile_handler(),
    create_link.create_link_handler(),
    my_links.my_links_handler(),
    cpanel.cpanel_handler(),
    profile.profile_handler(),
    vbeaver.router,
    take_for_vbeav.router,
    delete_bot.router,
    create_bot.router,
    edit_bot.tc_menu_handler(),
    add_main_chat.add_main_chat_handler(),
    add_vbeaver_chat.add_vbeaver_chat_handler()
]