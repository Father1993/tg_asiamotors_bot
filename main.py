import logging
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from dotenv import load_dotenv
import os
import json
import pandas as pd

# переменные окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# ID менеджера
MANAGER_ID = os.getenv('TELEGRAM_MANAGER_ID')

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Константы для состояний разговора
(
    WAITING_QUESTION,
    SURVEY_BUDGET,
    SURVEY_CAR_TYPE,
    SURVEY_USAGE,
    SURVEY_CONCERNS,
    SURVEY_FEATURES,
    SURVEY_TIMELINE,
    SURVEY_TRADE_IN,
    SURVEY_CONTACT
) = range(9)

# словарь для хранения ответов пользователей
survey_responses = {}
# словарь для хранения состояний пользователей
user_states = {}

# Данные об автомобилях
cars_data = {
    'economy': {
        'sedan': [
            {'name': 'Geely Emgrand', 'price': 1450000, 'year': 2023},
            {'name': 'Chery Arrizo', 'price': 1350000, 'year': 2023}
        ],
        'crossover': [
            {'name': 'Haval Jolion', 'price': 1850000, 'year': 2023},
            {'name': 'Chery Tiggo 4', 'price': 1750000, 'year': 2023}
        ]
    },
    'medium': {
        'sedan': [
            {'name': 'GAC Empow', 'price': 2450000, 'year': 2023},
            {'name': 'Chery Arrizo 8', 'price': 2350000, 'year': 2023}
        ],
        'crossover': [
            {'name': 'Haval F7', 'price': 2850000, 'year': 2023},
            {'name': 'Geely Atlas Pro', 'price': 2650000, 'year': 2023}
        ]
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начальное меню бота"""
    keyboard = [
        [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
        [InlineKeyboardButton("💰 Калькулятор стоимости", callback_data='calculator')],
        [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
        [InlineKeyboardButton("👨‍💼 Связаться с менеджером", callback_data='contact_manager')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! 👋 Я помогу вам подобрать автомобиль из Китая. Чем могу помочь?",
        reply_markup=reply_markup
    )

async def car_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало процесса подбора автомобиля"""
    keyboard = [
        [
            InlineKeyboardButton("До 1.5 млн", callback_data='budget_economy'),
            InlineKeyboardButton("1.5-3 млн", callback_data='budget_medium'),
            InlineKeyboardButton("Больше 3 млн", callback_data='budget_premium')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Какой у вас бюджет? 💰",
        reply_markup=reply_markup
    )

async def select_body_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор типа кузова"""
    query = update.callback_query
    budget = query.data.split('_')[1]
    user_states[query.from_user.id] = {'budget': budget}
    
    keyboard = [
        [
            InlineKeyboardButton("Седан", callback_data=f'body_sedan_{budget}'),
            InlineKeyboardButton("Кроссовер", callback_data=f'body_crossover_{budget}')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.message.reply_text(
        "Выберите тип кузова: 🚗",
        reply_markup=reply_markup
    )

async def show_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ подходящих автомобилей"""
    query = update.callback_query
    body_type, budget = query.data.split('_')[1:]
    
    cars = cars_data[budget][body_type]
    
    message = "Вот что я нашёл для вас:\n\n"
    for car in cars:
        message += f"🚘 {car['name']} {car['year']}\n💰 {car['price']:,} ₽\n\n"
    
    keyboard = [
        [InlineKeyboardButton("Рассчитать полную стоимость", callback_data='calculate_full_price')],
        [InlineKeyboardButton("Вернуться в главное меню", callback_data='start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.answer()
    await query.message.reply_text(message, reply_markup=reply_markup)

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
        f"❗️ Новая заявка на консультацию ❗️\n\n"
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
            [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
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
            [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
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
        [InlineKeyboardButton("💰 Калькулятор стоимости", callback_data='calculator')],
        [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
        [InlineKeyboardButton("👨‍💼 Задать вопрос менеджеру", callback_data='contact_manager')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Вы вернулись в главное меню. Чем могу помочь?",
        reply_markup=reply_markup
    )

async def return_to_main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик возврата в главное меню через callback"""
    query = update.callback_query
    await query.answer()  # Важно ответить на callback_query
    
    keyboard = [
        [InlineKeyboardButton("🚗 Подобрать автомобиль", callback_data='car_selection')],
        [InlineKeyboardButton("💰 Калькулятор стоимости", callback_data='calculator')],
        [InlineKeyboardButton("📋 Пройти опрос", callback_data='survey')],
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
    return SURVEY_BUDGET

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
        f"🎯 Цель использования: {survey_responses[user_id]['usage']}\n"
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
        f"Хотите подобрать автомобиль прямо сейчас?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return ConversationHandler.END


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
            CallbackQueryHandler(start, pattern='^start$')
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
            CallbackQueryHandler(start, pattern='^start$')
        ]
    )
    
    application.add_handler(survey_handler)

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(car_selection, pattern='^car_selection$'))
    application.add_handler(CallbackQueryHandler(select_body_type, pattern='^budget_'))
    application.add_handler(CallbackQueryHandler(show_cars, pattern='^body_'))
    application.add_handler(contact_manager_handler)
    application.add_handler(survey_handler) 
    application.add_handler(CallbackQueryHandler(return_to_main_menu_callback, pattern='^start$'))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()