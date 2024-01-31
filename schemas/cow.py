from pydantic import BaseModel
from datetime import datetime, date
from typing import Dict, Optional

class Cow(BaseModel):
    name: str
    sex: str
    birthdate: date
    condition: str
    has_calf: bool

    class Config:
        from_attributes = True
        
class Weight(BaseModel):
    mass_kg: int
    last_measured: datetime

class Feeding(BaseModel):
    amout_kg: int
    corn_schedule: str
    last_measured: datetime
    
class Milk_production(BaseModel):
    last_milk: datetime
    cron_schedule: str
    amount_l: int
    
class CowInfo(BaseModel):
    name: str
    sex: str
    birthdate: date
    condition: str
    weight: Weight
    feeding: Feeding
    milk_production: Milk_production
    has_calves: bool
