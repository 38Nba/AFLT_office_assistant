from datetime import datetime, timedelta
import re

WEEKDAYS = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресенье": 6
}

SPECIAL_DAYS = {
    "сегодня": 0,
    "завтра": 1,
    "послезавтра": 2
}


def parse_human_date(text: str) -> str | None:
    text = text.lower().strip()
    today = datetime.today()

    # 1. Специальные дни
    for key, offset in SPECIAL_DAYS.items():
        if key in text:
            return (today + timedelta(days=offset)).strftime("%Y-%m-%d")

    # 2. День недели: "в понедельник", "в пятницу"
    for name, index in WEEKDAYS.items():
        if f"в {name}" in text:
            days_ahead = (index - today.weekday() + 7) % 7
            days_ahead = days_ahead or 7
            return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    # 3. Следующий день недели: "в следующий понедельник"
    for name, index in WEEKDAYS.items():
        if f"в следующий {name}" in text:
            days_ahead = (index - today.weekday() + 7) % 7 + 7
            return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    # 4. "на следующей неделе" — по умолчанию понедельник
    if "на следующей неделе" in text:
        next_monday = today + timedelta(days=(7 - today.weekday()) % 7 + 0)
        return next_monday.strftime("%Y-%m-%d")

    # 5. "через N дней"
    match = re.search(r"через\s+(\d+)\s+д(ень|ня|ней)", text)
    if match:
        days = int(match.group(1))
        return (today + timedelta(days=days)).strftime("%Y-%m-%d")

    # 6. ISO-формат: 2025-08-01
    match = re.search(r"\d{4}-\d{2}-\d{2}", text)
    if match:
        try:
            dt = datetime.strptime(match.group(), "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return None

    return None