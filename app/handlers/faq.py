import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.config import KeyboardButtons as kb
from app.keyboards import get_faq_keyboard, get_main_keyboard, get_faq_answer_keyboard
from app.constants.faq import faq_data

# Настройка логгера
logger = logging.getLogger(__name__)

router = Router()

@router.message(F.text == kb.FAQ)
@router.callback_query(F.data == "faq")
async def show_faq(event: Message | CallbackQuery, state: FSMContext):
    """Показать FAQ"""
    text = "❓ Часто задаваемые вопросы\n\nВыберите интересующий вас вопрос:"
    
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.edit_text(text, reply_markup=get_faq_keyboard())
    else:
        await event.answer(text, reply_markup=get_faq_keyboard())

@router.callback_query(F.data.startswith("faq_"))
async def show_faq_answer(callback: CallbackQuery, state: FSMContext):
    """Показ ответа на конкретный вопрос FAQ"""
    try:
        # Получаем ключ вопроса из callback_data
        # Берем всю строку после 'faq_'
        faq_key = callback.data[4:]  # пропускаем 'faq_' и берем весь остаток
        logger.info(f"Full callback data: {callback.data}")
        logger.info(f"Extracted key: {faq_key}")
        logger.info(f"Available keys: {list(faq_data.keys())}")
        
        if faq_key in faq_data:
            # Формируем текст ответа
            text = (
                f"❓ {faq_data[faq_key]['question']}\n\n"
                f"📝 {faq_data[faq_key]['answer']}"
            )
            
            # Отправляем ответ
            await callback.message.edit_text(
                text,
                reply_markup=get_faq_answer_keyboard()
            )
        else:
            logger.warning(f"FAQ key not found: {faq_key}")
            await callback.answer(
                "Вопрос не найден. Пожалуйста, выберите другой вопрос.",
                show_alert=True
            )
            
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Error in FAQ answer: {e}")
        await callback.answer(
            "Произошла ошибка. Попробуйте еще раз.",
            show_alert=True
        )

@router.callback_query(F.data == "start")
async def handle_start(callback: CallbackQuery, state: FSMContext):
    """Обработка возврата в главное меню"""
    await callback.message.delete()
    await callback.message.answer(
        "Выберите нужный раздел:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков FAQ"""
    dp.include_router(router) 