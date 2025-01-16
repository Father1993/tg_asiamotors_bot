from typing import List, Dict, Any
from app.constants.car_selection import SelectionOptions

class CarSelector:
    """Сервис для подбора автомобилей"""
    
    @staticmethod
    def get_car_recommendations(user_data: Dict[str, Any]) -> List[str]:
        """
        Анализирует ответы пользователя и возвращает рекомендации
        
        Args:
            user_data: Словарь с ответами пользователя
            
        Returns:
            List[str]: Список рекомендованных автомобилей
        """
        car_scores = {}
        
        # Маппинг категорий к соответствующим словарям опций
        category_mapping = {
            'lifestyle': SelectionOptions.LIFESTYLES,
            'budget': SelectionOptions.BUDGETS,
            'passengers': SelectionOptions.PASSENGERS,
            'usage': SelectionOptions.USAGE,
            'priorities': SelectionOptions.PRIORITIES
        }
        
        # Подсчет очков для каждого автомобиля
        for category, choice in user_data.items():
            if category in category_mapping:
                options = category_mapping[category]
                if choice in options:
                    for car in options[choice]:
                        car_scores[car] = car_scores.get(car, 0) + 1
        
        # Сортировка по количеству совпадений
        sorted_cars = sorted(car_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Возвращаем топ-3 рекомендации
        return [car[0] for car in sorted_cars[:3]]

    @staticmethod
    def format_recommendations(cars: List[str]) -> str:
        """
        Форматирует список рекомендаций
        
        Args:
            cars: Список рекомендованных автомобилей
            
        Returns:
            str: Отформатированный текст рекомендаций
        """
        recommendations_text = ""
        emojis = ["✨", "🌟", "⭐️"]
        
        for i, (car, emoji) in enumerate(zip(cars, emojis), 1):
            recommendations_text += f"{i}. {emoji} {car}\n"
            
        return recommendations_text