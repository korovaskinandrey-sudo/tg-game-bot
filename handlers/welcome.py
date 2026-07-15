from aiogram import Router, types

router = Router()


@router.chat_member()
async def welcome(event: types.ChatMemberUpdated):
    if event.new_chat_member.status not in ("member", "restricted"):
        return

    if event.old_chat_member.status in ("member", "restricted"):
        return

    name = event.new_chat_member.user.full_name
    await event.answer(
        f"👋 Добро пожаловать, {name}!\n\n"
        f"🎮 Я бот для отслеживания активности.\n"
        f"Пиши сообщения, получай XP и поднимайся в топе!\n\n"
        f"📌 Команды:\n"
        f"/profile — твой профиль\n"
        f"/top — топ игроков\n"
        f"/daily — ежедневный бонус\n"
        f"/mystats — твоя статистика\n"
        f"/dice — бросить кубик\n"
        f"/slots — слоты"
    )
