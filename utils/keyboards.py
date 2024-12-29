from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
        [InlineKeyboardButton("💰 Каталог", callback_data='catalog')],
        [InlineKeyboardButton("💰 Калькулятор стоимости", callback_data='calculator')],
        [InlineKeyboardButton("⭐️ Избранное", callback_data='favorites')],
        [InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')],
        [InlineKeyboardButton("📋 Опрос за подарок - 10 000₽!", callback_data='survey')],
        [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_catalog_countries_keyboard():
    keyboard = [
        [InlineKeyboardButton("🇨🇳 Китай", callback_data='catalog_country_china')],
        [InlineKeyboardButton("🇯🇵 Япония", callback_data='catalog_country_japan')],
        [InlineKeyboardButton("🇰🇷 Корея", callback_data='catalog_country_korea')],
        [InlineKeyboardButton("« Вернуться в меню", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_car_selection_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("До 1.5 млн", callback_data='budget_economy'),
            InlineKeyboardButton("1.5-3 млн", callback_data='budget_medium'),
            InlineKeyboardButton("Больше 3 млн", callback_data='budget_premium')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_body_type_keyboard(budget):
    keyboard = [
        [
            InlineKeyboardButton("Седан", callback_data=f'body_sedan_{budget}'),
            InlineKeyboardButton("Кроссовер", callback_data=f'body_crossover_{budget}')
        ],
        [
            InlineKeyboardButton("Минивэн", callback_data=f'body_minivan_{budget}'),
            InlineKeyboardButton("Внедорожник", callback_data=f'body_suv_{budget}')
        ],
        [
            InlineKeyboardButton("Электромобиль", callback_data=f'body_electric_{budget}')
        ],
        [
            InlineKeyboardButton("« Назад", callback_data='car_selection')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_car_actions_keyboard(car):
    keyboard = [
        [InlineKeyboardButton(
            f"⭐️ Добавить {car['brand']} {car['model']} в избранное",
            callback_data=f"favorite_{car['id']}"
        )]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_survey_start_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎯 Начать опрос", callback_data='survey_start')],
        [InlineKeyboardButton("« Вернуться в меню", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_survey_budget_keyboard():
    keyboard = [
        [InlineKeyboardButton("До 1.5 млн ₽", callback_data='survey_budget_1.5')],
        [InlineKeyboardButton("1.5 - 2.5 млн ₽", callback_data='survey_budget_2.5')],
        [InlineKeyboardButton("2.5 - 3.5 млн ₽", callback_data='survey_budget_3.5')],
        [InlineKeyboardButton("Более 3.5 млн ₽", callback_data='survey_budget_more')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_return_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Вернуться в главное меню", callback_data='start')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_navigation_keyboard(current_index, total_cars, category, country):
    keyboard = []
    nav_buttons = []
    
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            "⬅️ Предыдущий",
            callback_data=f'catalog_nav_{category}_{country}_{current_index-1}'
        ))
    if current_index < total_cars - 1:
        nav_buttons.append(InlineKeyboardButton(
            "Следующий ➡️",
            callback_data=f'catalog_nav_{category}_{country}_{current_index+1}'
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.extend([
        [InlineKeyboardButton("« Назад к категориям", callback_data=f'catalog_country_{country}')],
        [InlineKeyboardButton("« Вернуться в меню", callback_data='start')]
    ])
    
    return InlineKeyboardMarkup(keyboard)