from typing import List

from app.dto import Base, MenuCategory


class RestaurantBase(Base):
    name: str
    address: str
    is_verified: bool
    address: str
    latitude: float
    longitude: float
    working_time: str
    description: str


class RestaurantCreate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int
    menu_categories: List['MenuCategory'] = []
