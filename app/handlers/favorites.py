from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.keyboards.base import KeyboardButtons as kb
from app.utils.supabase import SupabaseService
from app.constants.catalog import CarInfoTemplate

router = Router()
supabase = SupabaseService()

@router.message(F.text == kb.FAVORITES)
async def show_favorites(message: Message, state: FSMContext):
    """Показать избранное"""
    cars = await supabase.get_favorites(message.from_user.id)
    
    if not cars:
        await message.answer(
            "❌ У вас пока нет избранных автомобилей\n"
            "Добавить автомобиль в избранное можно в каталоге"
        )
        return

    for car in cars:
        specs = car.get('specs', {})
        equipment_info = CarInfoTemplate.EQUIPMENT.format(
            equipment=car['equipment']
        ) if car.get('equipment') else ""
        
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

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="❌ Удалить из избранного",
                    callback_data=f"fav_{car['id']}"
                )
            ]]
        )

        if car.get('images') and len(car['images']) > 0:
            await message.answer_photo(
                photo=car['images'][0],
                caption=car_info,
                reply_markup=keyboard
            )
        else:
            await message.answer(car_info, reply_markup=keyboard)

@router.callback_query(F.data.startswith("fav_"))
async def toggle_favorite(callback: CallbackQuery):
    """Обработка добавления/удаления из избранного"""
    car_id = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    is_favorite = await supabase.is_favorite(user_id, car_id)
    
    if is_favorite:
        success = await supabase.remove_from_favorites(user_id, car_id)
        message = "✅ Автомобиль удален из избранного"
        new_text = "🤍 Добавить в избранное"
    else:
        success = await supabase.add_to_favorites(user_id, car_id)
        message = "✅ Автомобиль добавлен в избранное"
        new_text = "❤️ В избранном"
    
    if success:
        # Показываем уведомление
        await callback.answer(message, show_alert=True)
        
        # Обновляем кнопку
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=new_text,
                    callback_data=callback.data
                )
            ]]
        )
        
        try:
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        except Exception as e:
            # Если не удалось обновить кнопку, хотя бы показываем уведомление
            logger.error(f"Failed to update favorite button: {e}")
            pass
    else:
        await callback.answer("❌ Произошла ошибка. Попробуйте позже", show_alert=True)

def register_handlers(dp: Router) -> None:
    dp.include_router(router) 