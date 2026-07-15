import random
from datetime import datetime, timezone
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

MEMES = [
    "🎮 Когда все онлайн, а ты один в лобби...",
    "💀 Тиммейт умер от кулачка в_REPO",
    "🏆 Ты: 'Я профи!' | Реальность: 0 XP за день",
    "😴 Когда ждёшь пока сервер поднимется",
    "🔥 Тот момент когда получил 100 XP за одно сообщение",
    "🤡 Когда забыл /daily и потерял серию",
    "💀 Когда тебя убили в первый раз в игре",
    "🏆 Топ-1 в топе, но всех забанили",
    "😴 Ожидание: 5 минут | Реальность: 5 часов",
    "🎮 Играем в Repo? | Нет, я на /slots",
    "🔥 Когда серия 7 дней и бонус 70 XP",
    "💀 Тот момент когда /bet съел весь XP",
    "🏆 Когда все в топе, а ты>Last",
    "😴 Когда напоминание приходит в 3 часа ночи",
    "🎮 Давай мини-игру! | У нас уже есть слоты",
    "🔥 Легенда: 1000 XP | Я: 10 XP и горжусь",
    "💀 Когда /poll: 'Кто за?' | 0 голосов",
    "🏆 Когда забыл пароль от аккаунта",
    "😴 Когда бот упал, а ты не знаешь команд",
    "🎮 Я: 'Давай в Repo!' | Тиммейт: '/slots'",
]

QUOTES = [
    "💡 'XP не приходит к тем, кто сидит без дела.' — Мудрый Бот",
    "💡 'Каждое сообщение — это шаг к Легенде.' — Древний Пророк",
    "💡 'Серия важнее одноразового бонуса.' — Философ Бот",
    "💡 'Кубик не врёт, слоты не врут, только лень врёт.' — Учитель",
    "💡 'Бан — это не конец, это пауза.' — Админ",
    "💡 'Ставь XP — получай эмоции.' — Игрок",
    "💡 'Помни: /daily каждый день!' — Добрый Бот",
    "💡 'Топ строится сообщениями, не ставками.' — Мудрец",
    "💡 'Когда жизнь даёт лимоны — делай /slots.' — Оптимист",
    "💡 'Один XP — это лучше чем ноль XP.' — Философ",
]


@router.message(Command("meme"))
async def meme(message: types.Message):
    today = datetime.now(timezone.utc).day
    meme_text = MEMES[today % len(MEMES)]
    await message.answer(f"🤣 Мем дня:\n\n{meme_text}")


@router.message(Command("quote"))
async def quote(message: types.Message):
    today = datetime.now(timezone.utc).day
    quote_text = QUOTES[today % len(QUOTES)]
    await message.answer(quote_text)


@router.message(Command("randommeme"))
async def randommeme(message: types.Message):
    meme_text = random.choice(MEMES)
    await message.answer(f"🤣 Случайный мем:\n\n{meme_text}")
