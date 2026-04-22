from aiogram import Router
from aiogram.types import CallbackQuery
import aiosqlite
from keyboards.main import fart_keyboard, main_keyboard

from database import DB_NAME, get_user_id

router = Router()


# 📊 День
@router.callback_query(lambda c: c.data == "day")
async def stats_day(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    user_id = await get_user_id(callback.from_user.id)

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=? AND date(timestamp)=date('now')
        """, (user_id,)) as cursor:

            total = (await cursor.fetchone())[0] or 0

    if callback.message.chat.type == "private":
        await callback.message.answer(
            f"Сегодня: {total} 💨",
            reply_markup=main_keyboard()
        )
    else:
        await callback.message.answer(
            f"Сегодня: {total} 💨"
        )


# 📊 Неделя
@router.callback_query(lambda c: c.data == "week")
async def stats_week(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    user_id = await get_user_id(callback.from_user.id)

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=? 
        AND timestamp >= datetime('now', '-7 days')
        """, (user_id,)) as cursor:

            total = (await cursor.fetchone())[0] or 0

    if callback.message.chat.type == "private":
        await callback.message.answer(
            f"За 7 дней: {total} 💨",
            reply_markup=main_keyboard()
        )
    else:
        await callback.message.answer(
            f"За 7 дней: {total} 💨"
        )

# 📊 Месяц
@router.callback_query(lambda c: c.data == "month")
async def stats_month(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    user_id = await get_user_id(callback.from_user.id)

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=? 
        AND timestamp >= datetime('now', '-30 days')
        """, (user_id,)) as cursor:

            total = (await cursor.fetchone())[0] or 0

    if callback.message.chat.type == "private":
        await callback.message.answer(
            f"За 30 дней: {total} 💨",
            reply_markup=main_keyboard()
        )
    else:
        await callback.message.answer(
            f"За 30 дней: {total} 💨"
        )


# 📊 Всё время
@router.callback_query(lambda c: c.data == "all")
async def stats_all(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    user_id = await get_user_id(callback.from_user.id)

    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
        SELECT SUM(count) FROM events
        WHERE user_id=?
        """, (user_id,)) as cursor:

            total = (await cursor.fetchone())[0] or 0

    if callback.message.chat.type == "private":
        await callback.message.answer(
            f"За все время: {total} 💨",
            reply_markup=main_keyboard()
        )
    else:
        await callback.message.answer(
            f"За все время: {total} 💨"
        )


# 🏆 Рейтинг
@router.callback_query(lambda c: c.data == "rating")
async def rating(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
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
        await callback.answer("Пока нет данных", show_alert=True)
        return

    text = "🏆 Рейтинг:\n\n"
    for i, (name, count) in enumerate(rows, 1):
        text += f"{i}. {name or 'Без имени'} — {count} 💨\n"

    if callback.message.chat.type == "private":
        await callback.message.answer(text, reply_markup=main_keyboard())
    else:
        await callback.message.answer(text)