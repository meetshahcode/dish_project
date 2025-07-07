
import datetime

from apps.user.schema import User
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.user.utils import utcnow
from apps.dish.schema import GetDishResponse
from sqlalchemy import ForeignKey

class Dish(Base):
    __tablename__ = "dishes"
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(default=0.0)
    image_url: Mapped[str] = mapped_column(nullable=True)
    source: Mapped[str] = mapped_column(nullable=True)
    calories: Mapped[float] = mapped_column(default=0.0)
    carbs: Mapped[float] = mapped_column(default=0.0)
    protein: Mapped[float] = mapped_column(default=0.0)
    fat: Mapped[float] = mapped_column(default=0.0)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=utcnow())
    updated_at: Mapped[datetime.datetime] = mapped_column(default=utcnow(), onupdate=utcnow())

    @classmethod
    async def find_by_name(cls, db: AsyncSession, name: str):
        query = select(cls).where(cls.name == name)
        result = await db.execute(query)
        return result.scalars().first()
    
    @classmethod
    async def fuzzy_search(cls, db: AsyncSession, query: str):
        query = select(cls).where(cls.name.ilike(f"%{query}%"))
        result = await db.execute(query)
        return result.scalars().all()

    
    def cal_nutrition_per_serving(self, serving_size: float) -> dict:
        """
        Calculate nutrition values per serving based on the total nutrition and serving size.
        """
        if serving_size <= 0:
            raise ValueError("Serving size must be greater than zero.")
        return {
            "calories": str(self.calories * serving_size) + " kcal",
            "carbs": str(self.carbs * serving_size) + " g",
            "protein": str(self.protein * serving_size) + " g",
            "fat": str(self.fat * serving_size) + " g"
        }
    
    def toGetDishResponse(self, servings: int) -> GetDishResponse:
        """
        Convert the dish to a GetDishResponse format.
        """
        self.cal_nutrition_per_serving(servings)
        return GetDishResponse(
            dish_name=self.name,
            servings=servings,
            calories_per_serving=int(self.calories),
            carbs_per_serving=int(self.carbs),
            protein_per_serving=int(self.protein),
            fat_per_serving=int(self.fat)
        )