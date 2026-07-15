from aiogram import Router, types
from aiogram.filters import Command
from database import db
from config import ADMIN_IDS

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("reset"))
async def reset(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ!")
        return

    if message.reply_to_message is None or message.reply_to_message.from_user is None:
        await message.answer("Ответь на сообщение пользователя, которого хочешь сбросить.")
        return

    target_id = message.reply_to_message.from_user.id
    await db.reset_user(target_id, message.chat.id)
    await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} сброшен!")


@router.message(Command("setxp"))
async def set_xp(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ!")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Используй: /setxp <количество> (ответь на сообщение)")
        return

    try:
        xp = int(args[1])
    except ValueError:
        await message.answer("Количество XP должно быть числом!")
        return

    if message.reply_to_message is None or message.reply_to_message.from_user is None:
        await message.answer("Ответь на сообщение пользователя!")
        return

    target_id = message.reply_to_message.from_user.id
    await db.set_xp(target_id, message.chat.id, xp)
    await message.answer(f"У {message.reply_to_message.from_user.full_name} теперь {xp} XP!")


@router.message(Command("ban"))
async def ban(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ!")
        return

    if message.reply_to_message is None or message.reply_to_message.from_user is None:
        await message.answer("Ответь на сообщение пользователя, которого хочешь забанить.")
        return

    target_id = message.reply_to_message.from_user.id
    await db.ban_user(target_id, message.chat.id)
    await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} забанен!")


@router.message(Command("unban"))
async def unban(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ!")
        return

    if message.reply_to_message is None or message.reply_to_message.from_user is None:
        await message.answer("Ответь на сообщение пользователя, которого хочешь разбанить.")
        return

    target_id = message.reply_to_message.from_user.id
    await db.unban_user(target_id, message.chat.id)
    await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} разбанен!")
