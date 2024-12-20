from typing import List, Optional
from pydantic import BaseModel

class CarSpecs(BaseModel):
    mileage: int
    engine_volume: float
    fuel_type: str
    horse_power: int
    transmission: str
    drive_type: str
    color: Optional[str] = None
    generation: Optional[str] = None
    features: Optional[List[str]] = None

class Car(BaseModel):
  id: str
  brand: str
  model: str
  year: int
  category: str
  price: int
  country: str
  images: List[str]
  specs: CarSpecs
  available: bool = True