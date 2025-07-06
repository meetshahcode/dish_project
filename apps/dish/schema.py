from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    source: Optional[str] = None
    calories: float
    carbs: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None


    model_config = {
        "from_attributes": True
    }

    @field_validator('calories')
    @classmethod
    def calories_must_be_positive(cls, v):
        if v is None or v <= 0:
            raise ValueError('calories must be a positive, non-zero float')
        return v

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