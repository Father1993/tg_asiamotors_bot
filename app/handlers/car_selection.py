from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

from app.keyboards.base import KeyboardButtons as kb
from app.keyboards import (
    get_main_keyboard,
    get_lifestyle_keyboard,
    get_budget_keyboard,
    get_passengers_keyboard,
    get_usage_keyboard,
    get_priorities_keyboard
)
from app.constants.car_selection import SelectionMessages as msgs, SelectionOptions
from app.services.car_selector import CarSelector
from app.config import WEBSITE_URL

logger = logging.getLogger(__name__)
router = Router()
car_selector = CarSelector()

class CarSelectionStates(StatesGroup):
    """Состояния FSM для подбора автомобиля"""
    WAITING_LIFESTYLE = State()
    WAITING_BUDGET = State()
    WAITING_PASSENGERS = State()
    WAITING_USAGE = State()
    WAITING_PRIORITIES = State()

@router.message(F.text == kb.SELECT_CAR)
async def show_car_selection(message: Message, state: FSMContext):
    """Начало процесса подбора автомобиля"""
    await state.set_state(CarSelectionStates.WAITING_LIFESTYLE)
    await message.answer(msgs.WELCOME, reply_markup=get_lifestyle_keyboard())

@router.message(CarSelectionStates.WAITING_LIFESTYLE)
async def process_lifestyle(message: Message, state: FSMContext):
    """Обработка выбора образа жизни"""
    if message.text not in SelectionOptions.LIFESTYLES:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов")
        return
    
    await state.update_data(lifestyle=message.text)
    await state.set_state(CarSelectionStates.WAITING_BUDGET)
    await message.answer(msgs.BUDGET_QUESTION, reply_markup=get_budget_keyboard())

@router.message(CarSelectionStates.WAITING_BUDGET)
async def process_budget(message: Message, state: FSMContext):
    """Обработка выбора бюджета"""
    if message.text not in SelectionOptions.BUDGETS:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов")
        return
    
    await state.update_data(budget=message.text)
    await state.set_state(CarSelectionStates.WAITING_PASSENGERS)
    await message.answer(msgs.PASSENGERS_QUESTION, reply_markup=get_passengers_keyboard())

@router.message(CarSelectionStates.WAITING_PASSENGERS)
async def process_passengers(message: Message, state: FSMContext):
    """Обработка количества пассажиров"""
    if message.text not in SelectionOptions.PASSENGERS:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов")
        return
    
    await state.update_data(passengers=message.text)
    await state.set_state(CarSelectionStates.WAITING_USAGE)
    await message.answer(msgs.USAGE_QUESTION, reply_markup=get_usage_keyboard())

@router.message(CarSelectionStates.WAITING_USAGE)
async def process_usage(message: Message, state: FSMContext):
    """Обработка типа использования"""
    if message.text not in SelectionOptions.USAGE:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов")
        return
    
    await state.update_data(usage=message.text)
    await state.set_state(CarSelectionStates.WAITING_PRIORITIES)
    await message.answer(msgs.PRIORITIES_QUESTION, reply_markup=get_priorities_keyboard())

@router.message(CarSelectionStates.WAITING_PRIORITIES)
async def process_priorities(message: Message, state: FSMContext):
    """Обработка приоритетов и выдача рекомендаций"""
    if message.text not in SelectionOptions.PRIORITIES:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов")
        return
    
    await state.update_data(priorities=message.text)
    user_data = await state.get_data()
    
    # Получаем рекомендации
    recommendations = car_selector.get_car_recommendations(user_data)
    recommendations_text = car_selector.format_recommendations(recommendations)
    
    # Формируем персонализированное сообщение
    lifestyle_emoji = user_data['lifestyle'].split()[0]
    
    await message.answer(
        msgs.RECOMMENDATIONS_TEMPLATE.format(
            lifestyle_emoji=lifestyle_emoji,
            recommendations=recommendations_text,
            website_url=WEBSITE_URL
        ),
        reply_markup=get_main_keyboard()
    )
    
    await state.clear()

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков подбора автомобиля"""
    dp.include_router(router)