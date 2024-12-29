import logging
import random
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InputMediaPhoto
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    InlineQueryHandler
)
from dotenv import load_dotenv
import os
import json
from config import (
    TOKEN, 
    MANAGER_ID, 
    MANAGER_USERNAME, 
    logger,
    WAITING_QUESTION,
    SURVEY_BUDGET,
    WAITING_QUESTION,
    SURVEY_BUDGET,
    SURVEY_CAR_TYPE,
    SURVEY_USAGE,
    SURVEY_CONCERNS,
    SURVEY_FEATURES,
    SURVEY_TIMELINE,
    SURVEY_TRADE_IN,
    SURVEY_CONTACT
)
from data.catalog import get_filtered_cars, cars_data, categories, price_ranges, countries
from data import faq_data
from utils.keyboards import (
    get_main_menu_keyboard,
    get_catalog_countries_keyboard,
    get_car_selection_keyboard,
    get_body_type_keyboard,
    get_car_actions_keyboard,
    get_survey_start_keyboard,
    get_survey_budget_keyboard,
    get_return_menu_keyboard,
    get_navigation_keyboard
)

# словарь для хранения ответов пользователей
survey_responses = {}
# словарь для хранения состояний пользователей
user_states = {}
# Словарь для хранения избранных автомобилей пользователей
favorites = {}
# Словарь для хранения подписок на уведомления
notifications_subscribers = set()

# Данные для калькулятора
calculator_data = {
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начальное меню бота"""
    reply_markup = get_main_menu_keyboard()
    await update.message.reply_text(
        "Привет! 👋 Я помогу вам подобрать автомобиль из Китая. Чем могу помочь?",
        reply_markup=reply_markup
    )

async def car_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало процесса подбора автомобиля"""
    reply_markup = get_car_selection_keyboard()
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            "Какой у вас бюджет? 💰",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Какой у вас бюджет? 💰",
            reply_markup=reply_markup
        )

