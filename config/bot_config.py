from dotenv import load_dotenv
import os
import logging

# Загрузка переменных окружения
load_dotenv()

# Конфигурация бота
TOKEN = os.getenv('TELEGRAM_TOKEN')
MANAGER_ID = os.getenv('TELEGRAM_MANAGER_ID')
MANAGER_USERNAME = os.getenv('TELEGRAM_MANAGER_USERNAME')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния разговора
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