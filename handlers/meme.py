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


async def fetch_meme(subreddit="memes"):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://www.reddit.com/r/{subreddit}/random.json?limit=1"
            headers = {"User-Agent": "TelegramBot/1.0"}
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and data[0]["data"]["children"]:
                        post = data[0]["data"]["children"][0]["data"]
                        return {
                            "title": post.get("title", ""),
                            "url": post.get("url", ""),
                            "permalink": f"https://reddit.com{post.get('permalink', '')}",
                        }
    except Exception:
        pass
    return None


@router.message(Command("meme"))
async def meme(message: types.Message):
    await message.answer("🔍 Ищу мем...")

    meme_data = await fetch_meme("memes")
    if meme_data and meme_data["url"]:
        text = f"🤣 Мем дня:\n\n{meme_data['title']}"
        if meme_data["url"].endswith((".jpg", ".jpeg", ".png", ".gif")):
            await message.answer_photo(meme_data["url"], caption=text)
        else:
            text += f"\n\n🔗 {meme_data['permalink']}"
            await message.answer(text)
    else:
        await message.answer("🤣 Мем дня:\n\nНе удалось загрузить мем, попробуй позже!")


@router.message(Command("dark"))
async def dark(message: types.Message):
    await message.answer("🔍 Ищу чёрный юмор...")

    meme_data = await fetch_meme("dankmemes")
    if not meme_data:
        meme_data = await fetch_meme("DarkHumorAndMemes")
    if meme_data and meme_data["url"]:
        text = f"💀 Чёрный юмор:\n\n{meme_data['title']}"
        if meme_data["url"].endswith((".jpg", ".jpeg", ".png", ".gif")):
            await message.answer_photo(meme_data["url"], caption=text)
        else:
            text += f"\n\n🔗 {meme_data['permalink']}"
            await message.answer(text)
    else:
        await message.answer("💀 Чёрный юмор:\n\nНе удалось загрузить мем, попробуй позже!")


@router.message(Command("quote"))
async def quote(message: types.Message):
    today = datetime.now(timezone.utc).day
    quote_text = QUOTES[today % len(QUOTES)]
    await message.answer(quote_text)
