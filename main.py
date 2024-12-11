import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import json
import pandas as pd

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Настраиваем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Создаем словарь для хранения состояний пользователей
user_states = {}

# Данные об автомобилях (в реальном проекте должны храниться в БД)
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

def main():
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(car_selection, pattern='^car_selection$'))
    application.add_handler(CallbackQueryHandler(select_body_type, pattern='^budget_'))
    application.add_handler(CallbackQueryHandler(show_cars, pattern='^body_'))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()