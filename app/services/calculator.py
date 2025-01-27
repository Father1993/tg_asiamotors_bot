from datetime import datetime
from typing import Dict, Tuple
from app.constants.calculator import CalculatorConstants, DutyRates
from app.utils.supabase import SupabaseService

class CarCalculator:
    """Сервис для расчета стоимости автомобиля"""
    
    def __init__(self):
        self.constants = CalculatorConstants()
        self.db = SupabaseService()
        self._rates_cache = {}
        self._last_rates_update = None
    
    async def _update_rates_cache(self) -> None:
        """Обновление кэша курсов валют"""
        rates = await self.db.get_currency_rates()
        if rates:
            self._rates_cache = rates
            self._last_rates_update = datetime.now()
    
    async def _get_rate(self, currency: str) -> float:
        """Получение курса валюты с возможным обновлением кэша"""
        # Если кэш пустой или прошло больше часа, обновляем
        if (not self._rates_cache or 
            not self._last_rates_update or 
            (datetime.now() - self._last_rates_update).seconds > 3600):
            await self._update_rates_cache()
        
        # Возвращаем курс из кэша или константу как запасной вариант
        return self._rates_cache.get(currency, 
            self.constants.CNY_RATE if currency == 'CNY' else self.constants.EUR_RATE
        )
    
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
    
    async def calculate_total_cost(self, price_cny: float, year: int, engine_cc: int) -> Dict[str, float]:
        """
        Расчет полной стоимости автомобиля
        
        Args:
            price_cny: Цена в юанях
            year: Год выпуска
            engine_cc: Объем двигателя в куб.см
            
        Returns:
            Dict с результатами расчета
        """
        # Получаем актуальные курсы
        cny_rate = await self._get_rate('CNY')
        eur_rate = await self._get_rate('EUR')
        
        # Конвертация в рубли и евро
        price_rub = price_cny * cny_rate
        price_eur = price_cny * cny_rate / eur_rate
        
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
        duty_rub = duty_eur * eur_rate
        
        # Заменяем расчет комиссии на фиксированную сумму
        commission = self.constants.COMPANY_COMMISSION_RUB
        
        # Добавляем расходы
        expenses = (self.constants.CHINA_EXPENSES_CNY * cny_rate + 
                   self.constants.RUSSIA_EXPENSES_RUB)
        
        # Считаем итоговую стоимость
        total = price_rub + duty_rub + commission + expenses
        
        return {
            'price_rub': price_rub,
            'duty': duty_rub,
            'commission': commission,
            'total': total,
            'cny_rate': cny_rate,
            'eur_rate': eur_rate
        } 