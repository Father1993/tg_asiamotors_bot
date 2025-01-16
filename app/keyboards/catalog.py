from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.keyboards.base import KeyboardButtons as kb

class CatalogButtons:
    """Константы для кнопок каталога"""
    CROSSOVER = "Кроссовер"
    SUV = "Джип"
    SEDAN = "Седан"
    WAGON = "Универсал"
    MINIVAN = "Минивен"
    
    FULL_DRIVE = "Полный"
    FRONT_DRIVE = "Передний"
    REAR_DRIVE = "Задний"
    
    PETROL = "Бензин"
    DIESEL = "Дизель"
    HYBRID = "Гибрид"
    ELECTRIC = "Электро"
    
    SHOW_MORE = "Показать еще"
    TO_MAIN_MENU = "В главное меню"

def get_categories_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора категории автомобиля"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=CatalogButtons.CROSSOVER), 
             KeyboardButton(text=CatalogButtons.SUV)],
            [KeyboardButton(text=CatalogButtons.SEDAN), 
             KeyboardButton(text=CatalogButtons.WAGON)],
            [KeyboardButton(text=CatalogButtons.MINIVAN)],
            [KeyboardButton(text=kb.MAIN_MENU)]
        ],
        resize_keyboard=True
    )

def get_drive_types_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора типа привода"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=CatalogButtons.FULL_DRIVE)],
            [KeyboardButton(text=CatalogButtons.FRONT_DRIVE)],
            [KeyboardButton(text=CatalogButtons.REAR_DRIVE)],
            [KeyboardButton(text=kb.MAIN_MENU)]
        ],
        resize_keyboard=True
    )

def get_fuel_types_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора типа топлива"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=CatalogButtons.PETROL), 
             KeyboardButton(text=CatalogButtons.DIESEL)],
            [KeyboardButton(text=CatalogButtons.HYBRID), 
             KeyboardButton(text=CatalogButtons.ELECTRIC)],
            [KeyboardButton(text=kb.MAIN_MENU)]
        ],
        resize_keyboard=True
    )

def get_pagination_keyboard(offset: int) -> InlineKeyboardMarkup:
    """Клавиатура для пагинации"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CatalogButtons.SHOW_MORE, 
                    callback_data=f"show_more_{offset}"
                ),
                InlineKeyboardButton(
                    text=CatalogButtons.TO_MAIN_MENU, 
                    callback_data="to_main_menu"
                )
            ]
        ]
    )

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для возврата в главное меню"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=CatalogButtons.TO_MAIN_MENU, 
                    callback_data="to_main_menu"
                )
            ]
        ]
    )