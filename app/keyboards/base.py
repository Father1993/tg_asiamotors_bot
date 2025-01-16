from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Константы для клавиатур
class KeyboardButtons:
    CATALOG = "🚗 Каталог автомобилей"
    SELECT_CAR = "🔍 Подобрать автомобиль"
    CALCULATOR = "🧮 Калькулятор стоимости"
    FAVORITES = "⭐️ Избранное"
    NOTIFICATIONS = "🔔 Уведомления"
    SURVEY = f"🎁 Опрос за подарок - 10 000₽"
    SUPPORT = "👨‍💼 Связаться с менеджером"
    FAQ = "❓ FAQ"
    BACK = "⬅️ Назад"
    MAIN_MENU = "🏠 Главное меню" 

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    buttons = [
        [KeyboardButtons.CATALOG, KeyboardButtons.SELECT_CAR],
        [KeyboardButtons.CALCULATOR, KeyboardButtons.FAVORITES],
        [KeyboardButtons.NOTIFICATIONS, KeyboardButtons.SURVEY],
        [KeyboardButtons.SUPPORT, KeyboardButtons.FAQ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=text) for text in row] for row in buttons],
        resize_keyboard=True
    )

