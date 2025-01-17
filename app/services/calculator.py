from datetime import datetime
from typing import Dict, Tuple
from app.constants.calculator import CalculatorConstants, DutyRates

class CarCalculator:
    """Сервис для расчета стоимости автомобиля"""
    
    def __init__(self):
        self.constants = CalculatorConstants()
    
    def _get_car_age_category(self, year: int) -> str:
        """Определяет категорию возраста автомобиля"""
        current_year = datetime.now().year
        age = current_year - year
        
        if age <= 3:
            return "new"
        elif age <= 5:
            return "used_3_5"
        else:
            return "used_over_5"
    
    def _calculate_duty_new_car(self, price_eur: float, engine_cc: int) -> float:
        """Расчет пошлины для новых авто"""
        for rate in DutyRates.NEW_CARS:
            if price_eur <= rate['max_price_eur']:
                # Расчет по ставке
                duty_by_price = price_eur * rate['duty_rate']
                # Расчет по минимальной ставке за куб.см
                duty_by_cc = engine_cc * rate['min_duty_per_cc']
                # Выбираем большее значение
                return max(duty_by_price, duty_by_cc)
        return 0
    
    def _calculate_duty_used_car(self, engine_cc: int, is_over_5_years: bool) -> float:
        """Расчет пошлины для подержанных авто"""
        rates = DutyRates.USED_OVER_5_YEARS if is_over_5_years else DutyRates.USED_3_5_YEARS
        
        for rate in rates:
            if engine_cc <= rate['max_engine_cc']:
                return engine_cc * rate['duty_per_cc']
        return 0
    
    def calculate_total_cost(self, price_cny: float, year: int, engine_cc: int) -> Dict[str, float]:
        """
        Расчет полной стоимости автомобиля
        
        Args:
            price_cny: Цена в юанях
            year: Год выпуска
            engine_cc: Объем двигателя в куб.см
            
        Returns:
            Dict с результатами расчета
        """
        # Конвертация в рубли и евро
        price_rub = price_cny * self.constants.CNY_RATE
        price_eur = price_cny * self.constants.CNY_RATE / self.constants.EUR_RATE
        
        # Определяем категорию по возрасту
        age_category = self._get_car_age_category(year)
        
        # Расчет таможенной пошлины
        if age_category == "new":
            duty_eur = self._calculate_duty_new_car(price_eur, engine_cc)
        else:
            duty_eur = self._calculate_duty_used_car(
                engine_cc, 
                is_over_5_years=(age_category == "used_over_5")
            )
        
        # Конвертируем пошлину в рубли
        duty_rub = duty_eur * self.constants.EUR_RATE
        
        # Заменяем расчет комиссии на фиксированную сумму
        commission = self.constants.COMPANY_COMMISSION_RUB
        
        # Добавляем расходы
        expenses = (self.constants.CHINA_EXPENSES_CNY * self.constants.CNY_RATE + 
                   self.constants.RUSSIA_EXPENSES_RUB)
        
        # Считаем итоговую стоимость
        total = price_rub + duty_rub + commission + expenses
        
        return {
            'price_rub': price_rub,
            'duty': duty_rub,
            'commission': commission,
            'total': total,
            'cny_rate': self.constants.CNY_RATE,
            'eur_rate': self.constants.EUR_RATE
        } 