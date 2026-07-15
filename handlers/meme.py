import random
from datetime import datetime, timezone
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

MEME_IMAGES = [
    "https://i.imgflip.com/1h7in3.jpg",
    "https://i.imgflip.com/2/4x60y0.jpg",
    "https://i.imgflip.com/26am.jpg",
    "https://i.imgflip.com/1otk96.jpg",
    "https://i.imgflip.com/43a45p.jpg",
    "https://i.imgflip.com/30b1gx.jpg",
    "https://i.imgflip.com/2w4o2d.jpg",
    "https://i.imgflip.com/28rk0g.jpg",
    "https://i.imgflip.com/2ab7ty.jpg",
    "https://i.imgflip.com/2a6t4g.jpg",
    "https://i.imgflip.com/29v4tf.jpg",
    "https://i.imgflip.com/4t0m5u.jpg",
    "https://i.imgflip.com/486o2b.jpg",
    "https://i.imgflip.com/4er2kg.jpg",
    "https://i.imgflip.com/43i2zi.jpg",
    "https://i.imgflip.com/4/30b1gx.jpg",
    "https://i.imgflip.com/46tjik.jpg",
    "https://i.imgflip.com/2hd.jpg",
    "https://i.imgflip.com/39x0tp.jpg",
    "https://i.imgflip.com/4a4f6s.jpg",
]

DARK_IMAGES = [
    "https://i.imgflip.com/23w1k5.jpg",
    "https://i.imgflip.com/39x0tp.jpg",
    "https://i.imgflip.com/486o2b.jpg",
    "https://i.imgflip.com/4er2kg.jpg",
    "https://i.imgflip.com/4t0m5u.jpg",
    "https://i.imgflip.com/43i2zi.jpg",
    "https://i.imgflip.com/46tjik.jpg",
    "https://i.imgflip.com/4a4f6s.jpg",
    "https://i.imgflip.com/2hd.jpg",
    "https://i.imgflip.com/29v4tf.jpg",
    "https://i.imgflip.com/2a6t4g.jpg",
    "https://i.imgflip.com/28rk0g.jpg",
    "https://i.imgflip.com/2ab7ty.jpg",
    "https://i.imgflip.com/2w4o2d.jpg",
    "https://i.imgflip.com/26am.jpg",
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
    url = random.choice(MEME_IMAGES)
    try:
        await message.answer_photo(url, caption="🤣 Вот тебе мем:")
    except Exception:
        await message.answer("🤣 Мем:\n\nhttps://i.imgflip.com/1h7in3.jpg")


@router.message(Command("dark"))
async def dark(message: types.Message):
    url = random.choice(DARK_IMAGES)
    try:
        await message.answer_photo(url, caption="💀 Чёрный юмор:")
    except Exception:
        await message.answer("💀 Чёрный юмор:\n\nhttps://i.imgflip.com/23w1k5.jpg")


@router.message(Command("quote"))
async def quote(message: types.Message):
    today = datetime.now(timezone.utc).day
    quote_text = QUOTES[today % len(QUOTES)]
    await message.answer(quote_text)
