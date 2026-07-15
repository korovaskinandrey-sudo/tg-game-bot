TOKEN = "8913865659:AAE8FB4RRyCId5qbLloY4w98Zye7zvHQACs"

PROXY_URL = "socks5://185.204.168.242:1080"

XP_PER_MESSAGE = 10
XP_COOLDOWN_SECONDS = 60

LEVELS = {
    "Новичок": 0,
    "Игрок": 100,
    "Про": 500,
    "Легенда": 1000,
}

def get_level(xp):
    level_name = "Новичок"
    for name, required_xp in sorted(LEVELS.items(), key=lambda x: x[1], reverse=True):
        if xp >= required_xp:
            level_name = name
            break
    return level_name
