import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config import TOKEN
from database import db
from handlers import profile_router, activity_router


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await db.connect()

    dp.include_router(profile_router)
    dp.include_router(activity_router)

    logging.info("Bot started!")
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
