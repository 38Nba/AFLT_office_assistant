from datetime import datetime, timedelta
import re

WEEKDAYS = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресенье": 6,
}

PREPOSITIONS = ["в", "на", "по", "во"]

def parse_human_date(text: str) -> str | None:
    text = text.strip().lower()

    # Убираем предлоги перед днями недели
    for prep in PREPOSITIONS:
        if text.startswith(prep + " "):
            text = text[len(prep) + 1:]
            break

    # Обработка ключевых слов
    if text in ["сегодня"]:
        return datetime.now().strftime("%Y-%m-%d")
    if text in ["завтра"]:
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if text in ["послезавтра"]:
        return (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

    # Обработка даты в формате YYYY-MM-DD
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Обработка дня недели
    if text in WEEKDAYS:
        today = datetime.now()
        target_weekday = WEEKDAYS[text]
        days_ahead = (target_weekday - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7  # следующий понедельник, если сегодня понедельник
        target_date = today + timedelta(days=days_ahead)
        return target_date.strftime("%Y-%m-%d")

    return None
