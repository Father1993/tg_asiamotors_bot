# Asia Motors Telegram Bot

## Описание

Telegram бот для компании Asia Motors, специализирующейся на продаже и поставке автомобилей из Китая. Бот предоставляет полный спектр услуг: от подбора автомобиля до расчета итоговой стоимости с учетом всех таможенных платежей и дополнительных расходов.

## Ключевые особенности

### 🚗 Каталог автомобилей

-   Интеграция с Supabase для хранения и управления каталогом
-   Автоматическая синхронизация с сайтом компании
-   Удобная пагинация и фильтрация
-   Детальные карточки автомобилей с характеристиками

### 💰 Калькулятор стоимости "под ключ"

-   Динамический расчет с актуальными курсами валют
-   Интеграция с базой данных Supabase для хранения курсов
-   Расчет таможенных платежей и пошлин для разных категорий авто:
    -   Новые автомобили (до 3 лет)
    -   Подержанные (3-5 лет)
    -   Старые (более 5 лет)
-   Учет всех расходов:
    -   Стоимость автомобиля в юанях
    -   Таможенные платежи в евро
    -   Фиксированная комиссия компании
    -   Расходы в Китае и России

### 👨‍💼 Панель администратора

-   Команда `/admin` для доступа к панели управления
-   Управление курсами валют в реальном времени:
    -   Просмотр текущих курсов CNY и EUR
    -   Редактирование курсов через удобный интерфейс
    -   Автоматическое обновление в калькуляторе
-   Система кэширования для оптимизации запросов
-   Защита доступа по ID администратора

### Дополнительный функционал

-   ⭐ Избранное: сохранение интересующих автомобилей
-   🔔 Система уведомлений о новых поступлениях и изменениях цен
-   ❓ FAQ с автоматическими ответами на популярные вопросы
-   📋 Умный опросник для подбора автомобиля
-   💬 Техническая поддержка с уведомлением менеджеров

## Технический стек

### Backend

-   Python 3.12
-   aiogram 3.x (асинхронный фреймворк для Telegram Bot API)
-   Supabase (PostgreSQL + REST API)
-   FSM (Finite State Machine) для управления состояниями диалогов

### Инфраструктура

-   Docker & Docker Compose
-   GitHub Actions для CI/CD
-   Логирование с использованием стандартной библиотеки logging

## Установка и запуск

### Предварительные требования

-   Python 3.12+
-   Supabase аккаунт
-   Telegram Bot Token
-   ID администратора в Telegram

### Шаги по установке

1. Клонируйте репозиторий:

```bash
git clone [repository-url]
```

2. Настройте переменные окружения:

```bash
cp example.env .env
```

3. Заполните .env файл:

```env
# Telegram Bot
BOT_TOKEN=your_bot_token

# Admin Settings
ADMIN_IDS=your_admin_id
ADMIN_USERNAME=your_username

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Logging
LOG_LEVEL=INFO
```

4. Создайте необходимые таблицы в Supabase:

```sql
-- Таблица курсов валют
create table currency_rates (
    id uuid default uuid_generate_v4() primary key,
    currency_code text not null,
    rate decimal not null,
    updated_at timestamp with time zone default now(),
    created_at timestamp with time zone default now()
);

-- Создаем уникальный индекс по коду валюты
create unique index currency_rates_currency_code_idx on currency_rates(currency_code);
```

5. Установите зависимости:

```bash
pip install -r requirements.txt
```

6. Запустите бота:

```bash
python main.py
```

## Структура проекта

```
tg_am_bot/
├── app/
│   ├── handlers/         # Обработчики команд
│   │   ├── admin.py     # Админ-панель
│   │   ├── calculator.py # Калькулятор
│   │   └── ...
│   ├── keyboards/        # Клавиатуры и кнопки
│   ├── services/         # Бизнес-логика
│   │   ├── calculator.py # Сервис расчета стоимости
│   │   └── ...
│   ├── constants/        # Константы и сообщения
│   ├── FSM/             # Конечные автоматы состояний
│   ├── utils/           # Вспомогательные функции
│   │   ├── supabase.py  # Работа с базой данных
│   │   └── validators.py # Валидаторы
│   └── config.py        # Конфигурация
├── .env                 # Переменные окружения
└── requirements.txt     # Зависимости
```

## Разработчик

### Спиней Андрей

-   🔧 Full-stack разработчик
-   💼 Специализация: Python, Telegram Bots, Docker
-   🌟 Ключевые достижения в проекте:
    -   Разработка комплексного калькулятора таможенных платежей
    -   Интеграция с Supabase и создание системы кэширования
    -   Реализация админ-панели для управления курсами валют
    -   Внедрение FSM для управления состояниями диалогов
    -   Оптимизация работы с базой данных
    -   Внедрение системы логирования и мониторинга

## Лицензия

Проект является собственностью компании Asia Motors. Все права защищены.

---

© 2025 Asia Motors. Разработано [Спиней Андреем](https://github.com/Father1993)
