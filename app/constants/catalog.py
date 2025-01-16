class CatalogMessages:
    """Константы для сообщений каталога"""
    SELECT_BODY_TYPE = "🚗 Выберите тип кузова:"
    SELECT_DRIVE_TYPE = "Выберите тип привода:"
    SELECT_FUEL_TYPE = "Выберите тип топлива:"
    NO_CARS_FOUND = "К сожалению, автомобилей с такими параметрами не найдено."
    SHOW_MORE_PROMPT = "Хотите посмотреть больше автомобилей?"
    NO_MORE_CARS = "Это все доступные автомобили"
    ERROR_RETRY = "Произошла ошибка. Пожалуйста, начните поиск заново."
    NO_MORE_CARS_FOUND = "Больше автомобилей не найдено"
    RETURN_MAIN_MENU = "Вы вернулись в главное меню"

class CarInfoTemplate:
    """Шаблон для информации об автомобиле"""
    CARD = (
        "🏁 {brand} {model}\n"
        "📅 Год: {year}\n"
        "💰 Цена: {price}$\n"
        "🚘 Пробег: {mileage} км\n"
        "⚙️ Двигатель: {engine_volume} л. ({horse_power} л.с.)\n"
        "🔧 КПП: {transmission}\n"
        "{equipment}"
    )
    EQUIPMENT = "🛠 Комплектация: {equipment}\n"

class CatalogButtons:
    """Константы для кнопок каталога"""
    CROSSOVER = "Кроссовер"
    SUV = "Джип"
    SEDAN = "Седан"
    WAGON = "Универсал"
    MINIVAN = "Минивен"
    
    FULL_DRIVE = "Полный"
    FRONT_DRIVE = "Передний"
    REAR_DRIVE = "Задний"
    
    PETROL = "Бензин"
    DIESEL = "Дизель"
    HYBRID = "Гибрид"
    ELECTRIC = "Электро"
    
    SHOW_MORE = "Показать еще"

    # Маппинг категорий
CATEGORY_MAPPING = {
    "кроссовер": "Кроссоверы",
    "джип": "Внедорожники",
    "седан": "Седаны",
    "универсал": "Универсалы",
    "минивен": "Минивэны"
}