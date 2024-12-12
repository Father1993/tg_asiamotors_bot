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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

# Константы для состояний разговора
(
    WAITING_QUESTION,
) = range(1)



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

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(car_selection, pattern='^car_selection$'))
    application.add_handler(CallbackQueryHandler(select_body_type, pattern='^budget_'))
    application.add_handler(CallbackQueryHandler(show_cars, pattern='^body_'))
    application.add_handler(contact_manager_handler)
    application.add_handler(CallbackQueryHandler(return_to_main_menu_callback, pattern='^start$'))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()