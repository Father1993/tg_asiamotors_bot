import re
from typing import Tuple
from datetime import datetime

async def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Валидация и нормализация номера телефона.
    
    Args:
        phone (str): Номер телефона для проверки
        
    Returns:
        Tuple[bool, str]: (валиден ли номер, нормализованный номер)
    """
    # Убираем все пробелы, дефисы, скобки и другие спецсимволы
    cleaned_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Проверяем, начинается ли номер с 7 или 8
    if cleaned_phone.startswith('8'):
        normalized_phone = '+7' + cleaned_phone[1:]
    elif cleaned_phone.startswith('7'):
        normalized_phone = '+' + cleaned_phone
    elif cleaned_phone.startswith('9'):
        normalized_phone = '+7' + cleaned_phone
    else:
        return False, phone
        
    # Проверяем длину номера (должно быть 11 цифр после нормализации)
    if not re.match(r'^\+7\d{10}$', normalized_phone):
        return False, phone
        
    return True, normalized_phone

def is_valid_year(year: str) -> bool:
    """Проверка корректности года"""
    try:
        year_int = int(year)
        current_year = datetime.now().year
        return 1990 <= year_int <= current_year + 1
    except ValueError:
        return False

def is_valid_number(value: str) -> bool:
    """Проверка, является ли строка положительным числом"""
    try:
        num = float(value)
        return num > 0
    except ValueError:
        return False