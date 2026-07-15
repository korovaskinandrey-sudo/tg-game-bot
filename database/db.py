import os
import aiosqlite

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.db")


class Database:
    def __init__(self):
        self.db = None

    async def connect(self):
        self.db = await aiosqlite.connect(DB_PATH)
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                chat_id INTEGER,
                xp INTEGER DEFAULT 0,
                messages INTEGER DEFAULT 0,
                last_xp_time REAL DEFAULT 0,
                PRIMARY KEY (user_id, chat_id)
            )
        """)
        await self.db.commit()

    async def close(self):
        if self.db:
            await self.db.close()

    async def count_message(self, user_id, chat_id):
        cursor = await self.db.execute(
            "SELECT 1 FROM users WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id),
        )
        row = await cursor.fetchone()
        if row is None:
            await self.db.execute(
                "INSERT INTO users (user_id, chat_id, xp, messages) VALUES (?, ?, 0, 1)",
                (user_id, chat_id),
            )
        else:
            await self.db.execute(
                "UPDATE users SET messages = messages + 1 WHERE user_id = ? AND chat_id = ?",
                (user_id, chat_id),
            )
        await self.db.commit()

    async def add_xp(self, user_id, chat_id, xp, current_time):
        cursor = await self.db.execute(
            "SELECT last_xp_time FROM users WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id),
        )
        row = await cursor.fetchone()

        if row is None:
            await self.db.execute(
                "INSERT INTO users (user_id, chat_id, xp, messages, last_xp_time) VALUES (?, ?, ?, 1, ?)",
                (user_id, chat_id, xp, current_time),
            )
        else:
            await self.db.execute(
                "UPDATE users SET xp = xp + ?, messages = messages + 1, last_xp_time = ? WHERE user_id = ? AND chat_id = ?",
                (xp, current_time, user_id, chat_id),
            )
        await self.db.commit()

    async def get_user(self, user_id, chat_id):
        cursor = await self.db.execute(
            "SELECT xp, messages, last_xp_time FROM users WHERE user_id = ? AND chat_id = ?",
            (user_id, chat_id),
        )
        return await cursor.fetchone()

    async def get_top(self, chat_id, limit=10):
        cursor = await self.db.execute(
            "SELECT user_id, xp, messages FROM users WHERE chat_id = ? ORDER BY xp DESC LIMIT ?",
            (chat_id, limit),
        )
        return await cursor.fetchall()
