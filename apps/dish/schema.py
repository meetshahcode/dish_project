from pydantic import BaseModel, EmailStr
from datetime import datetime

class DishBase(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    source: str
    calories: float
    carbs: float
    protein: float
    fat: float

    model_config = {
        "from_attributes": True
    }

class DishCreate(DishBase):
    id: int 
    created_at: datetime 
    updated_at: datetime


class DishUpdate(DishBase):
    id: int

class DishResponse(DishBase):
    id: int
    created_at: datetime
    updated_at: datetime