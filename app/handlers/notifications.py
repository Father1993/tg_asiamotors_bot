from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.utils.supabase import SupabaseService
from app.keyboards.base import KeyboardButtons as kb
import logging

router = Router()
supabase = SupabaseService()
logger = logging.getLogger(__name__)

class NotificationTypes:
    PRICE_DROP = "price_drop"  # Снижение цены
    NEW_ARRIVAL = "new_arrival"  # Новые поступления
    SAVED_SEARCH = "saved_search"  # Результаты сохраненного поиска
    STOCK_STATUS = "stock_status"  # Статус наличия
    SIMILAR_CARS = "similar_cars"  # Похожие автомобили
    SPECIAL_OFFER = "special_offer"  # Специальные предложения

@router.message(F.text == kb.NOTIFICATIONS)
async def show_notifications_menu(message: Message, state: FSMContext):
    """Показать меню настроек уведомлений"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏷 Снижение цены",
                    callback_data="notify_settings_price_drop"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🆕 Новые поступления",
                    callback_data="notify_settings_new_arrival"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Сохраненный поиск",
                    callback_data="notify_settings_saved_search"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Статус наличия",
                    callback_data="notify_settings_stock_status"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚗 Похожие автомобили",
                    callback_data="notify_settings_similar_cars"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎁 Специальные предложения",
                    callback_data="notify_settings_special_offer"
                )
            ]
        ]
    )

    await message.answer(
        "🔔 Настройки уведомлений\n\n"
        "Выберите типы уведомлений, которые хотите получать:\n\n"
        "• Снижение цены - узнавайте первым о снижении цен на интересующие вас авто\n"
        "• Новые поступления - будьте в курсе новых автомобилей в каталоге\n"
        "• Сохраненный поиск - получайте уведомления о новых авто по вашим критериям\n"
        "• Статус наличия - отслеживайте изменения статуса выбранных авто\n"
        "• Похожие автомобили - рекомендации похожих авто на основе ваших интересов\n"
        "• Специальные предложения - эксклюзивные акции и выгодные предложения\n\n"
        "ℹ️ Нажмите на соответствующую кнопку для настройки каждого типа уведомлений",
        reply_markup=keyboard
    )

async def send_price_drop_notification(user_id: int, car_data: dict, old_price: float, new_price: float):
    """Отправка уведомления о снижении цены"""
    message_text = (
        "💰 Снижение цены!\n\n"
        f"🚗 {car_data['brand']} {car_data['model']} {car_data['year']}\n"
        f"📉 Старая цена: {old_price:,.0f} ¥\n"
        f"📊 Новая цена: {new_price:,.0f} ¥\n"
        f"💎 Ваша выгода: {(old_price - new_price):,.0f} ¥\n\n"
        "Успейте приобрести по выгодной цене!"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👀 Посмотреть автомобиль",
                    callback_data=f"view_car_{car_data['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧮 Рассчитать полную стоимость",
                    callback_data=f"calculate_{car_data['id']}"
                )
            ]
        ]
    )

    # Здесь будет код отправки уведомления пользователю
    # await bot.send_message(user_id, message_text, reply_markup=keyboard)

async def send_new_arrival_notification(user_id: int, car_data: dict):
    """Отправка уведомления о новом поступлении"""
    message_text = (
        "🆕 Новое поступление!\n\n"
        f"🚗 {car_data['brand']} {car_data['model']}\n"
        f"📅 Год: {car_data['year']}\n"
        f"💰 Цена: {car_data['price']:,.0f} ¥\n"
        f"🛠 Двигатель: {car_data['specs']['engineVolume']} л. "
        f"({car_data['specs']['horsePower']} л.с.)\n"
        f"📊 Пробег: {car_data['specs']['mileage']} км\n\n"
        "Будьте первым, кто увидит это предложение!"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📱 Связаться с менеджером",
                    callback_data=f"contact_manager_{car_data['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❤️ Добавить в избранное",
                    callback_data=f"fav_{car_data['id']}"
                )
            ]
        ]
    )

    # await bot.send_photo(user_id, car_data['images'][0], message_text, reply_markup=keyboard)

def register_handlers(dp: Router) -> None:
    """Регистрация обработчиков уведомлений"""
    dp.include_router(router) 