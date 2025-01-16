from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.config import KeyboardButtons as kb

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    buttons = [
        [kb.CATALOG, kb.SELECT_CAR],
        [kb.CALCULATOR, kb.FAVORITES],
        [kb.NOTIFICATIONS, kb.SURVEY],
        [kb.SUPPORT, kb.FAQ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in buttons],
        resize_keyboard=True
    )