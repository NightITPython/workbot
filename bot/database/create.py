import sqlite3
from config import DB, bot_id, ADMIN_ID, TOKEN


conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        balance REAL DEFAULT 0,
        profit REAL DEFAULT 0,
        referal INTEGER NULL,
        referal_count INTEGER DEFAULT 0,
        bot_id INTEGER UNIQUE NULL
    )"""
)
cur.execute("""
    CREATE TABLE IF NOT EXISTS bots(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bot_status TEXT CHECK (bot_status IN ('online', 'offline')),
        bot_id INTEGER UNIQUE,
        creator INTEGER,
        procent_per_work INTEGER,
        total_profit INTEGER DEFAULT 0,
        status TEXT DEFAULT 'offline' CHECK (status IN ('online', 'offline')),
        users_db TEXT,
        token TEXT UNIQUE,
        main_chat INTEGER,
        vbeaver_chat INTEGER
        
    )"""
)

cur.execute("""
    CREATE TABLE IF NOT EXISTS links(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        endpoint TEXT,
        creator INTEGER,
        vbeaver INTEGER,
        profit INTEGER,
        bot_id INTEGER
    )"""
)

cur.execute("""
    CREATE TABLE IF NOT EXISTS saved_tokens(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT
    )"""
)
cur.execute("INSERT OR IGNORE INTO bots (bot_id, creator, token) VALUES (?, ?, ?)", (bot_id, ADMIN_ID[0], TOKEN))

conn.commit()
conn.close()