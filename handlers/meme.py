import random
from datetime import datetime, timezone
from aiogram import Router, types
from aiogram.filters import Command
from io import BytesIO
import aiohttp

router = Router()

MEME_TEMPLATES = [
    (61580, "Два кукловода"),  # Drake
    (101470, "Сцена из фильма"),  # Disaster Girl
    (87743020, "Три кнопки"),  # Three Buttons
    (438680, "Batman Slapping Robin"),  # Batman
    (181913649, "Drake Hotline Bling"),  # Drake
    (93895088, "Expanding Brain"),  # Expanding Brain
    (112126428, "Distracted Boyfriend"),  # Distracted Boyfriend
    (61585, "Burn Kermit"),  # Kermit
    (222403160, "Bernie I Am Once Again"),  # Bernie
    (135256802, "Epic Handshake"),  # Epic Handshake
    (247375501, "Buff Doge vs Cheems"),  # Buff Doge
    (4087833, "Waiting Skeleton"),  # Waiting
    (91538330, "X, X Everywhere"),  # X
    (61520, "Futurama Fry"),  # Fry
    (101287, "Third World Skeptical Kid"),  # Skeptical
]

MEME_TEXTS = [
    ("Когда все в топе\nА ты>Last", "Но зато у тебя есть /daily"),
    ("Давай мини-игру", "У нас уже есть /slots"),
    ("Я: Давай в Repo\nТиммейт: /slots", ""),
    ("Когда забыл /daily\nИ потерял серию", "Но зато вспомнил вовремя"),
    ("Когда сделал /bet\nИ проиграл всё", "Но зато получил опыт"),
    ("Когда бот упал\nА ты не знаешь команд", "Жди пока Railway задеплоит"),
    ("Когда написал 100 сообщений\nА XP = 0", "Зато есть сообщения в топе"),
    ("Когда серия 7 дней\nИ бонус 70 XP", "Это лучше чем /slots"),
    ("Когда /poll: Кто за?\n0 голосов", "Зато есть ты"),
    ("Когда дуэль закончилась\nНичьей", "XP не забирается"),
    ("Когда вспомнил что забыл\n/daily 2 дня подряд", "Серия = 0"),
    ("Когда бот пишет\n'не удалось загрузить мем'", "Но вот тебе текстовый"),
    ("Когда тиммейт умер\nОт кулачка", "Респект тиммейту"),
    ("Когда все онлайн\nА ты один в лобби", "Зато есть бот"),
    ("Когда /ban а потом\nВспомнил что это ты", "Ой"),
]

DARK_TEXTS = [
    ("Когда понял что жизнь\nЭто просто бесконечный /daily", ""),
    ("Когда забыл /daily\n2 дня подряд", "Серия = 0, мотивация = 0"),
    ("Когда сделал /bet\nИ проиграл всё", "Зато теперь не надо думать"),
    ("Когда бот пишет\n'Ты уже получил бонус'", "А ты хотел ещё"),
    ("Когда напоминание приходит\nВ 3 часа ночи", "Спасибо боту"),
    ("Когда все в топе\nА ты последний", "Зато ты в топе... по сообщениям"),
    ("Когда бот упал\nА ты не знаешь команд", "Добро пожаловать в ад"),
    ("Когда забыл пароль\nОт аккаунта", "Ха-ха"),
    ("Когда /poll: Кто за?\n0 голосов", "Одинокий голосование"),
    ("Когда бот пишет\n'не удалось загрузить мем'", "Ты тоже не можешь"),
    ("Когда написал 100 сообщений\nА XP = 0", "Ты просто говорливый"),
    ("Когда дуэль закончилась\nНичьей", "Два проигравших"),
    ("Когда понял что бот\nЭто единственный друг", "Грустно"),
    ("Когда сделал /ban\nА потом вспомнил что это ты", "Сам себя забанил"),
    ("Когда серия 30 дней\nА бот забыл", "Пора менять бота"),
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


async def create_meme(template_id, text0, text1):
    try:
        async with aiohttp.ClientSession() as session:
            data = {
                "template_id": template_id,
                "username": "TgGameBot",
                "password": "TgGameBot123",
                "text0": text0,
                "text1": text1,
            }
            async with session.post(
                "https://api.imgflip.com/caption_image",
                data=data,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    if result.get("success"):
                        url = result["data"]["url"]
                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as img_resp:
                            if img_resp.status == 200:
                                return await img_resp.read()
    except Exception:
        pass
    return None


@router.message(Command("meme"))
async def meme(message: types.Message):
    await message.answer("🤣 Генерирую мем...")

    template_id, _ = random.choice(MEME_TEMPLATES)
    text0, text1 = random.choice(MEME_TEXTS)

    img_data = await create_meme(template_id, text0, text1)
    if img_data:
        photo = BytesIO(img_data)
        photo.name = "meme.jpg"
        await message.answer_photo(photo)
    else:
        await message.answer("🤣 Не удалось сгенерировать мем, попробуй позже!")


@router.message(Command("dark"))
async def dark(message: types.Message):
    await message.answer("💀 Генерирую чёрный юмор...")

    template_id, _ = random.choice(MEME_TEMPLATES)
    text0, text1 = random.choice(DARK_TEXTS)

    img_data = await create_meme(template_id, text0, text1)
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
