from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import re

from app.keyboards.base import KeyboardButtons as kb, get_main_keyboard
from app.keyboards.calculator import (
    get_calculator_keyboard,
    get_year_keyboard,
    get_engine_volume_keyboard,
    get_power_keyboard,
    get_price_keyboard
)
from app.constants.calculator import CalculatorMessages as msgs
from app.services.calculator import CarCalculator

router = Router()
calculator = CarCalculator()

class CalculatorStates(StatesGroup):
    """Состояния FSM для калькулятора"""
    WAITING_YEAR = State()
    WAITING_PRICE = State()
    WAITING_ENGINE = State()
    WAITING_POWER = State()

def is_valid_year(year: str) -> bool:
    """Проверка корректности года"""
    try:
        year_int = int(year)
        current_year = datetime.now().year
        return 1990 <= year_int <= current_year + 1
    except ValueError:
        return False

def is_valid_number(value: str) -> bool:
    """Проверка, является ли строка положительным числом"""
    try:
        num = float(value)
        return num > 0
    except ValueError:
        return False

async def start_calculation(message: Message, state: FSMContext):
    """Начало процесса расчета"""
    await state.set_state(CalculatorStates.WAITING_YEAR)
    await message.answer(msgs.WELCOME)
    await message.answer(msgs.ENTER_YEAR, reply_markup=get_year_keyboard())

@router.message(F.text == kb.CALCULATOR)
async def show_calculator(message: Message, state: FSMContext):
    """Начало расчета стоимости"""
    await start_calculation(message, state)

@router.message(F.text == kb.CALCULATE_MORE)
async def calculate_more(message: Message, state: FSMContext):
    """Обработка кнопки 'Посчитать ещё'"""
    await start_calculation(message, state)

@router.message(F.text == kb.MAIN_MENU)
async def return_to_main_menu(message: Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()
    await message.answer("Вы вернулись в главное меню", reply_markup=get_main_keyboard())

@router.message(CalculatorStates.WAITING_YEAR)
async def process_year(message: Message, state: FSMContext):
    """Обработка года выпуска"""
    if not is_valid_year(message.text):
        await message.answer(msgs.INVALID_YEAR)
        return
    
    await state.update_data(year=int(message.text))
    await state.set_state(CalculatorStates.WAITING_PRICE)
    await message.answer(msgs.ENTER_PRICE, reply_markup=get_price_keyboard())

@router.message(CalculatorStates.WAITING_PRICE)
async def process_price(message: Message, state: FSMContext):
    """Обработка цены"""
    if not is_valid_number(message.text):
        await message.answer(msgs.INVALID_PRICE)
        return
    
    await state.update_data(price=float(message.text))
    await state.set_state(CalculatorStates.WAITING_ENGINE)
    await message.answer(msgs.ENTER_ENGINE, reply_markup=get_engine_volume_keyboard())

@router.message(CalculatorStates.WAITING_ENGINE)
async def process_engine(message: Message, state: FSMContext):
    """Обработка объема двигателя"""
    if not is_valid_number(message.text):
        await message.answer(msgs.INVALID_ENGINE)
        return
    
    await state.update_data(engine=int(message.text))
    await state.set_state(CalculatorStates.WAITING_POWER)
    await message.answer(msgs.ENTER_POWER, reply_markup=get_power_keyboard())

@router.message(CalculatorStates.WAITING_POWER)
async def process_power(message: Message, state: FSMContext):
    """Обработка мощности и вывод результата"""
    if not is_valid_number(message.text):
        await message.answer(msgs.INVALID_POWER)
        return
    
    # Получаем все данные
    data = await state.get_data()
    
    # Рассчитываем стоимость
    result = calculator.calculate_total_cost(
        price_cny=data['price'],
        year=data['year'],
        engine_cc=data['engine']
    )
    
    # Отправляем результат
    await message.answer(
        msgs.RESULT_TEMPLATE.format(**result),
        reply_markup=get_calculator_keyboard()
    )
    
    # Очищаем состояние
    await state.clear()

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков калькулятора"""
    dp.include_router(router) 