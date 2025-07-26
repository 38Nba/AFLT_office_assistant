# AFLT Office Assistant Bot

Ассистент для бронирования мест в офисе через Telegram.

## Команды:
- /start — схема офиса
- /book A1 2025-07-30 — забронировать место
- /cancel A1 2025-07-30 — отменить бронь
- /map — актуальная схема
- /mybookings — мои брони
- /ai <вопрос> — ассистент

## Запуск
```
pip install -r requirements.txt
cp .env.example .env
python main.py
```