import random
import aiohttp
from datetime import datetime, timezone
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

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

MEME_APIS = [
    "https://meme-api.com/gimme",
    "https://meme-api.com/gimme/memes",
    "https://meme-api.com/gimme/dankmemes",
    "https://meme-api.com/gimme/darkmemes",
    "https://meme-api.com/gimme/me_irl",
]

DARK_APIS = [
    "https://meme-api.com/gimme/darkmemes",
    "https://meme-api.com/gimme/DarkHumorAndMemes",
    "https://meme-api.com/gimme/meanjokes",
    "https://meme-api.com/gimme/roastme",
]


async def fetch_meme(urls):
    for api_url in urls:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data and data.get("url"):
                            return data
        except Exception:
            continue
    return None


@router.message(Command("meme"))
async def meme(message: types.Message):
    await message.answer("🔍 Ищу мем...")

    meme_data = await fetch_meme(MEME_APIS)
    if meme_data:
        title = meme_data.get("title", "")
        url = meme_data.get("url", "")
        text = f"🤣 Мем:\n\n{title}" if title else "🤣 Вот тебе мем:"

        if url.endswith((".jpg", ".jpeg", ".png", ".gif")):
            try:
                await message.answer_photo(url, caption=text)
                return
            except Exception:
                pass

        if url:
            text += f"\n\n🔗 {url}"
        await message.answer(text)
    else:
        await message.answer("🤣 Мем дня:\n\nНе удалось загрузить мем, попробуй позже!")


@router.message(Command("dark"))
async def dark(message: types.Message):
    await message.answer("🔍 Ищу чёрный юмор...")

    meme_data = await fetch_meme(DARK_APIS)
    if meme_data:
        title = meme_data.get("title", "")
        url = meme_data.get("url", "")
        text = f"💀 Чёрный юмор:\n\n{title}" if title else "💀 Вот тебе мем:"

        if url.endswith((".jpg", ".jpeg", ".png", ".gif")):
            try:
                await message.answer_photo(url, caption=text)
                return
            except Exception:
                pass

        if url:
            text += f"\n\n🔗 {url}"
        await message.answer(text)
    else:
        await message.answer("💀 Чёрный юмор:\n\nНе удалось загрузить мем, попробуй позже!")


@router.message(Command("quote"))
async def quote(message: types.Message):
    today = datetime.now(timezone.utc).day
    quote_text = QUOTES[today % len(QUOTES)]
    await message.answer(quote_text)
