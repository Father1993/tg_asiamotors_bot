from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import re
from datetime import datetime
import logging

from app.keyboards.base import KeyboardButtons as kb
from app.config import ADMIN_IDS
from app.FSM.survey import SurveyStates
from app.constants.messages import SurveyMessages as msgs
from app.keyboards import (
    get_main_keyboard,
    get_budget_keyboard,
    get_timeframe_keyboard,
    get_features_keyboard,
    get_purpose_keyboard,
    get_current_car_keyboard,
    get_concerns_keyboard,
    get_contact_time_keyboard
)


logger = logging.getLogger(__name__)
router = Router()

async def send_admin_notification(message: Message, survey_data: dict, discount_code: str) -> None:
    """Отправка уведомления администраторам о новом прохождении опроса"""
    admin_message = (
        f"📊 Новый результат опроса!\n\n"
        f"👤 Имя: {survey_data['name']}\n"
        f"📱 Телефон: {survey_data['phone']}\n"
        f"💰 Бюджет: {survey_data['budget']}\n"
        f"🕒 Сроки покупки: {survey_data['timeframe']}\n"
        f"🚗 Текущий автомобиль: {survey_data['current_car']}\n"
        f"⭐️ Важные характеристики: {survey_data['features']}\n"
        f"🎯 Цель использования: {survey_data['purpose']}\n"
        f"❓ Сомнения/вопросы: {survey_data['concerns']}\n"
        f"📞 Удобное время для связи: {survey_data['contact_time']}\n"
        f"🎁 Промокод: {discount_code}"
    )
    
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_message)
        except Exception as e:
            logger.error(f"Ошибка отправки результатов админу {admin_id}: {e}")

def generate_discount_code(user_id: int) -> str:
    """Генерация уникального кода скидки"""
    return f"ASIA{user_id}{datetime.now().strftime('%d%m')}"

async def validate_phone(phone: str) -> bool:
    """Валидация номера телефона"""
    return bool(re.match(r'^\+7\d{10}$', phone))

@router.message(F.text == kb.SURVEY)
async def start_survey(message: Message, state: FSMContext) -> None:
    """Начало опроса"""
    await state.set_state(SurveyStates.WAITING_NAME)
    await message.answer(msgs.WELCOME)

@router.message(SurveyStates.WAITING_NAME)
async def process_name(message: Message, state: FSMContext) -> None:
    """Обработка имени"""
    await state.update_data(name=message.text)
    await state.set_state(SurveyStates.WAITING_PHONE)
    await message.answer(msgs.PHONE_REQUEST)

@router.message(SurveyStates.WAITING_PHONE)
async def process_phone(message: Message, state: FSMContext) -> None:
    """Обработка номера телефона"""
    if not await validate_phone(message.text):
        await message.answer(msgs.INVALID_PHONE)
        return

    await state.update_data(phone=message.text)
    await state.set_state(SurveyStates.WAITING_BUDGET)
    await message.answer(msgs.BUDGET_QUESTION, reply_markup=get_budget_keyboard())

@router.message(SurveyStates.WAITING_BUDGET)
async def process_budget(message: Message, state: FSMContext):
    await state.update_data(budget=message.text)
    await state.set_state(SurveyStates.WAITING_TIMEFRAME)
    await message.answer(msgs.TIMEFRAME_QUESTION, reply_markup=get_timeframe_keyboard())

@router.message(SurveyStates.WAITING_TIMEFRAME)
async def process_timeframe(message: Message, state: FSMContext):
    await state.update_data(timeframe=message.text)
    await state.set_state(SurveyStates.WAITING_CURRENT_CAR)
    await message.answer(msgs.CURRENT_CAR_QUESTION, reply_markup=get_current_car_keyboard())

@router.message(SurveyStates.WAITING_CURRENT_CAR)
async def process_current_car(message: Message, state: FSMContext):
    await state.update_data(current_car=message.text)
    await state.set_state(SurveyStates.WAITING_FEATURES)
    await message.answer(msgs.FEATURES_QUESTION, reply_markup=get_features_keyboard())

@router.message(SurveyStates.WAITING_FEATURES)
async def process_features(message: Message, state: FSMContext):
    await state.update_data(features=message.text)
    await state.set_state(SurveyStates.WAITING_PURPOSE)
    await message.answer(msgs.PURPOSE_QUESTION,reply_markup=get_purpose_keyboard())

@router.message(SurveyStates.WAITING_PURPOSE)
async def process_purpose(message: Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await state.set_state(SurveyStates.WAITING_CONCERNS)
    await message.answer(msgs.CONCERNS_QUESTION, reply_markup= get_concerns_keyboard())

@router.message(SurveyStates.WAITING_CONCERNS)
async def process_concerns(message: Message, state: FSMContext):
    await state.update_data(concerns=message.text)
    await state.set_state(SurveyStates.WAITING_CONTACT_TIME)
    await message.answer(msgs.CONTACT_TIME_QUESTION, reply_markup=get_contact_time_keyboard())

@router.message(SurveyStates.WAITING_CONTACT_TIME)
async def process_contact_time(message: Message, state: FSMContext) -> None:
    """Завершение опроса и отправка результатов"""
    await state.update_data(contact_time=message.text)
    
    survey_data = await state.get_data()
    discount_code = generate_discount_code(message.from_user.id)
    
    await message.answer(
        msgs.SURVEY_COMPLETE.format(
            discount_code=discount_code,
            contact_time=survey_data['contact_time']
        ),
        reply_markup=get_main_keyboard()
    )
    
    await send_admin_notification(message, survey_data, discount_code)
    await state.clear()

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков опроса"""
    dp.include_router(router)