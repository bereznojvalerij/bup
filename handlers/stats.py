from aiogram import Router
from aiogram.types import Message
import aiosqlite
from datetime import datetime, timedelta

from database import DB_NAME, get_user_id

router = Router()


@router.message(lambda msg: msg.text == "📊 День")
async def stats_day(message: Message):
    user_id = await get_user_id(message.from_user.id)

    today = datetime.utcnow().date()

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=? AND date(timestamp)=?
        """, (user_id, today)) as cursor:

            result = await cursor.fetchone()
            total = result[0] or 0

    await message.answer(f"Сегодня: {total} 💨")

@router.message(lambda msg: msg.text == "📊 Неделя")
async def stats_week(message: Message):
    user_id = await get_user_id(message.from_user.id)

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=? 
        AND timestamp >= datetime('now', '-7 days')
        """, (user_id,)) as cursor:

            total = (await cursor.fetchone())[0] or 0

    await message.answer(f"За 7 дней: {total} 💨")

@router.message(lambda msg: msg.text == "📊 Месяц")
async def stats_month(message: Message):
    user_id = await get_user_id(message.from_user.id)

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=? 
        AND timestamp >= datetime('now', '-30 days')
        """, (user_id,)) as cursor:

            total = (await cursor.fetchone())[0] or 0

    await message.answer(f"За 30 дней: {total} 💨")

@router.message(lambda msg: msg.text == "📊 Всё время")
async def stats_all(message: Message):
    user_id = await get_user_id(message.from_user.id)

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=?
        """, (user_id,)) as cursor:

            total = (await cursor.fetchone())[0] or 0

    await message.answer(f"За всё время: {total} 💨")

@router.message(lambda msg: msg.text == "🏆 Общий рейтинг")
async def rating(message: Message):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT users.username, SUM(events.count) as total
        FROM events
        JOIN users ON users.id = events.user_id
        GROUP BY users.id
        ORDER BY total DESC
        """) as cursor:

            rows = await cursor.fetchall()

    if not rows:
        await message.answer("Пока нет данных")
        return

    text = "🏆 Общий рейтинг:\n\n"

    for i, (name, count) in enumerate(rows, 1):
        text += f"{i}. {name} — {count} 💨\n"

    await message.answer(text)