import aiosqlite
from datetime import datetime

DB_NAME = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            count INTEGER,
            timestamp TEXT
        )
        """)

        await db.commit()


async def add_user(telegram_id, username):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT OR IGNORE INTO users (telegram_id, username)
        VALUES (?, ?)
        """, (telegram_id, username))
        await db.commit()


async def get_user_id(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT id FROM users WHERE telegram_id=?
        """, (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def add_event(user_id, count):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO events (user_id, count, timestamp)
        VALUES (?, ?, ?)
        """, (user_id, count, datetime.utcnow().isoformat()))
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT telegram_id, username FROM users") as cursor:
            return await cursor.fetchall()