from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.config import BOT_TOKEN
from app.handlers import (
    register_car_catalog_handlers,
    register_car_selection_handlers,
    register_calculator_handlers,
    register_favorites_handlers,
    register_survey_handlers,
    register_support_handlers,
    register_faq_handlers,
    register_admin_handlers
)
from app.handlers.base import register_handlers as register_base_handlers

async def create_bot() -> Bot:
    """Создание экземпляра бота"""
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    return Bot(token=BOT_TOKEN, default=default)

async def create_dispatcher(bot: Bot) -> Dispatcher:
    """Создание и настройка диспетчера"""
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация всех обработчиков
    register_base_handlers(dp)
    register_car_catalog_handlers(dp)
    register_car_selection_handlers(dp)
    register_calculator_handlers(dp)
    register_favorites_handlers(dp)
    register_survey_handlers(dp)
    register_support_handlers(dp)
    register_faq_handlers(dp)
    register_admin_handlers(dp)
    
    return dp 