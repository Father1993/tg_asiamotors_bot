# Страны
countries = [
    {'id': 'china', 'name': 'Китай'},
    {'id': 'japan', 'name': 'Япония'},
    {'id': 'korea', 'name': 'Корея'},
    {'id': 'europe', 'name': 'Европа'},
]

# Категории автомобилей
categories = [
    'Все',
    'Кроссоверы',
    'Седаны',
    'Электромобили',
    'Минивэны'
]

# Диапазоны цен
price_ranges = [
    'Все цены',
    'До 2 млн',
    '2-3 млн',
    '3-4 млн',
    'От 4 млн'
]

# Основной каталог
cars_data = {
    'china': [
        {
            'id': '4',
            'brand': 'Chery',
            'model': 'Arrizo8',
            'year': 2021,
            'category': 'Седаны',
            'price': 2165000,
            'images': [
                '/img/catalog/china/Chery-Arrizo8/1.jpg',
                '/img/catalog/china/Chery-Arrizo8/2.jpg',
                '/img/catalog/china/Chery-Arrizo8/3.jpg',
                '/img/catalog/china/Chery-Arrizo8/4.jpg',
                '/img/catalog/china/Chery-Arrizo8/5.jpg',
                '/img/catalog/china/Chery-Arrizo8/6.jpg',
                '/img/catalog/china/Chery-Arrizo8/7.jpg',
                '/img/catalog/china/Chery-Arrizo8/8.jpg',
                '/img/catalog/china/Chery-Arrizo8/9.jpg',
            ],
            'specs': {
                'mileage': 18000,
                'engine_volume': 1.6,
                'fuel_type': 'Бензин',
                'horse_power': 197,
                'transmission': 'Робот',
                'drive_type': 'Передний',
            },
            'available': False,
        },
        {
            'id': '5',
            'brand': 'Geely',
            'model': 'Coolray',
            'year': 2021,
            'category': 'Кроссоверы',
            'price': 1413000,
            'images': [
                '/img/catalog/china/Geely-Coolray/1.jpg',
                '/img/catalog/china/Geely-Coolray/2.jpg',
                '/img/catalog/china/Geely-Coolray/3.jpg',
                '/img/catalog/china/Geely-Coolray/4.jpg',
                '/img/catalog/china/Geely-Coolray/5.jpg',
                '/img/catalog/china/Geely-Coolray/6.jpg',
                '/img/catalog/china/Geely-Coolray/7.jpg',
                '/img/catalog/china/Geely-Coolray/8.jpg',
                '/img/catalog/china/Geely-Coolray/9.jpg',
            ],
            'specs': {
                'mileage': 0,
                'engine_volume': 1.5,
                'fuel_type': 'Бензин',
                'horse_power': 177,
                'transmission': 'Робот',
                'drive_type': 'Передний',
            },
            'available': False,
        },
        # ... добавьте остальные автомобили из Китая
    ],
    'japan': [
        {
            'id': '38',
            'brand': 'Honda',
            'model': 'Accord',
            'year': 2021,
            'category': 'Седаны',
            'price': 1950000,
            'images': [
                '/img/catalog/jp/Hоnda-Accord/1.jpg',
                '/img/catalog/jp/Hоnda-Accord/2.jpg',
                '/img/catalog/jp/Hоnda-Accord/3.jpg',
                '/img/catalog/jp/Hоnda-Accord/4.jpg',
                '/img/catalog/jp/Hоnda-Accord/5.jpg',
                '/img/catalog/jp/Hоnda-Accord/6.jpg',
                '/img/catalog/jp/Hоnda-Accord/7.jpg',
                '/img/catalog/jp/Hоnda-Accord/8.jpg',
                '/img/catalog/jp/Hоnda-Accord/9.jpg',
            ],
            'specs': {
                'mileage': 30000,
                'engine_volume': 1.5,
                'fuel_type': 'Бензин',
                'horse_power': 194,
                'transmission': 'Вариатор',
                'drive_type': 'Передний',
            },
            'available': False,
        },
        # ... добавьте остальные японские автомобили
    ],
    'korea': [
        {
            'id': '45',
            'brand': 'Hyundai',
            'model': 'Tucson',
            'year': 2021,
            'category': 'Кроссоверы',
            'price': 1930000,
            'images': [
                '/img/catalog/korea/Hyundai-Tucson/1.jpg',
                '/img/catalog/korea/Hyundai-Tucson/2.jpg',
                '/img/catalog/korea/Hyundai-Tucson/3.jpg',
                '/img/catalog/korea/Hyundai-Tucson/4.jpg',
                '/img/catalog/korea/Hyundai-Tucson/5.jpg',
                '/img/catalog/korea/Hyundai-Tucson/6.jpg',
                '/img/catalog/korea/Hyundai-Tucson/7.jpg',
                '/img/catalog/korea/Hyundai-Tucson/8.jpg',
            ],
            'specs': {
                'mileage': 31000,
                'engine_volume': 1.5,
                'fuel_type': 'Бензин',
                'horse_power': 200,
                'transmission': 'Робот',
                'drive_type': 'Передний',
                'color': 'Серый',
            },
            'available': False,
        },
        # ... добавьте остальные корейские автомобили
    ],
    'europe': [
        # ... добавьте европейские автомобили
    ]
}

# Функция для получения автомобилей по фильтрам
def get_filtered_cars(price_range=None, category=None, country=None):
    """
    Фильтрует автомобили по заданным параметрам
    """
    filtered_cars = []
    
    # Определяем границы цен
    price_limits = {
        'economy': (0, 1500000),        # До 1.5 млн
        'medium': (1500000, 3000000),   # 1.5-3 млн
        'premium': (3000000, float('inf'))  # Больше 3 млн
    }
    
    # Перебираем все страны или только выбранную
    countries_to_check = [country] if country else cars_data.keys()
    
    for country_key in countries_to_check:
        for car in cars_data[country_key]:
            # Проверяем соответствие фильтрам
            matches = True
            
            # Проверка ценового диапазона
            if price_range and price_range in price_limits:
                min_price, max_price = price_limits[price_range]
                if not (min_price <= car['price'] <= max_price):
                    matches = False
            
            # Проверка категории
            if category and category != 'Все':
                if car['category'] != category:
                    matches = False
            
            if matches:
                filtered_cars.append(car)
    
    return filtered_cars

catalog = {
    'cars_data': cars_data,
    'get_filtered_cars': get_filtered_cars,
    'categories': categories,
    'price_ranges': price_ranges,
    'countries': countries
}