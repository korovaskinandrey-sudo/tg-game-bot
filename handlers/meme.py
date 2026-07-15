import random
import urllib.parse
from datetime import datetime, timezone
from aiogram import Router, types
from aiogram.filters import Command
from io import BytesIO
import aiohttp

router = Router()

TEMPLATES = [
    "drake", "dsb", "buzz", "doge", "cmm",
    "afraid", "awkward", "cheems", "expanding",
    "panik", "kbd", "stewart", "rollsafe",
    "left", "two-buttons", "uno", "change",
    "iapologize", "bernice", "trump",
]

MEME_TEXTS = [
    ("Когда все в топе", "А ты Last"),
    ("Давай мини-игру", "У нас уже есть /slots"),
    ("Я: Давай в Repo", "Тиммейт: /slots"),
    ("Когда забыл /daily", "И потерял серию"),
    ("Когда сделал /bet", "И проиграл всё"),
    ("Когда бот упал", "А ты не знаешь команд"),
    ("Когда написал 100 сообщений", "А XP = 0"),
    ("Когда серия 7 дней", "И бонус 70 XP"),
    ("Когда /poll Кто за", "0 голосов"),
    ("Когда дуэль закончилась", "Ничьей"),
    ("Когда вспомнил что забыл daily", "2 дня подряд"),
    ("Когда тиммейт умер", "От кулачка"),
    ("Когда все онлайн", "А ты один в лобби"),
    ("Когда бот пишет не удалось", "Загрузить мем"),
    ("КогдаLegenda", "1000 XP"),
    ("Когда сделал /ban", "А потом вспомнил что это ты"),
    ("Когда бот это единственный друг", "Грустно"),
    ("Когда серия 30 дней", "А бот забыл"),
    ("Когда /unban не работает", "Помогите"),
    ("Когда понял что жизнь это бесконечный daily", ""),
]

DARK_TEXTS = [
    ("Когда понял что жизнь", "Это бесконечный daily"),
    ("Когда забыл daily 2 дня", "Серия = 0, мотивация = 0"),
    ("Когда сделал /bet", "И проиграл всё"),
    ("Когда бот пишет Ты уже получил", "А ты хотел ещё"),
    ("Когда напоминание в 3 часа ночи", "Спасибо боту"),
    ("Когда все в топе а ты последний", "Зато ты в топе по сообщениям"),
    ("Когда бот упал", "Добро пожаловать в ад"),
    ("Когда забыл пароль", "Ха-ха"),
    ("Когда 0 голосов", "Одинокий голосование"),
    ("Когда бот не может загрузить мем", "Ты тоже не можешь"),
    ("Когда 100 сообщений XP = 0", "Ты просто говорливый"),
    ("Когда дуэль ничья", "Два проигравших"),
    ("Когда понял что бот это друг", "Грустно"),
    ("Когда сам себя забанил", "Ой"),
    ("Когда серия 30 дней а бот забыл", "Пора менять бота"),
    ("Когда дуэль", "Ничья"),
    ("Когда бот это единственный друг", ""),
    ("Когда забыл daily 3 дня", "Кто ты теперь"),
    ("Когда бот не работает", "Паника"),
    ("Когда XP отрицательный", "Это возможно?"),
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


async def generate_meme(template, text0, text1):
    try:
        t0 = urllib.parse.quote(text0.replace(" ", "_"))
        t1 = urllib.parse.quote(text1.replace(" ", "_")) if text1 else ""
        url = f"https://api.memegen.link/images/{template}/{t0}/{t1}.jpg"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    return await resp.read()
    except Exception:
        pass
    return None


@router.message(Command("meme"))
async def meme(message: types.Message):
    await message.answer("🤣 Генерирую мем...")

    template = random.choice(TEMPLATES)
    text0, text1 = random.choice(MEME_TEXTS)

    img_data = await generate_meme(template, text0, text1)
    if img_data:
        photo = BytesIO(img_data)
        photo.name = "meme.jpg"
        await message.answer_photo(photo)
    else:
        await message.answer("🤣 Не удалось сгенерировать мем, попробуй позже!")


@router.message(Command("dark"))
async def dark(message: types.Message):
    await message.answer("💀 Генерирую чёрный юмор...")

    template = random.choice(TEMPLATES)
    text0, text1 = random.choice(DARK_TEXTS)

    img_data = await generate_meme(template, text0, text1)
    if img_data:
        photo = BytesIO(img_data)
        photo.name = "dark.jpg"
        await message.answer_photo(photo)
    else:
        await message.answer("💀 Не удалось сгенерировать мем, попробуй позже!")


@router.message(Command("quote"))
async def quote(message: types.Message):
    today = datetime.now(timezone.utc).day
    quote_text = QUOTES[today % len(QUOTES)]
    await message.answer(quote_text)
