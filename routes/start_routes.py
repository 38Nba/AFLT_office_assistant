from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from services.image_map import generate_office_map
from ai.gpt_assistant import ask_gpt
from database.db import save_user  # ✅ импорт сохранения пользователя

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    # ✅ Сохраняем пользователя в БД
    save_user(user_id=message.from_user.id, username=message.from_user.username)

    await message.answer(
        "Привет! Я твой личный ассистент по бронированию мест в офисе 🧠\n"
        "Я могу помочь с такими вещами как: \n"
        "- Кто будет в офисе\n"
        "- Какой день выбрать\n"
        "- Вопросы по команде, встречам и т.д.\n"
        "- Покажу схему мест\n"
        "- Забронирую или отменю бронирование\n"
        
        "Вот актуальная схема мест:"
    )
    image_path = generate_office_map()
    await message.answer_photo(FSInputFile(image_path))


@router.message(Command("aihelp"))
async def cmd_aihelp(message: Message):
    await message.answer(
        "🧾 Возможности чат-бота:\n\n"
        "📌 Команды:\n"
        "/start — начать работу и показать схему офиса\n"
        "/book A1 2025-08-01 — забронировать место\n"
        "/cancel A1 2025-08-01 — отменить бронь\n"
        "/mybookings — список ваших бронирований\n"
        "/map — схема мест на сегодня\n"
        "/ai [вопрос] — задать вопрос или получить помощь от ИИ\n"
        "🤖 Я также понимаю обычные фразы, например:\n"
        "— «забронируй место B2 завтра»\n"
        "— «кто будет в офисе в пятницу»\n"
        "— «покажи занятые места на 2025-08-12»"
    )