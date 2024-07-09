import psycopg2
from config import db_connection_string
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import user_handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from pybots.user_bot import add_gift_bonus, select_tokens, select_birthday

logging.basicConfig(level=logging.INFO)


async def check_users_birthday(bot):
    bds = select_birthday()
    for bd in bds:
        if datetime.date(datetime.now()) == bd[2]:
            await bot.send_message(chat_id=bd[0], text=f'С др {bd[1]}!')
            add_gift_bonus(500, datetime.date(datetime.now() + timedelta(weeks=1)), bd[0])


tokens = select_tokens()
user_bot = Bot(token=tokens[1][0])
dp = Dispatcher()


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_users_birthday, trigger='cron', day_of_week='*',
                      args=(user_bot,), hour=10, minute=30, timezone='Europe/Moscow')
    scheduler.start()
    dp.include_routers(user_handlers.router)
    await dp.start_polling(user_bot)


if __name__ == "__main__":
    asyncio.run(main())
