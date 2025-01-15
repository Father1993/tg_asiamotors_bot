import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Supabase конфигурация
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# ID администраторов
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))

# Настройки опроса
SURVEY_PRIZE = "10 000₽"

# Константы для клавиатур
class KeyboardButtons:
    CATALOG = "🚗 Каталог автомобилей"
    SELECT_CAR = "🔍 Подобрать автомобиль"
    CALCULATOR = "🧮 Калькулятор стоимости"
    FAVORITES = "⭐️ Избранное"
    NOTIFICATIONS = "🔔 Уведомления"
    SURVEY = f"🎁 Опрос за подарок - {SURVEY_PRIZE}"
    SUPPORT = "👨‍💼 Связаться с менеджером"
    FAQ = "❓ FAQ"
    BACK = "⬅️ Назад"
    MAIN_MENU = "🏠 Главное меню" 