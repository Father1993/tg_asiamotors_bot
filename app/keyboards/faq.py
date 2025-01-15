from aiogram.types import InlineKeyboardMarkup
from app.constants.faq import faq_data
from .utils import create_inline_keyboard

def get_faq_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура FAQ"""
    buttons = [
        [(data['question'], f'faq_{key}')]
        for key, data in faq_data.items()
    ]
    # Добавляем кнопку возврата
    buttons.append([("🏠 Вернуться в главное меню", "start")])
    
    return create_inline_keyboard(buttons)

def get_faq_answer_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для ответа FAQ"""
    buttons = [
        [("◀️ Назад к FAQ", "faq")],
        [("🏠 Вернуться в главное меню", "start")]
    ]
    return create_inline_keyboard(buttons)