from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_budget_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора бюджета"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="До 2 млн ₽"), KeyboardButton(text="2-3 млн ₽")],
            [KeyboardButton(text="3-4 млн ₽"), KeyboardButton(text="4-5 млн ₽")],
            [KeyboardButton(text="Более 5 млн ₽")]
        ],
        resize_keyboard=True
    )

def get_timeframe_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора временных рамок"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="В ближайший месяц")],
            [KeyboardButton(text="В течение 3 месяцев")],
            [KeyboardButton(text="В течение 6 месяцев")],
            [KeyboardButton(text="Просто интересуюсь")]
        ],
        resize_keyboard=True
    )

def get_features_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора характеристик"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Комфорт"), KeyboardButton(text="Безопасность")],
            [KeyboardButton(text="Экономичность"), KeyboardButton(text="Престиж")],
            [KeyboardButton(text="Технологичность"), KeyboardButton(text="Надежность")]
        ],
        resize_keyboard=True
    )

def get_purpose_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора цели использования"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Для города"), KeyboardButton(text="Для семьи")],
            [KeyboardButton(text="Для бизнеса"), KeyboardButton(text="Для путешествий")],
            [KeyboardButton(text="Как второй автомобиль")]
        ],
        resize_keyboard=True
    )

def get_current_car_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора текущего автомобиля"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇯🇵 Японский"), KeyboardButton(text="🇨🇳 Китайский")],
            [KeyboardButton(text="🇰🇷 Корейский"), KeyboardButton(text="🇪🇺 Европейский")],
            [KeyboardButton(text="🇺🇸 Американский"), KeyboardButton(text="🔄 Другой")]
        ],
        resize_keyboard=True
    )

def get_concerns_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора сомнений"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Качество сборки"), KeyboardButton(text="Надёжность")],
            [KeyboardButton(text="Наличие запчастей"), KeyboardButton(text="Стоимость обслуживания")],
            [KeyboardButton(text="Остаточная стоимость"), KeyboardButton(text="Безопасность")],
            [KeyboardButton(text="Нет сомнений")]
        ],
        resize_keyboard=True
    )

def get_contact_time_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора времени контакта"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Утро (9:00-12:00)")],
            [KeyboardButton(text="День (12:00-17:00)")],
            [KeyboardButton(text="Вечер (17:00-20:00)")]
        ],
        resize_keyboard=True
    )