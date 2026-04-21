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