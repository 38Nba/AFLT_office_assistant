import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers.commands import router as command_router
from routes.start_routes import router as start_router
from database.db import init_db

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключаем все роутеры
dp.include_router(command_router)
dp.include_router(start_router)

async def main():
    init_db()

    try:
        print("✅ Бот запущен. Нажмите Ctrl+C для остановки.")
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Бот остановлен пользователем.")
    finally:
        await bot.session.close()
        print("🔁 Сессия бота закрыта корректно.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Программа остановлена вручную.")