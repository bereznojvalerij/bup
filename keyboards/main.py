from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💨 Пук", callback_data="fart")],
        [InlineKeyboardButton(text="📊 День", callback_data="day"),
         InlineKeyboardButton(text="📊 Неделя", callback_data="week")],
        [InlineKeyboardButton(text="📊 Месяц", callback_data="month"),
         InlineKeyboardButton(text="📊 Всё время", callback_data="all")],
        [InlineKeyboardButton(text="🏆 Рейтинг", callback_data="rating")]
    ])


def fart_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="+1", callback_data="fart_1"),
         InlineKeyboardButton(text="+2", callback_data="fart_2"),
         InlineKeyboardButton(text="+3", callback_data="fart_3")],
        [InlineKeyboardButton(text="+4", callback_data="fart_4"),
         InlineKeyboardButton(text="+5", callback_data="fart_5"),
         InlineKeyboardButton(text="+6", callback_data="fart_6")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])