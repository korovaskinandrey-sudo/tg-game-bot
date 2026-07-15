import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config import TOKEN
from database import db
from handlers import profile_router, activity_router
from handlers.daily import router as daily_router
from handlers.admin import router as admin_router
from handlers.stats import router as stats_router
from handlers.games import router as games_router
from handlers.utils import router as utils_router
from handlers.welcome import router as welcome_router
from handlers.help import router as help_router
from handlers.meme import router as meme_router


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    await db.connect()

    dp.include_router(profile_router)
    dp.include_router(daily_router)
    dp.include_router(admin_router)
    dp.include_router(stats_router)
    dp.include_router(games_router)
    dp.include_router(utils_router)
    dp.include_router(welcome_router)
    dp.include_router(help_router)
    dp.include_router(meme_router)
    dp.include_router(activity_router)

    logging.info("Bot started!")
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
