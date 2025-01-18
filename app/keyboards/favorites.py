from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.constants.favorites import FavoriteButtons

def get_favorite_keyboard(car_id: str, is_favorite: bool) -> InlineKeyboardMarkup:
    """Клавиатура для управления избранным"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=FavoriteButtons.REMOVE if is_favorite else FavoriteButtons.ADD,
                callback_data=f"fav_{car_id}"
            )
        ]]
    ) 