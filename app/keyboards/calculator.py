from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.keyboards.base import KeyboardButtons as kb

def get_calculator_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для калькулятора с результатом"""
    keyboard = [
        [KeyboardButton(text=kb.CALCULATE_MORE)],
        [KeyboardButton(text=kb.MAIN_MENU)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_price_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для ввода цены"""
    keyboard = [
        [KeyboardButton(text=kb.MAIN_MENU)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_year_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора года"""
    current_years = [str(2024 - i) for i in range(5)]  # Последние 5 лет
    keyboard = [
        [KeyboardButton(text=year) for year in current_years[:2]],
        [KeyboardButton(text=year) for year in current_years[2:4]],
        [KeyboardButton(text=current_years[4])],
        [KeyboardButton(text=kb.MAIN_MENU)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_engine_volume_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора объема двигателя"""
    volumes = ['1500', '1600', '2000', '2500', '3000']
    keyboard = [
        [KeyboardButton(text=volumes[0]), KeyboardButton(text=volumes[1])],
        [KeyboardButton(text=volumes[2]), KeyboardButton(text=volumes[3])],
        [KeyboardButton(text=volumes[4])],
        [KeyboardButton(text=kb.MAIN_MENU)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_power_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора мощности двигателя"""
    powers = ['100', '150', '200', '250', '300']
    keyboard = [
        [KeyboardButton(text=powers[0]), KeyboardButton(text=powers[1])],
        [KeyboardButton(text=powers[2]), KeyboardButton(text=powers[3])],
        [KeyboardButton(text=powers[4])],
        [KeyboardButton(text=kb.MAIN_MENU)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
