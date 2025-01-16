import re
from typing import Optional

async def validate_phone(phone: str) -> bool:
    """
    Валидация номера телефона
    
    Args:
        phone: Номер телефона для проверки
        
    Returns:
        bool: True если номер валидный, False если нет
    """
    if not phone:
        return False
        
    # Удаляем все пробелы и дефисы
    phone = phone.replace(' ', '').replace('-', '')
    
    # Проверяем формат +7XXXXXXXXXX
    pattern = r'^\+7\d{10}$'
    return bool(re.match(pattern, phone))