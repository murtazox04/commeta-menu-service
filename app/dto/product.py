from pydantic import Field
from datetime import datetime
from typing import List, Optional

from app.dto import Base


class Parameter(Base):
    name: str = Field(
        title='Name',
        description='The name of the parameters',
    )


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


class DishParameter(Base):
    dish_id: int = Field(
        alias='dishId',
        title='Dish ID',
        description='The ID of the dish parameter',
    )
    value: str = Field(
        title='Value',
        description='The value of the parameter',
        examples=["500gr", "30kkal"]
    )
    key: Optional[Parameter] = Field(
        title='Key parameter',
        description='The key parameter of the parameter',
        default=None
    )


class Dish(Base):
    name: str = Field(
        title='Name',
        description='The name of the dish',
    )
    restaurant_id: int = Field(
        alias='restaurantId',
        title='Restaurant ID',
        description='The ID of the restaurants',
    )
    price: float = Field(
        title='Price',
        description='The price of the dish',
    )
    menu_id: int = Field(
        alias='menuId',
        title='Category ID',
        description='The ID of the category',
    )
    discounted_price: Optional[float] = Field(
        alias='discountedPrice',
        title='Discounted Price',
        description='The discounted price of the dish',
        default=None
    )
    params: Optional[List[DishParameter]] = Field(
        title='Dish Parameters',
        description='The parameters of the dish',
        default=[]
    )


class Menu(Base):
    name: str = Field(
        title='Name',
        description='The name of the menu',
    )
