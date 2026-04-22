from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import aiosqlite

from database import DB_NAME, get_all_users


def setup_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    @scheduler.scheduled_job("cron", hour=23, minute=0)
    async def daily_stats():
        today = datetime.utcnow().date()

        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute("""
            SELECT users.username, SUM(events.count)
            FROM events
            JOIN users ON users.id = events.user_id
            WHERE date(events.timestamp)=?
            GROUP BY user_id
            ORDER BY SUM(events.count) DESC
            """, (today,)) as cursor:

                rows = await cursor.fetchall()

        if not rows:
            return

        text = "🏆 Итоги дня:\n\n"

        for i, (name, count) in enumerate(rows, 1):
            text += f"{i}. {name} — {count} 💨\n"

        text += f"\n🎉 Победитель дня: {rows[0][0]}!"

        users = await get_all_users()

        for tg_id, _ in users:
            try:
                await bot.send_message(tg_id, text)
            except:
                pass

    scheduler.start()