from typing import List, Optional
from config.supabase_config import supabase
from models.car import Car
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CarService:
    @staticmethod
    async def get_filtered_cars(
        price_range: Optional[str] = None,
        category: Optional[str] = None,
        country: Optional[str] = None
    ) -> List[Car]:
        """
        Получает отфильтрованные автомобили из базы данных
        """
        try:
            # Начинаем запрос
            query = supabase.table('cars').select('*')
            
            # Определяем границы цен
            price_limits = {
                'economy': (0, 1500000),
                'medium': (1500000, 3000000),
                'premium': (3000000, float('inf'))
            }
            
            # Применяем фильтры
            if price_range and price_range in price_limits:
                min_price, max_price = price_limits[price_range]
                query = query.gte('price', min_price).lt('price', max_price)
            
            # Маппинг категорий
            if category:
                category_mapping = {
                    'sedan': 'Седаны',
                    'crossover': 'Кроссоверы',
                    'minivan': 'Минивэны',
                    'suv': 'Внедорожники',
                    'electric': 'Электромобили'
                }
                mapped_category = category_mapping.get(category)
                if mapped_category:
                    query = query.eq('category', mapped_category)
            
            # Фильтр по стране
            if country:
                query = query.eq('country', country)
            
            # Получаем только доступные автомобили
            query = query.eq('available', True)
            
            # Выполняем запрос
            response = query.execute()
        
            if not response.data:
                logger.info("No cars found with given filters")
                return []
                
            return [Car(**car) for car in response.data]
            
        except Exception as e:
            logging.error(f"Error fetching cars: {str(e)}")
            return []
        
    @staticmethod
    async def get_car_by_id(car_id: str) -> Optional[Car]:
      """
      Получает автомобиль по ID
      """
      try:
          response = supabase.table('cars').select('*').eq('id', car_id).single().execute()
          return Car(**response.data) if response.data else None
      except Exception as e:
          logging.error(f"Error fetching car by ID {car_id}: {str(e)}")
          return None
    @staticmethod
    async def get_cars_by_ids(car_ids: List[str]) -> List[Car]:
      """
      Получает список автомобилей по их ID (для избранного)
      """
      try:
          response = supabase.table('cars').select('*').in_('id', car_ids).execute()
          return [Car(**car) for car in response.data]
      except Exception as e:
          logging.error(f"Error fetching cars by IDs: {str(e)}")
          return []