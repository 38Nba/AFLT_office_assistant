from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from database.db import (
    book_seat,
    cancel_booking,
    get_bookings_by_user,
    get_seat_map
)
from services.image_map import generate_office_map
from ai.gpt_assistant import ask_gpt

router = Router()

@router.message(Command("book"))
async def book(message: Message):
    parts = message.text.strip().split()

    if len(parts) < 3:
        await message.answer("❗ Пожалуйста, укажи место и дату. Пример: /book A3 2025-07-30")
        return

    seat = parts[1].upper()
    date = parts[2]

    response = book_seat(message.from_user.id, seat, date)
    await message.reply(response)

@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    args = message.text.replace("/cancel", "").strip().split()
    if len(args) < 2:
        await message.reply("Укажи место и дату, например: /cancel A1 2025-07-30")
        return
    seat, date = args[0], args[1]
    response = cancel_booking(message.from_user.id, seat, date)
    await message.reply(response)

@router.message(Command("mybookings"))
async def cmd_mybookings(message: Message):
    result = get_bookings_by_user(message.from_user.id)
    await message.reply(result)

@router.message(Command("map"))
async def cmd_map(message: Message):
    img_path = generate_office_map()
    await message.answer_photo(FSInputFile(img_path))

@router.message(Command("ai"))
async def cmd_ai(message: Message):
    if not message.text:
        await message.reply("Пожалуйста, отправь вопрос после команды, например:\n`/ai кто будет в офисе в пятницу?`")
        return

    user_question = message.text.replace("/ai", "", 1).strip()
    if not user_question:
        await message.reply("Напиши вопрос после команды, например:\n`/ai кто будет в офисе в пятницу?`")
        return

    response = ask_gpt(user_question, user_id=message.from_user.id)

    if isinstance(response, dict) and response.get("type") == "image":
        await message.answer_photo(FSInputFile(response["path"]))
    else:
        await message.reply(response)

@router.message(Command("aihelp"))
async def cmd_aihelp(message: Message):
    await message.answer(
        "💡 Я умею помогать:"
        "- Забронировать место: 'забронируй место A1 в пятницу'\n"
        "- Отменить бронирование: 'отмени место A1 2025-08-01'\n"
        "- Показать схему мест: 'покажи схему мест на понедельник'\n"
        "- Узнать кто будет в офисе: 'кто будет в офисе в среду'\n\n"
        "Форматы дат: 'в понедельник', 'завтра', '2025-08-01'\n"
        "Место можно писать кириллицей или латиницей (А1 / A1 — это одно и то же)"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 Возможности AI", callback_data="aihelp")],
            [InlineKeyboardButton(text="📍 Схема мест", callback_data="map")],
            [InlineKeyboardButton(text="📅 Мои бронирования", callback_data="mybookings")],
        ]
    )
    await message.answer("Выбери, с чем тебе помочь:", reply_markup=kb)