from apps.dish import models
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.user import schema as UserSchema
from apps.dish import schema
from apps.user.jwt import get_current_user
from database import get_db
from fastapi_limiter.depends import RateLimiter
from fastapi_redis_cache import cache


router = APIRouter(tags=["Dish"],prefix="")

@router.post("/add", response_model=schema.DishResponse, dependencies=[Depends(RateLimiter(times=15, seconds=60))])
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
    dish_schema = schema.DishResponse.model_validate(dish.__dict__)
    return dish_schema

@router.get("/basic_search", response_model=schema.DishResponse, dependencies=[Depends(RateLimiter(times=15, seconds=60))])
@cache(expire=100)
async def search_dish(name: str, 
                      db: AsyncSession = Depends(get_db),
                      current_user: UserSchema.User = Depends(get_current_user)):
    """
        Search for a dish by name.
    """
    dish = await models.Dish.find_by_name(db, name)
    if not dish:
        return {"message": "Dish not found"}
    dish_schema = schema.DishResponse.model_validate(dish.__dict__)
    return dish_schema


@router.get("/search", response_model=list[schema.DishResponse],  dependencies=[Depends(RateLimiter(times=15, seconds=60))])
@cache(expire=100)
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
        res.append(schema.DishResponse.model_validate(dish.__dict__))
    return res

@router.delete("/delete/{dish_id}", dependencies=[Depends(RateLimiter(times=15, seconds=60))])
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

@router.post("/get-calories", response_model=list[schema.GetDishResponse],  dependencies=[Depends(RateLimiter(times=15, seconds=60))])
@cache(expire=100)
async def get_dish_calories(req: schema.GetDishRequest,
                            db: AsyncSession = Depends(get_db),
                            current_user: UserSchema.User = Depends(get_current_user)):
    """
        Get the calories for a dish by name.
    """
    dishes = await models.Dish.fuzzy_search(db, req.dish_name)
    if not dishes:
        return {"message": "Dish not found"}
    res = []
    for dish in dishes:
        res.append(dish.toGetDishResponse(servings=req.servings))
    print("res", res)
    return res
