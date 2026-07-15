import time
from aiogram import Router, types
from aiogram.filters import Command
from database import db

router = Router()


@router.message(Command("daily"))
async def daily(message: types.Message):
    if message.from_user is None:
        return

    if await db.is_banned(message.from_user.id, message.chat.id):
        await message.answer("Ты заблокирован и не можешь получать бонусы!")
        return

    now = time.time()
    bonus, streak = await db.claim_daily(message.from_user.id, message.chat.id, now)

    if bonus is None:
        await message.answer("Ты уже получил бонус сегодня! Приходи завтра.")
        return

    text = (
        f"🎁 Ежедневный бонус!\n\n"
        f"💰 Получено: {bonus} XP\n"
        f"🔥 Серия: {streak} дней\n\n"
        f"Продолжай заходить каждый день, чтобы увеличить бонус!"
    )
    await message.answer(text)
