from aiogram import Router, types
from aiogram.filters import Command
from database import db
from config import get_level, LEVELS

router = Router()

LEVEL_PERKS = {
    "Новичок": "Начни писать чтобы получить XP!",
    "Игрок": "🔓 Доступ к /bet (ставки на XP)",
    "Про": "🔓 Доступ к /bet (2x множитель)\n🔓 Приоритет в топе",
    "Легенда": "🔓 Доступ ко всем мини-играм\n🔓 Двойной ежедневный бонус\n👑 Титул Легенды",
}


@router.message(Command("profile"))
async def profile(message: types.Message):
    if message.from_user is None:
        return

    user = await db.get_user(message.from_user.id, message.chat.id)
    if user is None:
        await message.answer("Ты ещё не написал ни одного сообщения!")
        return

    xp, messages, _ = user
    level = get_level(xp)
    perks = LEVEL_PERKS.get(level, "")

    next_level_xp = None
    for name, req_xp in sorted(LEVELS.items(), key=lambda x: x[1]):
        if req_xp > xp:
            next_level_xp = req_xp
            break

    text = (
        f"🎮 Профиль: {message.from_user.full_name}\n\n"
        f"📊 Уровень: {level}\n"
        f"⭐ Опыт: {xp}\n"
        f"💬 Сообщений: {messages}\n\n"
        f"🎁 Бонусы уровня:\n{perks}"
    )
    if next_level_xp:
        text += f"\n\n📈 До следующего уровня: {next_level_xp - xp} XP"

    await message.answer(text)


@router.message(Command("top"))
async def top(message: types.Message):
    users = await db.get_top(message.chat.id)
    if not users:
        await message.answer("Пока нет данных!")
        return

    medals = ["🥇", "🥈", "🥉"]
    lines = ["🏆 Топ игроков:\n"]

    for i, (user_id, xp, messages) in enumerate(users):
        medal = medals[i] if i < 3 else f"{i+1}."
        level = get_level(xp)
        try:
            user = await message.bot.get_chat_member(message.chat.id, user_id)
            name = user.user.full_name
        except Exception:
            name = f"User {user_id}"
        lines.append(f"{medal} {name} — {xp} XP ({level})")

    await message.answer("\n".join(lines))