async def select_body_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор типа кузова"""
    query = update.callback_query
    budget = query.data.split('_')[1]
    user_states[query.from_user.id] = {'budget': budget}
    
    reply_markup = get_body_type_keyboard()
    
    await query.answer()
    await query.message.edit_text(
        "Выберите тип кузова: 🚗",
        reply_markup=reply_markup
    )

async def show_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ подходящих автомобилей (только 3 случайных)"""
    query = update.callback_query
    body_type, budget = query.data.split('_')[1:]
    
    # Получаем отфильтрованные автомобили
    filtered_cars = get_filtered_cars(price_range=budget, category=body_type)
    
    if not filtered_cars:
        await query.answer()
        await query.message.reply_text(
            "К сожалению, не найдено автомобилей по вашим критериям 😔"
        )
        return
    
    # Выбираем случайные 3 автомобиля
    selected_cars = random.sample(filtered_cars, min(3, len(filtered_cars)))
    
    await query.answer()
    await query.message.reply_text(
        f"Нашел для вас {len(selected_cars)} подходящих варианта 🚗"
    )
    
    for car in selected_cars:
        # Формируем описание автомобиля
        message = (
            f"🚘 {car['brand']} {car['model']} {car['year']}\n"
            f"💰 {car['price']:,} ₽\n"
            f"🛣 Пробег: {car['specs']['mileage']} км\n"
            f"🔧 Двигатель: {car['specs']['engine_volume']}л, {car['specs']['fuel_type']}\n"
            f"⚡️ Мощность: {car['specs']['horse_power']} л.с.\n"
            f"🔄 КПП: {car['specs']['transmission']}\n"
            f"🚙 Привод: {car['specs']['drive_type']}\n"
        )
        
        if 'features' in car['specs']:
            message += "✨ Особенности: " + ", ".join(car['specs']['features']) + "\n"
        
        # Создаем клавиатуру для каждого автомобиля
        keyboard = [
            [InlineKeyboardButton(
                f"⭐️ Добавить {car['brand']} {car['model']} в избранное",
                callback_data=f"favorite_{car['id']}"
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем описание автомобиля
        await query.message.reply_text(message, reply_markup=reply_markup)
        
        # Отправляем фотографии
        if car['images']:
            media_group = []
            # Ограничиваем количество фотографий до 5 для каждого автомобиля
            for image_path in car['images'][:5]:
                try:
                    # Преобразуем веб-путь в локальный путь
                    local_path = f"data{image_path}"
                    media_group.append(InputMediaPhoto(media=open(local_path, 'rb')))
                except Exception as e:
                    logging.error(f"Ошибка при загрузке изображения {image_path}: {e}")
                    continue
            
            if media_group:
                try:
                    await query.message.reply_media_group(media=media_group)
                except Exception as e:
                    logging.error(f"Ошибка при отправке медиагруппы: {e}")
    
        # Добавляем кнопки после показа всех автомобилей
        keyboard = []
        
        # Добавляем кнопку "Показать еще" только если есть дополнительные автомобили
        if len(filtered_cars) > 3:
            keyboard.append([
                InlineKeyboardButton(
                    "🔄 Показать другие варианты",
                    callback_data=f"body_{body_type}_{budget}"
                )
            ])
        
        # Всегда добавляем кнопку возврата в меню
        keyboard.append([
            InlineKeyboardButton(
                "« Вернуться в меню",
                callback_data='start'
            )
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "Выберите действие:",
            reply_markup=reply_markup
        )

async def contact_manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для связи с менеджером"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Вернуться в главное меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Пожалуйста, напишите ваш вопрос менеджеру:",
        reply_markup=reply_markup
    )
    
    return WAITING_QUESTION

async def process_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка полученного номера телефона"""
    user = update.message.from_user
    
    if update.message.text == "Отмена":
        await return_to_main_menu(update, context)
        return ConversationHandler.END
    
    if update.message.contact:
        phone = update.message.contact.phone_number
        context.user_data['phone'] = phone
        
        await update.message.reply_text(
            "Спасибо! Теперь опишите ваш вопрос одним сообщением:",
            reply_markup=ReplyKeyboardRemove()
        )
        return WAITING_QUESTION
    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопку 'Отправить номер телефона' или нажмите 'Отмена'."
        )
        return WAITING_PHONE
    
async def process_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка вопроса клиента"""
    user = update.message.from_user
    question = update.message.text
    
    # Формируем сообщение для менеджера
    manager_message = (
        f"❗️ Новая завка на консультацию ❗️\n\n"
        f"👤 Клиент: {user.first_name} {user.last_name or ''}\n"
        f"🆔 ID: {user.id}\n"
        f"💬 Username: @{user.username or 'отсутствует'}\n\n"
        f"❓ Вопрос:\n{question}"
    )
    
    try:
        await context.bot.send_message(
            chat_id=MANAGER_ID,
            text=manager_message
        )
        
        # Возвращаем пользователя в главное меню
        keyboard = [
            [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
            [InlineKeyboardButton("💰 Калькулятор стоимости", callback_data='calculator')],
            [InlineKeyboardButton("⭐️ Избранное", callback_data='favorites')],
            [InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')],
            [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
            [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
            [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Спасибо за ваш вопрос! Менеджер ответит вам в ближайшее время.",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления менеджеру: {e}")
        keyboard = [
            [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
            [InlineKeyboardButton("💰 Калькулятор стоимости", callback_data='calculator')],
            [InlineKeyboardButton("⭐️ Избранное", callback_data='favorites')],
            [InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')],
            [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
            [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
            [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Извините, произошла техническая ошибка. Пожалуйста, попробуйте позже.",
            reply_markup=reply_markup
        )
    
    return ConversationHandler.END

async def return_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню"""
    keyboard = [
        [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
        [InlineKeyboardButton("👨 Калькулятор стоимости", callback_data='calculator')],
        [InlineKeyboardButton("⭐️ Избранное", callback_data='favorites')],
        [InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')],
        [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
        [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Вы вернулись в главное меню. Чем могу помочь?",
        reply_markup=reply_markup
    )

async def return_to_main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик возврата в главное меню через callback"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
        [InlineKeyboardButton("👨 Калькулятор стоимости", callback_data='calculator')],
        [InlineKeyboardButton("⭐️ Избранное", callback_data='favorites')],
        [InlineKeyboardButton("🔔 Уведомления", callback_data='notifications')],
        [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
        [InlineKeyboardButton("❓ FAQ", callback_data='faq')],
        [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало опроса"""
    query = update.callback_query
    await query.answer()
    
    logger.info(f"Starting survey for user {query.from_user.id}")
    
    # Инициализируем хранение ответов пользователя
    user_id = query.from_user.id
    survey_responses[user_id] = {}
    
    keyboard = [
        [InlineKeyboardButton("🎯 Начать опрос", callback_data='survey_start')],
        [InlineKeyboardButton("« Вернуться в меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "🎁 Специальное предложение!\n\n"
        "Пройдите наш опрос и получите:\n"
        "✅ Персональную скидку 10000₽\n"
        "✅ Индивидуальное предложение\n"
        "✅ Приоритетное обслуживание\n\n"
        "⏱ Это займет всего 2-3 минуты.",
        reply_markup=reply_markup
    )

async def survey_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вопрос о бюджете"""
    query = update.callback_query
    await query.answer()
    
    logger.info(f"Survey budget question for user {query.from_user.id}")
    
    keyboard = [
        [InlineKeyboardButton("До 1.5 млн ₽", callback_data='survey_budget_1.5')],
        [InlineKeyboardButton("1.5 - 2.5 млн ₽", callback_data='survey_budget_2.5')],
        [InlineKeyboardButton("2.5 - 3.5 млн ₽", callback_data='survey_budget_3.5')],
        [InlineKeyboardButton("Более 3.5 млн ₽", callback_data='survey_budget_more')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "1️⃣ Какой бюджет вы рассматриваете для покупки автомобиля?\n\n"
        "💡 Включая дополнительное оборудование и страховку",
        reply_markup=reply_markup
    )
    return SURVEY_BUDGET

async def survey_car_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вопрос о типе автомобиля"""
    query = update.callback_query
    await query.answer()
    
    # Сохраняем ответ о бюджете
    user_id = query.from_user.id
    survey_responses[user_id]['budget'] = query.data.split('_')[-1]
    
    keyboard = [
        [InlineKeyboardButton("🚗 Новый автомобиль", callback_data='survey_type_new')],
        [InlineKeyboardButton("🚙 С пробегом до 1 года", callback_data='survey_type_1year')],
        [InlineKeyboardButton("🚘 С пробегом до 3 лет", callback_data='survey_type_3years')],
        [InlineKeyboardButton("🔄 Рассматриваю все варианты", callback_data='survey_type_all')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "2️⃣ Какой автомобиль вас интересует?",
        reply_markup=reply_markup
    )
    return SURVEY_CAR_TYPE

async def survey_usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вопрос о целях использования"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    survey_responses[user_id]['car_type'] = query.data.split('_')[-1]
    
    keyboard = [
        [InlineKeyboardButton("🏢 Для работы", callback_data='survey_usage_work')],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 Для семьи", callback_data='survey_usage_family')],
        [InlineKeyboardButton("🏃 Для активного отдыха", callback_data='survey_usage_active')],
        [InlineKeyboardButton("🌆 Для города", callback_data='survey_usage_city')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "3️⃣ Как планируете использовать автомобиль?",
        reply_markup=reply_markup
    )
    return SURVEY_USAGE

async def survey_concerns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вопрос о сомнениях"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    survey_responses[user_id]['usage'] = query.data.split('_')[-1]
    
    keyboard = [
        [InlineKeyboardButton("🔧 Сервис и запчасти", callback_data='survey_concerns_service')],
        [InlineKeyboardButton("💰 Остаточная стоимость", callback_data='survey_concerns_value')],
        [InlineKeyboardButton("⚙️ Надежность", callback_data='survey_concerns_reliability')],
        [InlineKeyboardButton("🤔 Нет сомнений", callback_data='survey_concerns_none')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "4️⃣ Что вызывает наибольшие сомнения при выборе китайского автомобиля?",
        reply_markup=reply_markup
    )
    return SURVEY_CONCERNS

async def generate_promo_code(user_id: int) -> str:
    """Генерация уникального промокода"""
    import hashlib
    import time
    
    # Создаем уникальный код на основе ID пользователя и времени
    hash_string = f"{user_id}{time.time()}".encode()
    hash_object = hashlib.md5(hash_string)
    return f"ASIASTART{hash_object.hexdigest()[:6].upper()}"

async def finish_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение опроса"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    survey_responses[user_id]['concerns'] = query.data.split('_')[-1]
    
    # Генерируем промокод
    promo_code = await generate_promo_code(user_id)
    survey_responses[user_id]['promo_code'] = promo_code
    
    # Отправляем данные менеджеру
    manager_message = (
        f"📊 Новый заполненный опрос!\n\n"
        f"👤 Клиент: {query.from_user.first_name} {query.from_user.last_name or ''}\n"
        f"🆔 ID: {user_id}\n"
        f"💬 Username: @{query.from_user.username or 'отсутствует'}\n\n"
        f"💰 Бюджет: {survey_responses[user_id]['budget']}\n"
        f"🚗 Тип авто: {survey_responses[user_id]['car_type']}\n"
        f"💬 Цель использования: {survey_responses[user_id]['usage']}\n"
        f"❓ Сомнения: {survey_responses[user_id]['concerns']}\n"
        f"🎁 Промокод: {promo_code}"
    )
    
    try:
        await context.bot.send_message(
            chat_id=MANAGER_ID,
            text=manager_message
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке результатов опроса менеджеру: {e}")

    keyboard = [
        [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
        [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')],
        [InlineKeyboardButton("« Вернуться в меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        f"🎉 Поздравляем! Вы получили персональную скидку!\n\n"
        f"Ваш промокод: `{promo_code}`\n\n"
        f"💡 Сохраните промокод и предъявите его менеджеру при покупке автомобиля.\n"
        f"⏰ Срок действия: 14 дней\n\n"
        f"Хотите подбрать автомобиль прямо сейчас?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик inline-запросов для быстрого поиска автомобилей"""
    query = update.inline_query.query.lower()
    results = []
    
    # Поиск по всем автомобилям
    for budget_category in catalog.values():
        for body_type in budget_category.values():
            for car in body_type:
                if query in car['name'].lower():
                    results.append(
                        InlineQueryResultArticle(
                            id=f"{car['name']}_{car['year']}",
                            title=f"{car['name']} ({car['year']})",
                            description=f"Цена: {car['price']:,} ₽",
                            input_message_content=InputTextMessageContent(
                                message_text=f"🚗 {car['name']} {car['year']}\n"
                                           f"💰 Цена: {car['price']:,} ₽\n"
                                           f"Для подробной информации используйте команду /start"
                            )
                        )
                    )
    
    await update.inline_query.answer(results[:50])

async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ FAQ раздела"""
    keyboard = []
    for key, data in faq_data.items():
        keyboard.append([InlineKeyboardButton(data['question'], callback_data=f'faq_{key}')])
    keyboard.append([InlineKeyboardButton("Вернуться в главное меню", callback_data='start')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            "Часто задаваемые вопросы:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Часто задаваемые вопросы:",
            reply_markup=reply_markup
        )

async def show_faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ ответа на конкретный вопрос FAQ"""
    query = update.callback_query
    faq_key = query.data.split('_')[1]
    
    keyboard = [
        [InlineKeyboardButton("Назад к FAQ", callback_data='faq')],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.answer()
    await query.message.reply_text(
        f"❓ {faq_data[faq_key]['question']}\n\n"
        f"📝 {faq_data[faq_key]['answer']}",
        reply_markup=reply_markup
    )

async def add_to_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавление автомобиля в избранное"""
    query = update.callback_query
    catalog = query.data.split('_')[1:]  # favorite_budget_bodytype_index
    user_id = query.from_user.id
    
    if user_id not in favorites:
        favorites[user_id] = []
    
    budget = catalog[0]
    body_type = catalog[1]
    car_index = int(catalog[2])
    
    car = catalog[budget][body_type][car_index]
    
    if car not in favorites[user_id]:
        favorites[user_id].append(car)
        await query.answer("Автомобиль добавлен в избранное! ⭐️")
    else:
        await query.answer("Этот автомобиль уже в избранном!")

async def show_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ списка избранных автомобилей"""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        message = query.message
    else:
        user_id = update.message.from_user.id
        message = update.message
    
    if user_id not in favorites or not favorites[user_id]:
        keyboard = [[InlineKeyboardButton("Вернуться в главное меню", callback_data='start')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(
            "У вас пока нет избранных автомобилей! ⭐️\n"
            "Добавьте их при просмотре каталога.",
            reply_markup=reply_markup
        )
        return
    
    text = "Ваши избранные автомобили:\n\n"
    keyboard = []
    
    for i, car in enumerate(favorites[user_id]):
        text += f"🚗 {car['name']} {car['year']}\n💰 {car['price']:,} ₽\n\n"
        keyboard.append([InlineKeyboardButton(
            f"❌ Удалить {car['name']}", 
            callback_data=f'remove_favorite_{i}'
        )])
    
    keyboard.append([InlineKeyboardButton("Вернуться в главное меню", callback_data='start')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(text, reply_markup=reply_markup)

async def remove_from_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаление автомобиля из избранного"""
    query = update.callback_query
    user_id = query.from_user.id
    index = int(query.data.split('_')[2])
    
    if user_id in favorites and 0 <= index < len(favorites[user_id]):
        removed_car = favorites[user_id].pop(index)
        await query.answer(f"{removed_car['name']} удален из избранного!")
        await show_favorites(update, context)
    else:
        await query.answer("Ошибка при удалении из избранного")

async def toggle_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Включение/выключение уведомлений о новых моделях"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id in notifications_subscribers:
        notifications_subscribers.remove(user_id)
        await query.answer("Уведомления отключены! 🔕")
    else:
        notifications_subscribers.add(user_id)
        await query.answer("Уведомления включены! 🔔")
    
    await show_notification_settings(update, context)

async def show_notification_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ настроек уведомлений"""
    if update.callback_query:
        query = update.callback_query
        user_id = query.from_user.id
        message = query.message
    else:
        user_id = update.message.from_user.id
        message = update.message
    
    status = "включены 🔔" if user_id in notifications_subscribers else "выключены 🔕"
    
    keyboard = [
        [InlineKeyboardButton(
            "Выключить уведомления 🔕" if user_id in notifications_subscribers else "Включить уведомления 🔔",
            callback_data='toggle_notifications'
        )],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(
        f"Настройки уведомлений\n\n"
        f"Статус: {status}\n\n"
        f"При включенных уведомлениях вы будете получать информацию о:\n"
        f"• Новых моделях автомобилей\n"
        f"• Специальных предложениях\n"
        f"• Изменениях цен",
        reply_markup=reply_markup
    )

async def notify_about_new_car(context: ContextTypes.DEFAULT_TYPE, car_info: dict):
    """тправка уведомления о новой модели всем подписчикам"""
    message = (
        f"🆕 Новая модель в каталоге!\n\n"
        f"🚗 {car_info['name']} {car_info['year']}\n"
        f"💰 Цена: {car_info['price']:,} ₽\n\n"
        f"Нажмите /start чтобы узнать подробнее"
    )
    
    for user_id in notifications_subscribers:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=message
            )
        except Exception as e:
            logging.error(f"Ошибка при отправке уведомления пользователю {user_id}: {e}")

async def start_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало работы калькулятора"""
    query = update.callback_query
    await query.answer()
    
    # Очищаем предыдущие данные калькулятора
    context.user_data.clear()
    context.user_data['calculator'] = {
        'base_price': 0,
        'options': set(),
        'services': set(),
        'total': 0
    }
    
    keyboard = [
        [InlineKeyboardButton("До 1.5 млн ₽", callback_data='calc_1500000')],
        [InlineKeyboardButton("1.5 - 2.5 млн ₽", callback_data='calc_2500000')],
        [InlineKeyboardButton("2.5 - 3.5 млн ₽", callback_data='calc_3500000')],
        [InlineKeyboardButton("« Вернуться в меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "🧮 Калькулятор стоимости\n\n"
        "Давайте рассчитаем полную стоимость автомобиля.\n"
        "Для начала выберите базовую стоимость:",
        reply_markup=reply_markup
    )

async def select_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор дополнительных опций"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('calc_'):
        # Получаем базовую цену
        base_price = int(query.data.split('_')[1])
        context.user_data['calculator']['base_price'] = base_price
    
    # Формируем клавиатуру с опциями
    keyboard = []
    calc_data = context.user_data['calculator']
    
    for option_id, option in calculator_data['additional_options'].items():
        checkbox = '✅' if option_id in calc_data['options'] else '⬜️'
        keyboard.append([InlineKeyboardButton(
            f"{checkbox} {option['name']} (+{option['price']:,} ₽)",
            callback_data=f'option_{option_id}'
        )])
    
    keyboard.append([InlineKeyboardButton("➡️ Далее", callback_data='calc_services')])
    keyboard.append([InlineKeyboardButton("« Вернуться в меню", callback_data='start')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    total = calc_data['base_price']
    for opt in calc_data['options']:
        total += calculator_data['additional_options'][opt]['price']
    
    context.user_data['calculator']['total'] = total
    
    await query.message.edit_text(
        "🛠 Выберите дополнительные опции:\n\n"
        f"Базовая стоимость: {calc_data['base_price']:,} ₽\n"
        f"Стоимость опций: {(total - calc_data['base_price']):,} ₽\n"
        f"Итого: {total:,} ₽",
        reply_markup=reply_markup
    )

async def select_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор дополнительных услуг"""
    query = update.callback_query
    await query.answer()
    
    calc_data = context.user_data['calculator']
    
    if query.data.startswith('option_'):
        # Обработка ыбора опции
        option_id = query.data.split('_')[1]
        if option_id in calc_data['options']:
            calc_data['options'].remove(option_id)
        else:
            calc_data['options'].add(option_id)
        return await select_options(update, context)
    
    if query.data.startswith('service_'):
        # Обработка выбора услуги
        service_id = query.data.split('_')[1]
        if service_id in calc_data['services']:
            calc_data['services'].remove(service_id)
        else:
            calc_data['services'].add(service_id)
    
    # Форруем клавиатуру с услугами
    keyboard = []
    
    for service_id, service in calculator_data['services'].items():
        checkbox = '✅' if service_id in calc_data['services'] else '⬜️'
        keyboard.append([InlineKeyboardButton(
            f"{checkbox} {service['name']} (+{service['price']:,} ₽)",
            callback_data=f'service_{service_id}'
        )])
    
    keyboard.append([InlineKeyboardButton("📊 Показать итог", callback_data='calc_result')])
    keyboard.append([InlineKeyboardButton("« Вернуться к опциям", callback_data='calc_back_options')])
    keyboard.append([InlineKeyboardButton("« Вернуться в меню", callback_data='start')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Подсчет общей стоимости
    total = calc_data['base_price']
    options_cost = sum(calculator_data['additional_options'][opt]['price'] for opt in calc_data['options'])
    services_cost = sum(calculator_data['services'][srv]['price'] for srv in calc_data['services'])
    total += options_cost + services_cost
    
    context.user_data['calculator']['total'] = total
    
    await query.message.edit_text(
        "🛎 Выберите дополнительные услуги:\n\n"
        f"Базовая стоимость: {calc_data['base_price']:,} ₽\n"
        f"Стоимость опций: {options_cost:,} ₽\n"
        f"Стоимость услуг: {services_cost:,} ₽\n"
        f"Итого: {total:,} ₽",
        reply_markup=reply_markup
    )

async def show_calculator_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ итоговой стоимости"""
    query = update.callback_query
    await query.answer()
    
    calc_data = context.user_data['calculator']
    
    # Формируем детальный отчет
    options_text = ""
    if calc_data['options']:
        options_text = "Выбранные опции:\n" + "\n".join(
            f"• {calculator_data['additional_options'][opt]['name']}: {calculator_data['additional_options'][opt]['price']:,} ₽"
            for opt in calc_data['options']
        ) + "\n\n"
    
    services_text = ""
    if calc_data['services']:
        services_text = "Выбранные услуги:\n" + "\n".join(
            f"• {calculator_data['services'][srv]['name']}: {calculator_data['services'][srv]['price']:,} ₽"
            for srv in calc_data['services']
        ) + "\n\n"
    
    # Подсчет стоимости
    options_cost = sum(calculator_data['additional_options'][opt]['price'] for opt in calc_data['options'])
    services_cost = sum(calculator_data['services'][srv]['price'] for srv in calc_data['services'])
    total = calc_data['base_price'] + options_cost + services_cost
    
    keyboard = [
        [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
        [InlineKeyboardButton("🔄 Новый расчет", callback_data='calculator')],
        [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')],
        [InlineKeyboardButton("« Вернуться в меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Создаем ссылку на менеджера
    manager_link = f'<a href="https://t.me/{MANAGER_USERNAME}">менеджера</a>' if MANAGER_USERNAME else 'менеджера'
    
    await query.message.edit_text(
        "📊 Итоговый расчет стоимости:\n\n"
        f"Базовая стоимость: {calc_data['base_price']:,} ₽\n\n"
        f"{options_text}"
        f"{services_text}"
        f"Итоговая стоимость: {total:,} ₽\n\n"
        f"💡 Точную стоимость автомоиля с учетом всех акций и скидок вы можете узнать у {manager_link}.",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def send_car_photos(update: Update, context: ContextTypes.DEFAULT_TYPE, car_data: dict):
    """Отправка фотографий автомобиля"""
    if 'images' in car_data:
        media_group = []
        for image_path in car_data['images'][:10]:  # Ограничиваем до 10 фото
            # Преобразуем путь из веб-формата в локальный
            local_path = f"static{image_path}"
            try:
                media_group.append(InputMediaPhoto(media=open(local_path, 'rb')))
            except FileNotFoundError:
                continue
        
        if media_group:
            await update.message.reply_media_group(media=media_group)
        else:
            await update.message.reply_text("К сожалению, фотографии временно недоступны")

def main():
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    # Создаем обработчик разговора для связи с менеджером
    contact_manager_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(contact_manager, pattern='^contact_manager$')],
        states={
            WAITING_QUESTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_question)
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(return_to_main_menu_callback, pattern='^start$')
        ]
    )

    # Добавляем обработчик опроса
    survey_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_survey, pattern='^survey$')],
        states={
            SURVEY_BUDGET: [
                CallbackQueryHandler(survey_budget, pattern='^survey_start$'),
                CallbackQueryHandler(survey_car_type, pattern='^survey_budget_')
            ],
            SURVEY_CAR_TYPE: [CallbackQueryHandler(survey_usage, pattern='^survey_type_')],
            SURVEY_USAGE: [CallbackQueryHandler(survey_concerns, pattern='^survey_usage_')],
            SURVEY_CONCERNS: [CallbackQueryHandler(finish_survey, pattern='^survey_concerns_')]
        },
        fallbacks=[
            CommandHandler('start', start),
            CallbackQueryHandler(return_to_main_menu_callback, pattern='^start$'),
            CallbackQueryHandler(start_survey, pattern='^survey$')
        ],
        allow_reentry=True
    )
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(car_selection, pattern='^car_selection$'))
    application.add_handler(CallbackQueryHandler(select_body_type, pattern='^budget_'))
    application.add_handler(CallbackQueryHandler(show_cars, pattern='^body_'))
    application.add_handler(contact_manager_handler)
    application.add_handler(survey_handler)
    application.add_handler(CallbackQueryHandler(return_to_main_menu_callback, pattern='^start$'))
    application.add_handler(InlineQueryHandler(inline_search))
    application.add_handler(CallbackQueryHandler(show_faq, pattern='^faq$'))
    application.add_handler(CallbackQueryHandler(show_faq_answer, pattern='^faq_.*$'))
    application.add_handler(CallbackQueryHandler(show_favorites, pattern='^favorites$'))
    application.add_handler(CallbackQueryHandler(add_to_favorites, pattern='^favorite_.*$'))
    application.add_handler(CallbackQueryHandler(remove_from_favorites, pattern='^remove_favorite_.*$'))
    application.add_handler(CallbackQueryHandler(show_notification_settings, pattern='^notifications$'))
    application.add_handler(CallbackQueryHandler(toggle_notifications, pattern='^toggle_notifications$'))
    application.add_handler(CallbackQueryHandler(start_calculator, pattern='^calculator$'))
    application.add_handler(CallbackQueryHandler(select_options, pattern='^calc_[0-9]+$'))
    application.add_handler(CallbackQueryHandler(select_options, pattern='^calc_back_options$'))
    application.add_handler(CallbackQueryHandler(select_services, pattern='^calc_services$'))
    application.add_handler(CallbackQueryHandler(select_services, pattern='^option_'))
    application.add_handler(CallbackQueryHandler(select_services, pattern='^service_'))
    application.add_handler(CallbackQueryHandler(show_calculator_result, pattern='^calc_result$'))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()