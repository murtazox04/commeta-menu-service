from pydantic import Field
from datetime import datetime

from app.dto import Base


class Discount(Base):
    dish_id: int = Field(
        alias='dishId',
        title='Dish ID',
        description='The ID of the dish',
    )
    start_date: datetime = Field(
        alias='startDate',
        title='Start Date',
        description='The start date of the dish discount',
    )
    end_date: datetime = Field(
        alias='endDate',
        title='End Date',
        description='The end date of the dish discount',
    )
    price: float = Field(
        title='Price',
        description='The price of the discount',
    )
    is_active: bool = Field(
        alias='isActive',
        title='Active',
        description='Whether the discount is active',
        default=True
    )


class Dish(Base):
    name: str = Field(
        title='Name',
        description='The name of the dish',
    )
    price: float = Field(
        title='Price',
        description='The price of the dish',
    )
    category_id: int = Field(
        alias='categoryId',
        title='Category ID',
        description='The ID of the category',
    )


class MenuCategory(Base):
    name: str = Field(
        title='Name',
        description='The name of the menu category',
    )
    restaurant_id: int = Field(
        alias='restaurantId',
        title='Restaurant ID',
        description='The ID of the restaurant',
    )


class DishParameter(Base):
    dish_id: int = Field(
        alias='dishId',
        title='Dish ID',
        description='The ID of the dish parameter',
    )
    key: str = Field(
        title='Key',
        description='The key of the parameter',
        examples=["weight", "calories"]
    )
    value: str = Field(
        title='Value',
        description='The value of the parameter',
        examples=["500gr", "30kkal"]
    )
