from supabase.client import create_client, Client
from typing import List, Dict, Any
from app.config import SUPABASE_URL, SUPABASE_KEY

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async def get_cars(self, filters: Dict[str, Any], limit: int = 3, offset: int = 0) -> List[Dict]:
        query = self.client.table('cars').select('*')
        
        if filters.get('category'):
            query = query.eq('category', filters['category'])
            
        specs = filters.get('specs', {})
        if specs.get('driveType'):
            query = query.eq('specs->>driveType', specs['driveType'])
        if specs.get('fuelType'):
            query = query.eq('specs->>fuelType', specs['fuelType'])
            
        query = query.limit(limit).offset(offset)
        
        result = query.execute()
        return result.data

    async def add_to_favorites(self, user_id: int, car_id: str) -> bool:
        """Добавление автомобиля в избранное"""
        try:
            result = self.client.table('favorites').insert({
                'user_id': user_id,
                'car_id': car_id
            }).execute()
            return bool(result.data)
        except Exception:
            return False

    async def remove_from_favorites(self, user_id: int, car_id: str) -> bool:
        """Удаление автомобиля из избранного"""
        try:
            result = self.client.table('favorites')\
                .delete()\
                .eq('user_id', user_id)\
                .eq('car_id', car_id)\
                .execute()
            return bool(result.data)
        except Exception:
            return False

    async def get_favorites(self, user_id: int) -> List[Dict]:
        """Получение списка избранных автомобилей пользователя"""
        try:
            result = self.client.table('favorites')\
                .select('cars(*)')\
                .eq('user_id', user_id)\
                .execute()
            return [item['cars'] for item in result.data]
        except Exception:
            return []

    async def is_favorite(self, user_id: int, car_id: str) -> bool:
        """Проверка, находится ли автомобиль в избранном"""
        result = self.client.table('favorites')\
            .select('id')\
            .eq('user_id', user_id)\
            .eq('car_id', car_id)\
            .execute()
        return bool(result.data)

    async def get_currency_rates(self) -> Dict[str, float]:
        """Получение текущих курсов валют"""
        try:
            result = self.client.table('currency_rates')\
                .select('currency_code, rate')\
                .execute()
            return {item['currency_code']: float(item['rate']) for item in result.data}
        except Exception:
            return {}

    async def update_currency_rate(self, currency_code: str, new_rate: float) -> bool:
        """Обновление курса валюты"""
        try:
            result = self.client.table('currency_rates')\
                .update({'rate': new_rate})\
                .eq('currency_code', currency_code)\
                .execute()
            return bool(result.data)
        except Exception:
            return False

    async def get_single_currency_rate(self, currency_code: str) -> float | None:
        """Получение курса конкретной валюты"""
        try:
            result = self.client.table('currency_rates')\
                .select('rate')\
                .eq('currency_code', currency_code)\
                .execute()
            return float(result.data[0]['rate']) if result.data else None
        except Exception:
            return None