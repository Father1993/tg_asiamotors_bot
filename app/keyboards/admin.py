from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура админ-панели"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💱 Редактировать курсы валют",
                callback_data="edit_currency"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_currency_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора валюты для редактирования"""
    keyboard = [
        [
            InlineKeyboardButton(text="🇨🇳 CNY (Юань)", callback_data="CNY"),
            InlineKeyboardButton(text="🇪🇺 EUR (Евро)", callback_data="EUR")
        ],
        [
            InlineKeyboardButton(text="« Назад", callback_data="admin")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 