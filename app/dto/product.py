from typing import List
from pydantic import Field
from datetime import datetime

from app.dto import Base


class Discount(Base):
    dish_id: int = Field(alias='dishId')
    start_date: datetime = Field(alias='startDate')
    end_date: datetime = Field(alias='endDate')
    price: float
    is_active: bool = Field(alias='isActive', default=True)


class Dish(Base):
    name: str
    price: float
    category_id: int = Field(alias='categoryId')


class MenuCategory(Base):
    name: str
    restaurant_id: int = Field(alias='restaurantId')


class DishParameter(Base):
    dish_id: int = Field(alias='dishId')
    key: str
    value: str
