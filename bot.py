import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db

from handlers import start, fart, stats
from scheduler import setup_scheduler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    await init_db()

    dp.include_router(start.router)
    dp.include_router(fart.router)
    dp.include_router(stats.router)

    setup_scheduler(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())