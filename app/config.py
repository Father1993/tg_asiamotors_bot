import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Supabase конфигурация
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# ID администраторов
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))

# URL сайта
WEBSITE_URL = "https://asiamotors.su"
