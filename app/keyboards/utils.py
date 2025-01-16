from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_inline_keyboard(buttons: List[List[Tuple[str, str]]]) -> InlineKeyboardMarkup:
    """
    Создает inline клавиатуру из списка кнопок
    
    Args:
        buttons: Список строк кнопок в формате [(text, callback_data), ...]
    """
    keyboard = [
        [InlineKeyboardButton(text=text, callback_data=data) for text, data in row]
        for row in buttons
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)