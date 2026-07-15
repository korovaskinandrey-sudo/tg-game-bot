from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    text = (
        "📌 Команды бота:\n\n"
        "🎮 Основные:\n"
        "/profile — твой профиль\n"
        "/top — топ игроков\n"
        "/daily — ежедневный бонус\n"
        "/help — эта справка\n\n"
        "📊 Статистика:\n"
        "/mystats — твоя статистика\n"
        "/topday — топ за сегодня\n"
        "/topweek — топ за неделю\n"
        "/active — активность по часам\n\n"
        "🎲 Мини-игры:\n"
        "/dice — бросить кубик\n"
        "/slots — слоты\n"
        "/bet <сумма> — поставить XP\n\n"
        "🤣 Развлечения:\n"
        "/meme — мем дня\n"
        "/quote — цитата дня\n"
        "/randommeme — случайный мем\n\n"
        "🔧 Утилиты:\n"
        "/remind <время> <текст> — напоминание\n"
        "/poll <вопрос> | <вариант1> | <вариант2> — опрос\n\n"
        "👑 Админ:\n"
        "/reset — сбросить XP (ответом)\n"
        "/setxp <число> — установить XP (ответом)\n"
        "/ban — забанить (ответом)\n"
        "/unban — разбанить (ответом)\n\n"
        "⏱ Время: m=минуты, h=часы, d=дни\n"
        "Пример: /remind 2h рейд"
    )
    await message.answer(text)
