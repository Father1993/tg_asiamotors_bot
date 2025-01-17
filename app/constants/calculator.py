from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class CalculatorConstants:
    """Константы для расчета стоимости авто"""
    CNY_RATE = 14.7  # Курс юаня к рублю
    EUR_RATE = 106.2  # Курс евро к рублю
    COMPANY_COMMISSION_RUB = 100000  # Фиксированная комиссия в рублях
    CHINA_EXPENSES_CNY = 15000  # Расходы в Китае (юани)
    RUSSIA_EXPENSES_RUB = 150000  # Расходы в РФ (рубли)

class DutyRates:
    """Ставки пошлин для разных категорий авто"""
    
    # До 3 лет
    NEW_CARS = [
        {
            'max_price_eur': 8500,
            'duty_rate': 0.54,
            'min_duty_per_cc': 2.5
        },
        {
            'max_price_eur': 16700,
            'duty_rate': 0.48,
            'min_duty_per_cc': 3.5
        },
        {
            'max_price_eur': 42300,
            'duty_rate': 0.48,
            'min_duty_per_cc': 5.5
        },
        {
            'max_price_eur': 84500,
            'duty_rate': 0.48,
            'min_duty_per_cc': 7.5
        },
        {
            'max_price_eur': 169000,
            'duty_rate': 0.48,
            'min_duty_per_cc': 15
        },
        {
            'max_price_eur': float('inf'),
            'duty_rate': 0.48,
            'min_duty_per_cc': 20
        }
    ]
    
    # От 3 до 5 лет
    USED_3_5_YEARS = [
        {
            'max_engine_cc': 1000,
            'duty_per_cc': 1.5
        },
        {
            'max_engine_cc': 1500,
            'duty_per_cc': 1.7
        },
        {
            'max_engine_cc': 1800,
            'duty_per_cc': 2.5
        },
        {
            'max_engine_cc': 2300,
            'duty_per_cc': 2.7
        },
        {
            'max_engine_cc': 3000,
            'duty_per_cc': 3.0
        },
        {
            'max_engine_cc': float('inf'),
            'duty_per_cc': 3.6
        }
    ]
    
    # Более 5 лет
    USED_OVER_5_YEARS = [
        {
            'max_engine_cc': 1000,
            'duty_per_cc': 3.0
        },
        {
            'max_engine_cc': 1500,
            'duty_per_cc': 3.2
        },
        {
            'max_engine_cc': 1800,
            'duty_per_cc': 3.5
        },
        {
            'max_engine_cc': 2300,
            'duty_per_cc': 4.8
        },
        {
            'max_engine_cc': 3000,
            'duty_per_cc': 5.0
        },
        {
            'max_engine_cc': float('inf'),
            'duty_per_cc': 5.7
        }
    ]

class CalculatorMessages:
    """Сообщения для калькулятора"""
    WELCOME = (
        "🧮 Калькулятор стоимости авто из Китая\n\n"
        "Для расчета стоимости мне потребуется несколько параметров.\n"
        "Давайте начнем с года выпуска автомобиля."
    )
    
    ENTER_YEAR = "📅 Введите год выпуска автомобиля (например: 2022):"
    
    ENTER_PRICE = (
        "💰 Введите стоимость автомобиля в юанях (только число):\n"
        "Например: 150000"
    )
    
    ENTER_ENGINE = (
        "🚗 Введите объем двигателя в кубических сантиметрах:\n"
        "Например: 2000"
    )
    
    ENTER_POWER = (
        "⚡️ Введите мощность двигателя в л.с.:\n"
        "Например: 150"
    )
    
    INVALID_YEAR = "❌ Некорректный год. Пожалуйста, введите год в формате YYYY (например: 2022)"
    INVALID_PRICE = "❌ Некорректная цена. Пожалуйста, введите только число"
    INVALID_ENGINE = "❌ Некорректный объем двигателя. Пожалуйста, введите только число"
    INVALID_POWER = "❌ Некорректная мощность. Пожалуйста, введите только число"
    
    RESULT_TEMPLATE = (
        "📊 Расчет стоимости автомобиля:\n\n"
        "🚗 Стоимость авто: {price_rub:,.0f} ₽\n"
        "📦 Таможенная пошлина: {duty:,.0f} ₽\n"
        "💰 Комиссия компании: {commission:,.0f} ₽\n\n"
        "💵 Итоговая стоимость: {total:,.0f} ₽\n\n"
        "ℹ️ Расчет произведен по курсам:\n"
        "CNY: {cny_rate} ₽\n"
        "EUR: {eur_rate} ₽\n\n"
        "❗️Окончательная стоимость может отличаться в зависимости от курсов валют и других факторов"
    ) 