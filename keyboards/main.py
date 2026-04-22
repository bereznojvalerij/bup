from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    kb = [
        [KeyboardButton(text="💨 Пук")],
        [KeyboardButton(text="📊 День"), KeyboardButton(text="📊 Неделя")],
        [KeyboardButton(text="📊 Месяц"), KeyboardButton(text="📊 Всё время")],
        [KeyboardButton(text="🏆 Общий рейтинг")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

def fart_keyboard():
    kb = [
        [KeyboardButton(text="+1"), KeyboardButton(text="+2"), KeyboardButton(text="+3")],
        [KeyboardButton(text="+4"), KeyboardButton(text="+5"), KeyboardButton(text="+6")],
        [KeyboardButton(text="⬅️ Назад")]
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)