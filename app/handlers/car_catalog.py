from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import logging

from app.keyboards.base import KeyboardButtons as kb
from app.FSM.catalog import CatalogStates
from app.utils.supabase import SupabaseService
from app.keyboards import (
    get_main_keyboard,
    get_categories_keyboard,
    get_drive_types_keyboard,
    get_fuel_types_keyboard,
    get_pagination_keyboard,
    get_main_menu_keyboard
)
from app.constants.catalog import CatalogMessages as msgs, CATEGORY_MAPPING, CarInfoTemplate

logger = logging.getLogger(__name__)
router = Router()
supabase = SupabaseService()


async def send_cars_info(message: Message, cars: list, show_more_button: bool = True, offset: int = 0) -> None:
    """Отправка информации об автомобилях"""
    for car in cars:
        specs = car.get('specs', {})
        equipment_info = CarInfoTemplate.EQUIPMENT.format(equipment=car['equipment']) if car.get('equipment') else ""
        
        car_info = CarInfoTemplate.CARD.format(
            brand=car.get('brand', ''),
            model=car.get('model', ''),
            year=car.get('year', 'Не указан'),
            price=car.get('price', 'По запросу'),
            mileage=specs.get('mileage', 'Не указан'),
            engine_volume=specs.get('engineVolume', ''),
            horse_power=specs.get('horsePower', ''),
            transmission=specs.get('transmission', 'Не указана'),
            equipment=equipment_info
        )

        # Проверяем, в избранном ли автомобиль
        is_favorite = await supabase.is_favorite(message.from_user.id, car['id'])
        
        # Добавляем индикатор избранного в описание
        favorite_indicator = "❤️ В избранном\n" if is_favorite else ""
        car_info = favorite_indicator + car_info

        # Формируем кнопку с правильным текстом
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❤️ В избранном" if is_favorite else "🤍 Добавить в избранное",
                        callback_data=f"fav_{car['id']}"
                    )
                ],
                # Можно добавить другие кнопки если нужно
            ]
        )

        if car.get('images') and len(car['images']) > 0:
            await message.answer_photo(
                photo=car['images'][0], 
                caption=car_info,
                reply_markup=keyboard
            )
        else:
            await message.answer(
                car_info,
                reply_markup=keyboard
            )

    keyboard = get_pagination_keyboard(offset) if show_more_button else get_main_menu_keyboard()
    await message.answer(
        msgs.SHOW_MORE_PROMPT if show_more_button else msgs.NO_MORE_CARS,
        reply_markup=keyboard
    )

@router.message(F.text == kb.CATALOG)
async def show_catalog(message: Message, state: FSMContext) -> None:
    """Начало выбора параметров автомобиля"""
    await state.set_state(CatalogStates.WAITING_CATEGORY)
    await message.answer(msgs.SELECT_BODY_TYPE, reply_markup=get_categories_keyboard())

@router.message(CatalogStates.WAITING_CATEGORY)
async def process_category(message: Message, state: FSMContext):
    """Обработка выбора категории"""
    if message.text == kb.MAIN_MENU:
        await state.clear()
        await message.answer(msgs.RETURN_MAIN_MENU, reply_markup=get_main_keyboard())
        return

    category = message.text.lower()
    mapped_category = CATEGORY_MAPPING.get(category, category)
    await state.update_data(category=mapped_category)
    await state.set_state(CatalogStates.WAITING_DRIVE_TYPE)
    await message.answer(msgs.SELECT_DRIVE_TYPE, reply_markup=get_drive_types_keyboard())

@router.message(CatalogStates.WAITING_DRIVE_TYPE)
async def process_drive_type(message: Message, state: FSMContext):
    """Обработка выбора типа привода"""
    if message.text == kb.MAIN_MENU:
        await state.clear()
        await message.answer(msgs.RETURN_MAIN_MENU, reply_markup=get_main_keyboard())
        return

    await state.update_data(drive_type=message.text)
    await state.set_state(CatalogStates.WAITING_FUEL_TYPE)
    await message.answer(msgs.SELECT_FUEL_TYPE, reply_markup=get_fuel_types_keyboard())

@router.message(CatalogStates.WAITING_FUEL_TYPE)
async def process_fuel_type(message: Message, state: FSMContext):
    """Обработка выбора типа топлива и показ результатов"""
    if message.text == kb.MAIN_MENU:
        await state.clear()
        await message.answer(msgs.RETURN_MAIN_MENU, reply_markup=get_main_keyboard())
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