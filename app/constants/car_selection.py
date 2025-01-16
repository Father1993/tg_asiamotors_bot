class SelectionMessages:
    """Константы для сообщений подбора автомобиля"""
    WELCOME = (
        "🚗 Добро пожаловать в умный подбор автомобиля!\n\n"
        "Я задам вам несколько вопросов, чтобы подобрать идеальный автомобиль, "
        "который будет соответствовать вашему стилю жизни и потребностям.\n\n"
        "💫 Для начала, выберите, какой образ жизни вам ближе всего:"
    )
    
    BUDGET_QUESTION = (
        "💰 Отлично! Теперь давайте определимся с бюджетом.\n"
        "Выберите подходящий диапазон:"
    )
    
    PASSENGERS_QUESTION = "👥 Сколько пассажиров обычно будет в автомобиле?"
    
    USAGE_QUESTION = "🛣 Где вы планируете чаще всего использовать автомобиль?"
    
    PRIORITIES_QUESTION = "⭐️ И последний вопрос: что для вас наиболее важно в автомобиле?"
    
    RECOMMENDATIONS_TEMPLATE = (
        "{lifestyle_emoji} На основе ваших ответов, я подобрал для вас идеальные варианты!\n\n"
        "🏆 Топ рекомендации:\n"
        "{recommendations}\n"
        "🌐 Узнайте больше об этих моделях на нашем сайте:\n"
        "{website_url}/catalog\n\n"
        "💡 На сайте вы найдете:\n"
        "• Подробные характеристики\n"
        "• Фотографии и видео\n"
        "• Комплектации и цены\n"
    )

class SelectionOptions:
    """Варианты ответов для разных категорий"""
    LIFESTYLES = {
        "🏢 Городской житель": ["HAVAL JOLION", "CHERY TIGGO 4 PRO", "CHERY TIGGO 7 PRO"],
        "👨‍👩‍👧‍👦 Семьянин": ["HAVAL H9", "EXEED VX", "GAC GS8"],
        "💼 Бизнесмен": ["HONGQI H9", "EXEED TXL", "TANK 300"],
        "🏔 Путешественник": ["HAVAL DARGO", "TANK 500", "GWM POER"],
        "🌟 Ценитель премиум": ["HONGQI E-HS9", "VOYAH FREE", "EXEED VX"]
    }

    BUDGETS = {
        "До 3 млн ₽": ["HAVAL JOLION", "CHERY TIGGO 4 PRO"],
        "3-4 млн ₽": ["HAVAL DARGO", "EXEED TXL", "CHERY TIGGO 8 PRO MAX"],
        "4-5 млн ₽": ["TANK 300", "EXEED VX", "GAC GS8"],
        "Более 5 млн ₽": ["HONGQI H9", "VOYAH FREE", "TANK 500"]
    }

    PASSENGERS = {
        "1-2 человека": ["HAVAL JOLION", "CHERY TIGGO 4 PRO"],
        "3-4 человека": ["HAVAL DARGO", "EXEED TXL"],
        "5 и более": ["EXEED VX", "GAC GS8", "TANK 500"]
    }

    USAGE = {
        "🏙 Город": ["HAVAL JOLION", "CHERY TIGGO 4 PRO"],
        "🛣 Трасса": ["HONGQI H9", "EXEED TXL"],
        "🏔 Бездорожье": ["TANK 300", "TANK 500", "GWM POER"],
        "🏠 Загород": ["HAVAL H9", "GAC GS8"]
    }

    PRIORITIES = {
        "💰 Экономичность": ["HAVAL JOLION", "CHERY TIGGO 4 PRO"],
        "🛡 Безопасность": ["EXEED VX", "VOYAH FREE"],
        "🎯 Надежность": ["TANK 300", "HAVAL H9"],
        "✨ Престиж": ["HONGQI H9", "HONGQI E-HS9"]
    }