import asyncio
import re
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

TIME_UNITS = {"m": 60, "h": 3600, "d": 86400}


def parse_time(time_str):
    match = re.match(r"(\d+)([mhd])", time_str.lower())
    if not match:
        return None
    value, unit = int(match.group(1)), match.group(2)
    return value * TIME_UNITS[unit]


@router.message(Command("remind"))
async def remind(message: types.Message):
    if message.from_user is None:
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer(
            "Используй: /remind <время> <текст>\n"
            "Примеры:\n"
            "/remind 30m выйти зализ\n"
            "/remind 2h рейд\n"
            "/remind 1d донат"
        )
        return

    seconds = parse_time(args[1])
    if seconds is None:
        await message.answer("Неверный формат времени! Используй: 30m, 2h, 1d")
        return

    text = args[2]
    user_name = message.from_user.full_name

    await message.answer(f"✅ Напоминание через {args[1]}: {text}")

    await asyncio.sleep(seconds)

    await message.answer(f"🔔 {user_name}, напоминаю: {text}")


@router.message(Command("poll"))
async def poll(message: types.Message):
    if message.from_user is None:
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "Используй: /poll <вопрос> | <вариант1> | <вариант2>\n"
            "Пример: /poll Играем в Repo? | Да | Нет | Может быть"
        )
        return

    parts = [p.strip() for p in args[1].split("|")]
    if len(parts) < 2:
        await message.answer("Нужно минимум 2 варианта через |")
        return

    question = parts[0]
    options = parts[1:]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    for i, option in enumerate(options):
        keyboard.inline_keyboard.append([
            types.InlineKeyboardButton(text=f"{option} (0)", callback_data=f"poll:{i}:0")
        ])

    await message.answer(f"📊 {question}", reply_markup=keyboard)
