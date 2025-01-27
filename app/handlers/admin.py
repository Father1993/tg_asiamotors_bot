from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.utils.supabase import SupabaseService
from app.config import ADMIN_IDS
from app.keyboards.admin import get_admin_keyboard, get_currency_keyboard
from app.constants.calculator import CalculatorConstants

router = Router()
db = SupabaseService()
calculator_constants = CalculatorConstants()

class AdminCurrencyStates(StatesGroup):
    waiting_for_currency = State()
    waiting_for_rate = State()

def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in ADMIN_IDS

@router.message(Command("admin"))
async def admin_command(message: Message):
    """Обработка команды /admin"""
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав администратора")
        return
    
    await message.answer(
        "👨‍💼 Панель администратора\n\n"
        "Выберите действие:",
        reply_markup=get_admin_keyboard()
    )

@router.callback_query(F.data == "edit_currency")
async def edit_currency_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки редактирования курсов валют"""
    if not is_admin(callback.from_user.id):
        await callback.answer("У вас нет прав администратора")
        return

    rates = await db.get_currency_rates()
    message_text = "💱 Текущие курсы валют:\n\n"
    
    # Используем значения из базы или константы по умолчанию
    cny_rate = rates.get('CNY', calculator_constants.CNY_RATE)
    eur_rate = rates.get('EUR', calculator_constants.EUR_RATE)
    
    message_text += f"CNY: {cny_rate:.2f} ₽\n"
    message_text += f"EUR: {eur_rate:.2f} ₽\n"
    
    message_text += "\nВыберите валюту для редактирования:"
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_currency_keyboard()
    )
    await state.set_state(AdminCurrencyStates.waiting_for_currency)

@router.callback_query(AdminCurrencyStates.waiting_for_currency)
async def currency_selected(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора валюты для редактирования"""
    currency = callback.data  # CNY или EUR
    
    # Получаем текущий курс из базы или используем значение по умолчанию
    current_rate = await db.get_single_currency_rate(currency)
    if current_rate is None:
        current_rate = (
            calculator_constants.CNY_RATE 
            if currency == 'CNY' 
            else calculator_constants.EUR_RATE
        )
    
    await state.update_data(currency=currency)
    
    await callback.message.edit_text(
        f"Введите новый курс для {currency}\n"
        f"Текущий курс: {current_rate:.2f} ₽\n\n"
        "Формат: число с точкой, например 13.97",
        reply_markup=get_currency_keyboard()  # Добавляем клавиатуру с кнопкой "Назад"
    )
    await state.set_state(AdminCurrencyStates.waiting_for_rate)

@router.callback_query(F.data == "admin")
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
    """Обработка возврата в главное меню админки"""
    if not is_admin(callback.from_user.id):
        await callback.answer("У вас нет прав администратора")
        return
    
    await state.clear()
    await callback.message.edit_text(
        "👨‍💼 Панель администратора\n\n"
        "Выберите действие:",
        reply_markup=get_admin_keyboard()
    )

@router.message(AdminCurrencyStates.waiting_for_rate)
async def process_new_rate(message: Message, state: FSMContext):
    """Обработка ввода нового курса валюты"""
    try:
        new_rate = float(message.text.replace(',', '.'))
        if new_rate <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "❌ Некорректное значение. Введите положительное число.",
            reply_markup=get_admin_keyboard()
        )
        return

    data = await state.get_data()
    currency = data['currency']
    
    if await db.update_currency_rate(currency, new_rate):
        await message.answer(
            f"✅ Курс {currency} успешно обновлен до {new_rate:.2f} ₽\n\n"
            "Выберите следующее действие:",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            "❌ Произошла ошибка при обновлении курса.\n"
            "Попробуйте позже или обратитесь к разработчику.",
            reply_markup=get_admin_keyboard()
        )
    
    await state.clear() 