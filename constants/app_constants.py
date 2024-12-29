# Данные для калькулятора
CALCULATOR_DATA = {
    'additional_options': {
        'winter': {'name': '❄️ Зимний пакет', 'price': 150000},
        'security': {'name': '🔐 Пакет безопасности', 'price': 200000},
        'multimedia': {'name': '🎵 Мультимедиа пакет', 'price': 180000},
        'comfort': {'name': '💺 Пакет комфорта', 'price': 250000}
    },
    'services': {
        'insurance': {'name': '📋 Страховка КАСКО', 'price': 120000},
        'registration': {'name': '📝 Регистрация авто', 'price': 35000},
        'delivery': {'name': '🚛 Доставка', 'price': 150000}
    }
}

# Ценовые диапазоны
PRICE_RANGES = {
    'economy': (0, 1500000),
    'medium': (1500000, 3000000),
    'premium': (3000000, float('inf'))
}

# Категории автомобилей
CATEGORY_MAPPING = {
    'sedan': 'Седаны',
    'crossover': 'Кроссоверы',
    'minivan': 'Минивэны',
    'suv': 'Внедорожники',
    'electric': 'Электромобили'
}