class FAQMessages:
    """Константы для текстовых сообщений FAQ раздела"""
    MAIN_MENU = "❓ Часто задаваемые вопросы\n\nВыберите интересующий вас вопрос:"
    ERROR = "Произошла ошибка. Попробуйте еще раз."
    NOT_FOUND = "Вопрос не найден. Пожалуйста, выберите другой вопрос."
    MAIN_MENU_PROMPT = "Выберите нужный раздел:" 

class SurveyMessages:
    WELCOME = (
        "🎁 Добро пожаловать в наш опрос!\n\n"
        "Пройдите короткий опрос и получите гарантированную скидку 10 000₽ "
        "на покупку автомобиля в нашей компании!\n\n"
        "👤 Как мы можем к вам обращаться? Введите ваше имя:"
    )
    PHONE_REQUEST = "📱 Спасибо! Для получения скидки, оставьте ваш номер телефона:\nФормат: +7XXXXXXXXXX"
    INVALID_PHONE = "❌ Неверный формат номера. Пожалуйста, используйте формат: +7XXXXXXXXXX"
    BUDGET_QUESTION = "💰 Какой бюджет вы рассматриваете для покупки автомобиля?"
    TIMEFRAME_QUESTION = "🕒 Когда планируете приобретение автомобиля?"
    CURRENT_CAR_QUESTION = "🚗 Какой автомобиль вы используете сейчас?"
    FEATURES_QUESTION = "⭐️ Какие характеристики автомобиля для вас наиболее важны?"
    PURPOSE_QUESTION = "🎯 Для каких целей вы планируете использовать новый автомобиль?"
    CONCERNS_QUESTION = "❓ Что вас больше всего беспокоит при выборе автомобиля из Китая?"
    CONTACT_TIME_QUESTION = "📞 В какое время вам удобнее получить консультацию нашего специалиста?"
    SURVEY_COMPLETE = (
        "🎉 Поздравляем! Вы успешно прошли опрос!\n\n"
        "Ваш промокод на скидку 10 000₽: `{discount_code}`\n\n"
        "💡 Наш менеджер свяжется с вами в указанное время: {contact_time}\n\n"
        "Спасибо за участие в опросе! Ждем вас в нашем офисе!"
    )