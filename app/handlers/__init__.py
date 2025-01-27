# Импорт обработчиков
from aiogram import Dispatcher
from .car_catalog import router as car_catalog_router
from .car_selection import router as car_selection_router
from .calculator import router as calculator_router
from .favorites import router as favorites_router
# from .notifications import register_handlers as register_notifications_handlers 
from .survey import router as survey_router
from .support import router as support_router
from .faq import router as faq_router
from .admin import router as admin_router

def register_car_catalog_handlers(dp: Dispatcher):
    dp.include_router(car_catalog_router)

def register_car_selection_handlers(dp: Dispatcher):
    dp.include_router(car_selection_router)

def register_calculator_handlers(dp: Dispatcher):
    dp.include_router(calculator_router)

def register_favorites_handlers(dp: Dispatcher):
    dp.include_router(favorites_router)

def register_survey_handlers(dp: Dispatcher):
    dp.include_router(survey_router)

def register_support_handlers(dp: Dispatcher):
    dp.include_router(support_router)

def register_faq_handlers(dp: Dispatcher):
    dp.include_router(faq_router)

def register_admin_handlers(dp: Dispatcher):
    dp.include_router(admin_router)

# Экспорт обработчиков
__all__ = [
    'register_car_catalog_handlers',
    'register_car_selection_handlers',
    'register_calculator_handlers',
    'register_favorites_handlers',
    # 'register_notifications_handlers',
    'register_survey_handlers',
    'register_support_handlers',
    'register_faq_handlers',
    'register_admin_handlers'
]