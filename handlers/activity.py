import time
from aiogram import Router, types
from database import db
from config import XP_PER_MESSAGE, XP_COOLDOWN_SECONDS

router = Router()


@router.message()
async def handle_message(message: types.Message):
    if message.from_user is None or message.from_user.is_bot:
        return

    if await db.is_banned(message.from_user.id, message.chat.id):
        return

    await db.count_message(message.from_user.id, message.chat.id)

    now = time.time()
    user = await db.get_user(message.from_user.id, message.chat.id)

    if user:
        last_time = user[2] if user[2] else 0
        if now - last_time < XP_COOLDOWN_SECONDS:
            return

    await db.add_xp(message.from_user.id, message.chat.id, XP_PER_MESSAGE, now)
