

from apps.dish import models
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.user import schema as UserSchema
from apps.dish import schema
from apps.user.jwt import get_current_user
from database import get_db


router = APIRouter(tags=["Dish"],prefix="")

@router.post("/add", response_model=schema.DishCreate)
async def add_dish(dish: schema.DishBase, 
             current_user: UserSchema.User = Depends(get_current_user),
             db: AsyncSession = Depends(get_db)):
    """
        Add a new dish to the menu.
    """
    dish = models.Dish(**dish.model_dump(), created_by=current_user.id)
    dish.created_by = current_user.id
    dish.updated_by = current_user.id
    await dish.save(db=db)
    dish_schema = schema.DishCreate.model_validate(dish.__dict__)
    return dish_schema

@router.get("/basic_search", response_model=schema.DishCreate)
async def search_dish(name: str, 
                      db: AsyncSession = Depends(get_db),
                      current_user: UserSchema.User = Depends(get_current_user)):
    """
        Search for a dish by name.
    """
    dish = await models.Dish.find_by_name(db, name)
    if not dish:
        return {"message": "Dish not found"}
    dish_schema = schema.DishCreate.model_validate(dish.__dict__)
    return dish_schema


@router.get("/search", response_model=list[schema.DishCreate])
async def fuzzy_search_dish(query: str, 
                            serving_size: int,
                            db: AsyncSession = Depends(get_db),
                            current_user: UserSchema.User = Depends(get_current_user)):
    """
        Fuzzy search for dishes by name.
    """
    dishes = await models.Dish.fuzzy_search(db, query=query)
    if not dishes:
        return {"message": "No dishes found"}
    
    res = []
    for dish in dishes:
        dish.cal_nutrition_per_serving(serving_size=serving_size)
        res.append(schema.DishCreate.model_validate(dish.__dict__))
    return res

@router.delete("/delete/{dish_id}", response_class=dict)
async def delete_dish(dish_id: int, 
                       db: AsyncSession = Depends(get_db),
                       current_user: UserSchema.User = Depends(get_current_user)):
    """
        Delete a dish from the menu.
    """
    dish = await models.Dish.find_by_id(db, dish_id)
    if not dish:
        return {"message": "Dish not found"}
    await dish.delete(db=db)
    return {"message": "Dish deleted successfully"}

@router.patch("/update/{dish_id}", response_model=schema.DishCreate)
async def update_dish(dish_id: int, 
                       dish: schema.DishUpdate, 
                       db: AsyncSession = Depends(get_db),
                       current_user: UserSchema.User = Depends(get_current_user)):
    """
        Update a dish in the menu.
    """
    return await models.Dish.update(db, dish_id, dish)