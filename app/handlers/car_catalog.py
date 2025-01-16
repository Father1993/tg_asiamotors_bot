from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import json

from app.keyboards.base import KeyboardButtons as kb
from app.FSM.catalog import CatalogStates
from app.utils.supabase import SupabaseService
from app.keyboards import get_main_keyboard

router = Router()
supabase = SupabaseService()

# Маппинг категорий
CATEGORY_MAPPING = {
    "кроссовер": "Кроссоверы",
    "джип": "Внедорожники",
    "седан": "Седаны",
    "универсал": "Универсалы",
    "минивен": "Минивэны"
}

# Клавиатуры для выбора
categories_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кроссовер"), KeyboardButton(text="Джип")],
        [KeyboardButton(text="Седан"), KeyboardButton(text="Универсал")],
        [KeyboardButton(text="Минивен")],
        [KeyboardButton(text=kb.MAIN_MENU)]
    ],
    resize_keyboard=True
)

drive_types_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Полный")],
        [KeyboardButton(text="Передний")],
        [KeyboardButton(text="Задний")],
        [KeyboardButton(text=kb.MAIN_MENU)]
    ],
    resize_keyboard=True
)

fuel_types_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Бензин"), KeyboardButton(text="Дизель")],
        [KeyboardButton(text="Гибрид"), KeyboardButton(text="Электро")],
        [KeyboardButton(text=kb.MAIN_MENU)]
    ],
    resize_keyboard=True
)

async def send_cars_info(message: Message, cars: list, show_more_button: bool = True, offset: int = 0):
    """Отправка информации об автомобилях"""
    for car in cars:
        specs = car.get('specs', {})
        car_info = (
            f"🏁 {car.get('brand', '')} {car.get('model', '')}\n"
            f"📅 Год: {car.get('year', 'Не указан')}\n"
            f"💰 Цена: {car.get('price', 'По запросу')}$\n"
            f"🚘 Пробег: {specs.get('mileage', 'Не указан')} км\n"
            f"⚙️ Двигатель: {specs.get('engineVolume', '')} л. ({specs.get('horsePower', '')} л.с.)\n"
            f"🔧 КПП: {specs.get('transmission', 'Не указана')}\n"
        )
        if car.get('equipment'):
            car_info += f"🛠 Комплектация: {car['equipment']}\n"

        # Если есть фотографии, отправляем первую
        if car.get('images') and len(car['images']) > 0:
            await message.answer_photo(
                photo=car['images'][0],
                caption=car_info
            )
        else:
            await message.answer(car_info)

    if show_more_button:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Показать еще", callback_data=f"show_more_{offset}"),
                    InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")
                ]
            ]
        )
        await message.answer("Хотите посмотреть больше автомобилей?", reply_markup=keyboard)
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")]
            ]
        )
        await message.answer("Это все доступные автомобили", reply_markup=keyboard)

@router.message(F.text == kb.CATALOG)
async def show_catalog(message: Message, state: FSMContext):
    """Начало выбора параметров автомобиля"""
    await state.set_state(CatalogStates.WAITING_CATEGORY)
    await message.answer(
        "🚗 Выберите тип кузова:",
        reply_markup=categories_kb
    )

@router.message(CatalogStates.WAITING_CATEGORY)
async def process_category(message: Message, state: FSMContext):
    """Обработка выбора категории"""
    if message.text == kb.MAIN_MENU:
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=get_main_keyboard())
        return

    category = message.text.lower()
    mapped_category = CATEGORY_MAPPING.get(category, category)
    await state.update_data(category=mapped_category)
    await state.set_state(CatalogStates.WAITING_DRIVE_TYPE)
    await message.answer("Выберите тип привода:", reply_markup=drive_types_kb)

@router.message(CatalogStates.WAITING_DRIVE_TYPE)
async def process_drive_type(message: Message, state: FSMContext):
    """Обработка выбора типа привода"""
    if message.text == kb.MAIN_MENU:
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=get_main_keyboard())
        return

    await state.update_data(drive_type=message.text)
    await state.set_state(CatalogStates.WAITING_FUEL_TYPE)
    await message.answer("Выберите тип топлива:", reply_markup=fuel_types_kb)

@router.message(CatalogStates.WAITING_FUEL_TYPE)
async def process_fuel_type(message: Message, state: FSMContext):
    """Обработка выбора типа топлива и показ результатов"""
    if message.text == kb.MAIN_MENU:
        await state.clear()
        await message.answer("Вы вернулись в главное меню", reply_markup=get_main_keyboard())
        return

    user_data = await state.get_data()
    
    # Формируем фильтры для запроса
    filters = {
        'category': user_data['category'],
        'specs': {
            'driveType': user_data['drive_type'],
            'fuelType': message.text
        }
    }
    
    # Сохраняем фильтры в состоянии для пагинации
    await state.update_data(filters=filters)
    
    # Получаем первые 3 автомобиля
    cars = await supabase.get_cars(filters)
    
    if not cars:
        await message.answer(
            "К сожалению, автомобилей с такими параметрами не найдено.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")
                ]]
            )
        )
        await state.clear()
        return

    # Проверяем, есть ли еще автомобили
    more_cars = await supabase.get_cars(filters, limit=1, offset=3)
    await send_cars_info(message, cars, bool(more_cars), 3)
    
    if not more_cars:
        await state.clear()

@router.callback_query(F.data.startswith("show_more_"))
async def show_more_cars(callback_query: CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки 'Показать еще'"""
    await callback_query.answer()
    
    # Получаем текущее смещение из callback_data
    current_offset = int(callback_query.data.split('_')[2])
    
    # Получаем сохраненные фильтры
    user_data = await state.get_data()
    filters = user_data.get('filters')
    
    if not filters:
        await callback_query.message.answer("Произошла ошибка. Пожалуйста, начните поиск заново.")
        await state.clear()
        return
    
    # Получаем следующую порцию автомобилей
    cars = await supabase.get_cars(filters, offset=current_offset)
    
    if not cars:
        await callback_query.message.answer(
            "Больше автомобилей не найдено",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="В главное меню", callback_data="to_main_menu")
                ]]
            )
        )
        await state.clear()
        return
    
    # Проверяем, есть ли еще автомобили
    more_cars = await supabase.get_cars(filters, limit=1, offset=current_offset + 3)
    await send_cars_info(callback_query.message, cars, bool(more_cars), current_offset + 3)
    
    if not more_cars:
        await state.clear()

@router.callback_query(F.data == "to_main_menu")
async def return_to_main_menu(callback_query: CallbackQuery, state: FSMContext):
    """Обработка возврата в главное меню"""
    await callback_query.answer()
    await state.clear()
    await callback_query.message.answer("Вы вернулись в главное меню", reply_markup=get_main_keyboard())

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков каталога"""
    dp.include_router(router)