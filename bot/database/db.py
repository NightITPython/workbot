import aiosqlite
from config import DB

class Database:
    def __init__(
        self
    ):
        pass

    async def user_exists(
        self,
        user_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            async with db.execute(
                "SELECT user_id FROM users WHERE user_id = ?",
                (user_id,)
            ) as cursor:
                fetch = await cursor.fetchone()
        return fetch is not None

    async def add_user(
        self,
        user_id: int,
        username: str,
        referal: int=0
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id, username, referal) VALUES (?, ?, ?)", (user_id, username, referal))
            await db.commit()


    
    async def get_user_info(
        self,
        user_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                fetch = await cursor.fetchone()
                if fetch is None:
                    return None
        return {
            'username': fetch[2],
            'balance': fetch[3],
            'profit': fetch[4],
            'referal': fetch[5],
            'referal_count': fetch[6],
            'bot_id': fetch[7]
        }

    async def update_balance(self, user_id: int, new_balance: int):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "UPDATE users SET balance = ? WHERE user_id = ?",
                (new_balance, user_id)
            )
            await db.commit()


    async def get_bot_info(
        self,
        bot_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            async with db.execute(
                "SELECT bot_status, creator, procent_per_work, total_profit, status, users_db, token, main_chat, vbeaver_chat FROM bots WHERE bot_id = ?",
                (bot_id,)
            ) as cursor:
                fetch = await cursor.fetchone()
                if fetch is None:
                    return None
                return {
                    "bot_id": bot_id,
                    "bot_status": fetch[0],
                    "creator": fetch[1],
                    "procent_per_work": fetch[2],
                    "total_profit": fetch[3],
                    "status": fetch[4],
                    "users_db": fetch[5],
                    "token": fetch[6],
                    "main_chat": fetch[7],
                    "vbeaver_chat": fetch[8]
                }

    async def get_bots_info(
        self
    ):
        async with aiosqlite.connect(DB) as db:
            async with db.execute(
                "SELECT bot_id FROM bots"
            ) as cursor:
                fetch = await cursor.fetchall()

        bots = []
        for bot in fetch:
            bot_info = await self.get_bot_info(bot[0])
            bots.append(bot_info)

        return bots

    async def ban_user(
        self,
        user_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO banned (user_id) VALUES (?) ",
                (user_id,)
            )
            await db.commit()
            
    async def unban_user(
        self,
        user_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "DELETE FROM banned WHERE user_id = ?",
                (user_id,)
            )
            await db.commit()

    async def check(
        self,
        user_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            async with db.execute(
                "SELECT user_id FROM banned WHERE user_id = ?",
                (user_id,)
            ) as cursor:
                fetch = await cursor.fetchone()
                return fetch is not None

    async def create_table(
        self,
        bot_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {bot_id}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    user_id INTEGER UNIQUE, 
                    username TEXT,
                    isvbeaver INTEGER,
                    profit INTEGER
                )"""
            )
            await db.commit()


    async def add_bot(
        self,
        bot_id: int,
        creator: int,
        token: str,
        chat: int
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO bots (bot_id, creator, token) VALUES (?, ?, ?)",
                (bot_id, creator, token)
            )
            await self.create_table(bot_id)
            await db.commit()

    async def edit_bot(
        self,
        bot_id,
        column,
        value
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                f"UPDATE bots SET {column} = ? WHERE bot_id = ?",
                (value, bot_id)
            )
            await db.commit()


    async def get_user_links(
        self,
        user_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            async with db.execute(
                "SELECT * FROM links WHERE creator = ?",
                (user_id,)
            ) as cursor:
                fetch = await cursor.fetchall()

        data = []

        for link in fetch:
            data.append(
                {
                    "endpoint": link[1],
                    "creator": link[2],
                    "vbeaver": link[3],
                    "profit": link[4]
                }
            )

        return data


    async def delete_bot(
        self,
        bot_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "DELETE FROM bots WHERE bot_id = ?" 
                (bot_id,)
            )
            await db.commit()

    
    async def add_token(
        self,
        token: str
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO saved_tokens (token) VALUES (?)",
                (token,)
            )
            await db.commit()
            async with db.execute(
                "SELECT id FROM saved_tokens WHERE token = ?",
                (token,)
            ) as cursor:
                fetch = await cursor.fetchone()

        return fetch[0]


    async def delete_token(
        self,
        id: int
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "DELETE FROM saved_tokens WHERE id = ?",
                (id,)
            )
            await db.commit()


    async def get_token(
        self,
        id: int
    ):
        async with aiosqlite.connect(DB) as db:

            async with db.execute(
                "SELECT token FROM saved_tokens WHERE id = ?",
                (id,)
            ) as cursor:
                fetch = await cursor.fetchone()

        return fetch[0]


    async def get_token_id(
        self,
        token: str
    ):
        async with aiosqlite.connect(DB) as db:

            async with db.execute(
                "SELECT id FROM saved_tokens WHERE token = ?",
                (token,)
            ) as cursor:
                fetch = await cursor.fetchone()

        return fetch[0]

    async def add_vbeaver(
        self,
        vbeaver_id: int
    ):
        pass


    async def add_endpoint(
        self,
        user_id: int,
        endpoint: str,
        bot_id: int
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO links (endpoint, creator) VALUES (?, ?)",
                (endpoint, user_id, bot_id)
            )
            await db.commit()


    async def get_endpoint(
        self,
        endpoint: str
    ):
        async with aiosqlite.connect(DB) as db:
            async with db.execute(
                "SELECT creator, bot_id, vbeaver, profit FROM links WHERE endpoint = ?",
                (endpoint,)
            ) as cursor:
                fetch = await cursor.fetchone()


        if fetch is None:
            return None
        return {
            "creator": fetch[0],
            "bot_id": fetch[1],
            "vbeaver": fetch[2],
            "profit": fetch[3]
        }


    async def edit_link(
        self,
        endpoint: str,
        column: str,
        value
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                f"UPDATE links SET {column} = ? WHERE endpoint = ?",
                (value, endpoint)
            )
            await db.commit()

    async def add_link(
        self,
        creator: int,
        bot_id: int,
        endpoint: str
    ):
        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "INSERT OR IGNORE INTO links (creator, bot_id, endpoint) VALUES (?, ?, ?)",
                (creator, bot_id, endpoint)
            )
            await db.commit()