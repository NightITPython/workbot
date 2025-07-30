from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from uvicorn import Config, Server
from backend.app import app
from copy import deepcopy


async def start_bot(token: str, routers: list, dp: Dispatcher):
    """ Запуск ботов из БД """
    bot = Bot(
        token=token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        )
    )
    routers = deepcopy(routers)
    dp.include_routers(*routers)
    await dp.start_polling(bot)



async def start_fastapi():
    """ Запуск FastAPI (Только для тестов)"""
    config = Config(app=app, host="localhost", port=8000, log_level="debug")
    server = Server(config)
    await server.serve()
