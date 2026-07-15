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


pending_duels = {}


@router.message(Command("duel"))
async def duel(message: types.Message):
    if message.from_user is None:
        return

    if await db.is_banned(message.from_user.id, message.chat.id):
        await message.answer("Ты заблокирован!")
        return

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.answer("Ответь на сообщение того, с кем хочешь дуэль!")
        return

    challenger_id = message.from_user.id
    target_id = message.reply_to_message.from_user.id

    if challenger_id == target_id:
        await message.answer("Нельзя дуэлить сам с собой!")
        return

    if message.reply_to_message.from_user.is_bot:
        await message.answer("Нельзя дуэлить с ботом!")
        return

    user = await db.get_user(challenger_id, message.chat.id)
    if not user or user[0] < 10:
        await message.answer("Нужно минимум 10 XP для дуэли!")
        return

    target = await db.get_user(target_id, message.chat.id)
    if not target or target[0] < 10:
        await message.answer("У противника недостаточно XP!")
        return

    target_name = message.reply_to_message.from_user.full_name

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text="⚔️ Принять дуэль!", callback_data=f"duel_accept:{challenger_id}")
    ]])

    await message.answer(
        f"⚔️ {message.from_user.full_name} вызывает {target_name} на дуэль!\n\n"
        f"Ставка: 10 XP\n"
        f"Ждём ответа...",
        reply_markup=keyboard
    )

    pending_duels[challenger_id] = {
        "target_id": target_id,
        "chat_id": message.chat.id,
    }


@router.callback_query(lambda c: c.data.startswith("duel_accept:"))
async def duel_accept(callback: types.CallbackQuery):
    challenger_id = int(callback.data.split(":")[1])
    target_id = callback.from_user.id

    if challenger_id not in pending_duels:
        await callback.answer("Дуэль уже отменена!")
        return

    duel_data = pending_duels[challenger_id]
    if duel_data["target_id"] != target_id:
        await callback.answer("Эта дуэль не для тебя!")
        return

    chat_id = duel_data["chat_id"]
    del pending_duels[challenger_id]

    challenger_roll = random.randint(1, 6)
    target_roll = random.randint(1, 6)

    challenger_user = await callback.bot.get_chat_member(chat_id, challenger_id)
    target_user = await callback.bot.get_chat_member(chat_id, target_id)

    c_name = challenger_user.user.full_name
    t_name = target_user.user.full_name

    if challenger_roll > target_roll:
        winner_id, loser_id = challenger_id, target_id
        winner_name, loser_name = c_name, t_name
        w_roll, l_roll = challenger_roll, target_roll
    elif target_roll > challenger_roll:
        winner_id, loser_id = target_id, challenger_id
        winner_name, loser_name = t_name, c_name
        w_roll, l_roll = target_roll, challenger_roll
    else:
        await callback.message.edit_text(
            f"⚔️ Дуэль: {c_name} vs {t_name}\n\n"
            f"{DICE_FACES[challenger_roll - 1]} vs {DICE_FACES[target_roll - 1]}\n\n"
            f"Ничья! XP не забирается."
        )
        await callback.answer()
        return

    await db.add_xp(winner_id, chat_id, 10, 0)
    await db.add_xp(loser_id, chat_id, -10, 0)

    await callback.message.edit_text(
        f"⚔️ Дуэль: {c_name} vs {t_name}\n\n"
        f"{DICE_FACES[w_roll - 1]} vs {DICE_FACES[l_roll - 1]}\n\n"
        f"🏆 Победитель: {winner_name}!\n"
        f"💰 +10 XP победителю, -10 XP проигравшему"
    )
    await callback.answer()
