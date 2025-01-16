from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.keyboards.base import KeyboardButtons as kb
from app.constants.car_selection import SelectionOptions

def get_keyboard_from_dict(options: dict) -> list:
    """
    Создает клавиатуру из словаря опций
    
    Args:
        options: Словарь с опциями
        
    Returns:
        list: Список кнопок для клавиатуры
    """
    return [[KeyboardButton(text=option)] for option in options.keys()]

def get_lifestyle_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора образа жизни"""
    keyboard = get_keyboard_from_dict(SelectionOptions.LIFESTYLES)
    keyboard.append([KeyboardButton(text=kb.MAIN_MENU)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_budget_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора бюджета"""
    keyboard = get_keyboard_from_dict(SelectionOptions.BUDGETS)
    keyboard.append([KeyboardButton(text=kb.MAIN_MENU)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_passengers_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора количества пассажиров"""
    keyboard = get_keyboard_from_dict(SelectionOptions.PASSENGERS)
    keyboard.append([KeyboardButton(text=kb.MAIN_MENU)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_usage_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора типа использования"""
    keyboard = get_keyboard_from_dict(SelectionOptions.USAGE)
    keyboard.append([KeyboardButton(text=kb.MAIN_MENU)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_priorities_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора приоритетов"""
    keyboard = get_keyboard_from_dict(SelectionOptions.PRIORITIES)
    keyboard.append([KeyboardButton(text=kb.MAIN_MENU)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)