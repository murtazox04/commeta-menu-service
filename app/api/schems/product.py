from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DiscountCreateUpdate(BaseModel):
    dish_id: int = Field(
        alias="dishId",
        title="Dish ID",
        description="The ID of the associated dish"
    )
    start_date: Optional[datetime] = Field(
        alias="startDate",
        title="Start Date",
        description="Start date of the discount validity"
    )
    end_date: datetime = Field(
        alias="endDate",
        title="End Date",
        description="End date of the discount validity"
    )
    price: float = Field(
        title="Price",
        description="Discounted price of the dish"
    )
    is_active: bool = Field(
        alias='isActive',
        title="Is Active",
        description="Whether the discount is active",
        default=True
    )


class MenuCategoryCreateUpdate(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the menu category",
        min_length=1,
        max_length=100
    )
    restaurant_id: int = Field(
        alias="restaurantId",
        title="Restaurant ID",
        description="The ID of the associated restaurant"
    )


class DishCreateUpdate(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the dish",
        min_length=1,
        max_length=100
    )
    price: float = Field(
        title="Price",
        description="The price of the dish"
    )
    category_id: int = Field(
        alias="categoryId",
        title="Category ID",
        description="The ID of the associated menu category"
    )


class DishParameterCreateUpdate(BaseModel):
    dish_id: int = Field(
        alias="dishId",
        title="Dish ID",
        description="The ID of the associated dish"
    )
    key: str = Field(
        title="Key",
        description="Key or name of the parameter",
        min_length=1,
        max_length=100
    )
    value: str = Field(
        title="Value",
        description="Value associated with the parameter",
        max_length=255
    )
