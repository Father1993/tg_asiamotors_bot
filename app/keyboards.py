from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.config import KeyboardButtons as kb
from app.constants.faq import faq_data

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    keyboard = [
        [KeyboardButton(text=kb.CATALOG), KeyboardButton(text=kb.SELECT_CAR)],
        [KeyboardButton(text=kb.CALCULATOR), KeyboardButton(text=kb.FAVORITES)],
        [KeyboardButton(text=kb.NOTIFICATIONS), KeyboardButton(text=kb.SURVEY)],
        [KeyboardButton(text=kb.SUPPORT), KeyboardButton(text=kb.FAQ)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_faq_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура FAQ"""
    keyboard = []
    # Добавляем все вопросы
    for key, data in faq_data.items():
        keyboard.append([
            InlineKeyboardButton(
                text=data['question'],
                callback_data=f'faq_{key}'
            )
        ])
    
    # Добавляем кнопку возврата
    keyboard.append([
        InlineKeyboardButton(
            text="🏠 Вернуться в главное меню",
            callback_data="start"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_faq_answer_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для ответа FAQ"""
    keyboard = [
        [InlineKeyboardButton(text="◀️ Назад к FAQ", callback_data="faq")],
        [InlineKeyboardButton(text="🏠 Вернуться в главное меню", callback_data="start")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 