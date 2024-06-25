from typing import List
from datetime import datetime

from app.dto import Base


class Discount(Base):
    dish_id: int
    start_time: datetime
    end_time: datetime
    discounted_price: float


class MenuCategory(Base):
    id: int
    name: str
    restaurant_id: int
    dishes: List['Dish'] = []


class Dish(Base):
    id: int
    name: str
    price: float
    category_id: int
    parameters: List['ProductParameter'] = []
    discounts: List['Discount'] = []


class ProductParameter(Base):
    id: int
    dish_id: int
    key: str
    value: str
