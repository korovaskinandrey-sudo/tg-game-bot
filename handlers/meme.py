import random
import aiohttp
from datetime import datetime, timezone
from aiogram import Router, types
from aiogram.filters import Command
from io import BytesIO

router = Router()

MEME_SOURCES = [
    "https://meme-api.com/gimme",
    "https://meme-api.com/gimme/memes",
    "https://meme-api.com/gimme/dankmemes",
]

DARK_SOURCES = [
    "https://meme-api.com/gimme/darkmemes",
    "https://meme-api.com/gimme/DarkHumorAndMemes",
    "https://meme-api.com/gimme/meanjokes",
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


async def download_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    if len(data) > 1000:
                        return data
    except Exception:
        pass
    return None


async def get_meme(sources):
    for api_url in sources:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        img_url = data.get("url", "")
                        title = data.get("title", "")

                        if img_url and img_url.endswith((".jpg", ".jpeg", ".png", ".gif")):
                            img_data = await download_image(img_url)
                            if img_data:
                                return title, img_data

                        if img_url and "reddit.com" not in img_url:
                            img_data = await download_image(img_url)
                            if img_data:
                                return title, img_data
        except Exception:
            continue
    return None, None


@router.message(Command("meme"))
async def meme(message: types.Message):
    await message.answer("🔍 Ищу мем...")

    title, img_data = await get_meme(MEME_SOURCES)
    if img_data:
        photo = BytesIO(img_data)
        photo.name = "meme.jpg"
        caption = f"🤣 {title}" if title else "🤣 Мем"
        await message.answer_photo(photo, caption=caption)
    else:
        await message.answer("🤣 Мем загрузить не удалось, попробуй позже!")


@router.message(Command("dark"))
async def dark(message: types.Message):
    await message.answer("🔍 Ищу чёрный юмор...")

    title, img_data = await get_meme(DARK_SOURCES)
    if img_data:
        photo = BytesIO(img_data)
        photo.name = "dark.jpg"
        caption = f"💀 {title}" if title else "💀 Чёрный юмор"
        await message.answer_photo(photo, caption=caption)
    else:
        await message.answer("💀 Чёрный юмор загрузить не удалось, попробуй позже!")


@router.message(Command("quote"))
async def quote(message: types.Message):
    today = datetime.now(timezone.utc).day
    quote_text = QUOTES[today % len(QUOTES)]
    await message.answer(quote_text)
