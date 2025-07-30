from .. import (
    start,
    profile,
    create_link,
    my_links,
    cpanel,
    profile
)


from ..tc import (
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
    edit_bot.tc_menu_handler(),
    add_main_chat.add_main_chat_handler(),
    add_vbeaver_chat.add_vbeaver_chat_handler()
]