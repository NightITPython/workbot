
from database import create
from asyncio import run, create_task, gather
from handlers.__init__ import routers
from database.db import Database
from start import start_bot, start_fastapi
from aiogram import Dispatcher
from config import bots as bots_data
from copy import deepcopy

db = Database()


async def main() -> None:
    bots = await db.get_bots_info()
    tasks = []
    for bot in bots:
        token = bot['token']
        bot_id = bot['bot_id']
        dp = Dispatcher()
        bots_data[bot_id] = dp
        tasks.append(
            create_task(
                start_bot(
                    token=token,
                    routers=deepcopy(routers),
                    dp=dp
                )
            )
        )

    tasks.append(
        create_task(
            start_fastapi()
        )
    )

    await gather(*tasks)


if __name__ == "__main__":
    run(main())