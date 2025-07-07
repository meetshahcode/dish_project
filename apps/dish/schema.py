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


class GetDishRequest(BaseModel):
    dish_name: str
    servings: int

    @field_validator('dish_name')
    @classmethod
    def dish_name_must_not_be_empty(cls, v):
        v = v.strip()
        if not v or v.strip() == "" or len(v.strip()) == 0:
            raise ValueError('dish_name must not be empty')
        if len(v) > 10**5:
            raise ValueError('dish_name must not exceed 100,000 characters')
        return v

    @field_validator('servings')
    @classmethod
    def servings_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('invalid servings, must be a positive integer')
        return v
    
class GetDishResponse(BaseModel):
    dish_name: str
    servings: int
    calories_per_serving: int
    carbs_per_serving: Optional[int] = None
    protein_per_serving: Optional[int] = None
    fat_per_serving: Optional[int] = None