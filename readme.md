# Бот для подбора автомобиля 🚗

Телеграм-бот, который помогает пользователям выбрать автомобиль на основе их бюджета и типа кузова из коллекции автомобилей, доступных в Китае.

## Функции

-   🏠 **Главное меню**: Предлагает варианты для выбора автомобиля, калькуляции цен, прохождения опроса или связи с менеджером.
-   💰 **Выбор автомобиля**: Возможность выбора автомобилей по бюджету (до 1.5 млн, 1.5 млн - 3 млн, выше 3 млн) и типу кузова (седан или кроссовер).
-   📋 **Опрос**: Пользователи могут пройти опрос для получения персонализированных рекомендаций.
-   👨‍💼 **Связаться с менеджером**: Возможность связи с менеджером для дальнейших консультаций.
-   🔢 **Калькулятор стоимости**: Оценка полной стоимости выбранных автомобилей.

## Используемые технологии

-   Python
-   [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) для интеграции с API Telegram
-   [python-dotenv](https://github.com/theskumar/python-dotenv) для управления переменными окружения
-   Логирование для отслеживания ошибок
-   Pandas для обработки данных

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/your-username/car-selection-bot.git
    cd car-selection-bot
    ```

2. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

3. Создайте файл `.env` и добавьте токен вашего бота (получите его от [BotFather](https://core.telegram.org/bots#botfather)):

    ```bash
    TELEGRAM_TOKEN=your_telegram_bot_token
    ```

4. Запустите бота:

    ```bash
    python bot.py
    ```

## Обзор кода

### Ключевые функции

-   **`start(update, context)`**: Отображает главное меню с вариантами для начала подбора автомобиля, использования калькулятора, прохождения опроса или связи с менеджером.
-   **`car_selection(update, context)`**: Запрашивает у пользователя выбор бюджета.
-   **`select_body_type(update, context)`**: Позволяет выбрать тип кузова (седан или кроссовер).
-   **`show_cars(update, context)`**: Показывает автомобили на основе выбранного бюджета и типа кузова с подробной информацией, такой как название, цена и год выпуска.

### Пример взаимодействия

1. Пользователь запускает бота, отправляя команду `/start`.
2. Бот запрашивает **бюджет** и **тип кузова**.
3. В зависимости от выбора показываются автомобили, подходящие под выбранные параметры.
4. Пользователь может рассчитать полную стоимость или вернуться в главное меню.

## Переменные окружения

-   **`TELEGRAM_TOKEN`**: Токен вашего бота, полученный от [BotFather](https://core.telegram.org/bots#botfather).

## Вклад в проект

Не стесняйтесь форкать репозиторий и создавать pull request для улучшений или исправлений ошибок. Внесение вклада приветствуется!

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для подробностей.
