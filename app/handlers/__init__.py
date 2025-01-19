# Импорт обработчиков
from .car_catalog import register_handlers as register_car_catalog_handlers
from .car_selection import register_handlers as register_car_selection_handlers
from .calculator import register_handlers as register_calculator_handlers
from .favorites import register_handlers as register_favorites_handlers
# from .notifications import register_handlers as register_notifications_handlers 
from .survey import register_handlers as register_survey_handlers
from .support import register_handlers as register_support_handlers
from .faq import register_handlers as register_faq_handlers

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
]