import time
from datetime import datetime, timezone, timedelta
from aiogram import Router, types
from aiogram.filters import Command
from database import db

router = Router()


def get_day_start():
    now = datetime.now(timezone.utc)
    return now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


def get_week_start():
    now = datetime.now(timezone.utc)
    return (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()


@router.message(Command("mystats"))
async def mystats(message: types.Message):
    if message.from_user is None:
        return

    today = get_day_start()
    week = get_week_start()

    today_count = await db.get_user_stats(message.from_user.id, message.chat.id, today)
    week_count = await db.get_user_stats(message.from_user.id, message.chat.id, week)

    text = (
        f"📊 Твоя статистика: {message.from_user.full_name}\n\n"
        f"📅 Сегодня: {today_count} сообщений\n"
        f"📆 За неделю: {week_count} сообщений"
    )
    await message.answer(text)


@router.message(Command("topday"))
async def topday(message: types.Message):
    since = get_day_start()
    users = await db.get_top_period(message.chat.id, since)
    if not users:
        await message.answer("Сегодня пока нет активности!")
        return

    medals = ["🥇", "🥈", "🥉"]
    lines = ["🏆 Топ за сегодня:\n"]

    for i, (user_id, count) in enumerate(users):
        medal = medals[i] if i < 3 else f"{i+1}."
        try:
            member = await message.bot.get_chat_member(message.chat.id, user_id)
            name = member.user.full_name
        except Exception:
            name = f"User {user_id}"
        lines.append(f"{medal} {name} — {count} сообщений")

    await message.answer("\n".join(lines))


@router.message(Command("topweek"))
async def topweek(message: types.Message):
    since = get_week_start()
    users = await db.get_top_period(message.chat.id, since)
    if not users:
        await message.answer("На этой неделе пока нет активности!")
        return

    medals = ["🥇", "🥈", "🥉"]
    lines = ["🏆 Топ за неделю:\n"]

    for i, (user_id, count) in enumerate(users):
        medal = medals[i] if i < 3 else f"{i+1}."
        try:
            member = await message.bot.get_chat_member(message.chat.id, user_id)
            name = member.user.full_name
        except Exception:
            name = f"User {user_id}"
        lines.append(f"{medal} {name} — {count} сообщений")

    await message.answer("\n".join(lines))


@router.message(Command("active"))
async def active(message: types.Message):
    week = get_week_start()
    hourly = await db.get_hourly_activity(message.chat.id, week)
    if not hourly:
        await message.answer("Пока нет данных об активности!")
        return

    max_count = max(c for _, c in hourly)
    bar_width = 15

    lines = ["📈 Активность по часам (за неделю):\n"]
    for hour, count in hourly:
        bar_len = int((count / max_count) * bar_width) if max_count > 0 else 0
        bar = "█" * bar_len
        lines.append(f"{hour:02d}:00 | {bar} {count}")

    await message.answer("\n".join(lines))
