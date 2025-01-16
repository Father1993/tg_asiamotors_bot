from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from app.keyboards.base import KeyboardButtons as kb
from app.keyboards import get_main_keyboard
from app.config import ADMIN_IDS
from app.constants.support import SupportMessages as msgs, AdminMessages as admin_msgs
from app.utils.validators import validate_phone

logger = logging.getLogger(__name__)
router = Router()

class SupportStates(StatesGroup):
    """Состояния FSM для обработки обращения в поддержку"""
    WAITING_NAME = State()
    WAITING_PHONE = State()
    WAITING_QUESTION = State()

async def send_admin_notification(message: Message, support_data: dict) -> None:
    """
    Отправка уведомления администраторам о новом обращении
    
    Args:
        message: Объект сообщения
        support_data: Данные обращения в поддержку
    """
    admin_message = admin_msgs.NEW_REQUEST.format(
        name=support_data['name'],
        phone=support_data['phone'],
        question=support_data['question'],
        user_id=message.from_user.id,
        username=message.from_user.username or 'Отсутствует'
    )
    
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_message)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления админу {admin_id}: {e}")

@router.message(F.text == kb.SUPPORT)
async def show_support(message: Message, state: FSMContext):
    """Начало диалога с поддержкой"""
    await state.set_state(SupportStates.WAITING_NAME)
    await message.answer(msgs.WELCOME)

@router.message(SupportStates.WAITING_NAME)
async def process_name(message: Message, state: FSMContext):
    """Обработка имени"""
    await state.update_data(name=message.text)
    await state.set_state(SupportStates.WAITING_PHONE)
    await message.answer(msgs.PHONE_REQUEST)

@router.message(SupportStates.WAITING_PHONE)
async def process_phone(message: Message, state: FSMContext):
    """Обработка телефона"""
    if not await validate_phone(message.text):
        await message.answer(msgs.INVALID_PHONE)
        return

    await state.update_data(phone=message.text)
    await state.set_state(SupportStates.WAITING_QUESTION)
    await message.answer(msgs.QUESTION_REQUEST)

@router.message(SupportStates.WAITING_QUESTION)
async def process_question(message: Message, state: FSMContext):
    """Обработка вопроса и завершение диалога"""
    await state.update_data(question=message.text)
    
    # Получаем все данные
    support_data = await state.get_data()
    
    # Отправляем уведомление админам
    await send_admin_notification(message, support_data)
    
    # Отправляем подтверждение пользователю
    await message.answer(
        msgs.COMPLETION.format(name=support_data['name']),
        reply_markup=get_main_keyboard()
    )
    
    # Очищаем состояние
    await state.clear()

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков поддержки"""
    dp.include_router(router)