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