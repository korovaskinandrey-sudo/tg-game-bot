import random
from aiogram import Router, types
from aiogram.filters import Command
from database import db

router = Router()

DICE_FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
SLOT_SYMBOLS = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣"]


@router.message(Command("dice"))
async def dice(message: types.Message):
    if message.from_user is None:
        return

    if await db.is_banned(message.from_user.id, message.chat.id):
        await message.answer("Ты заблокирован!")
        return

    result = random.randint(1, 6)
    xp = result * 2

    user = await db.get_user(message.from_user.id, message.chat.id)
    if user:
        await db.add_xp(message.from_user.id, message.chat.id, xp, 0)

    await message.answer(
        f"🎲 {message.from_user.full_name} бросает кубик...\n\n"
        f"{DICE_FACES[result - 1]}\n\n"
        f"Выпало: {result}\n"
        f"💰 Получено: {xp} XP"
    )


@router.message(Command("slots"))
async def slots(message: types.Message):
    if message.from_user is None:
        return

    if await db.is_banned(message.from_user.id, message.chat.id):
        await message.answer("Ты заблокирован!")
        return

    symbols = [random.choice(SLOT_SYMBOLS) for _ in range(3)]
    s1, s2, s3 = symbols

    if s1 == s2 == s3:
        xp = 50
        result = "ДЖЕКПОТ! 🎉"
    elif s1 == s2 or s2 == s3 or s1 == s3:
        xp = 15
        result = "Почти! 🤏"
    else:
        xp = 0
        result = "Не повезло 😢"

    user = await db.get_user(message.from_user.id, message.chat.id)
    if user and xp > 0:
        await db.add_xp(message.from_user.id, message.chat.id, xp, 0)

    text = (
        f"🎰 Слоты для {message.from_user.full_name}\n\n"
        f"[ {s1} | {s2} | {s3} ]\n\n"
        f"{result}\n"
    )
    if xp > 0:
        text += f"💰 Получено: {xp} XP"

    await message.answer(text)


@router.message(Command("bet"))
async def bet(message: types.Message):
    if message.from_user is None:
        return

    if await db.is_banned(message.from_user.id, message.chat.id):
        await message.answer("Ты заблокирован!")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Используй: /bet <сумма>\nПример: /bet 50")
        return

    try:
        amount = int(args[1])
    except ValueError:
        await message.answer("Сумма должна быть числом!")
        return

    if amount <= 0:
        await message.answer("Сумма должна быть больше 0!")
        return

    user = await db.get_user(message.from_user.id, message.chat.id)
    if not user or user[0] < amount:
        await message.answer(f"Недостаточно XP! У тебя {user[0] if user else 0} XP")
        return

    multiplier = random.choice([0, 0.5, 1, 1.5, 2, 3])
    win = int(amount * multiplier)

    if win > 0:
        await db.add_xp(message.from_user.id, message.chat.id, win - amount, 0)
        emoji = "🟢"
        result = f"Выигрыш: +{win} XP"
    else:
        await db.add_xp(message.from_user.id, message.chat.id, -amount, 0)
        emoji = "🔴"
        result = f"Проигрыш: -{amount} XP"

    new_xp = user[0] + win - amount
    await message.answer(
        f"🎲 Ставка {message.from_user.full_name}: {amount} XP\n\n"
        f"{emoji} {result}\n"
        f"💰 Баланс: {new_xp} XP"
    )
