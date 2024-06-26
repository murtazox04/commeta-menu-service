from typing import List
from pydantic import Field
from datetime import datetime

from app.dto import Base


class Discount(Base):
    dishId: int = Field(alias='dish_id')
    startDate: datetime = Field(alias='start_date')
    endDate: datetime = Field(alias='end_date')
    price: float


class MenuCategory(Base):
    name: str
    restaurantId: int = Field(alias='restaurant_id')
    dishes: List['Dish'] = []


class Dish(Base):
    name: str
    price: float
    categoryId: int = Field(alias='category_id')


class ProductParameter(Base):
    dishId: int = Field(alias='dish_id')
    key: str
    value: str
