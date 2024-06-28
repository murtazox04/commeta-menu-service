from uuid import UUID
from typing import List
from datetime import datetime
from pydantic import Field, BaseModel

from .base import Base, serialize_time


class CartItem(Base):
    dish_id: int = Field(
        alias='dishId',
        title='Dish ID',
        description='The ID of the dish',
    )
    quantity: int = Field(
        title='Quantity',
        description='The quantity of the dish',
    )
    total_cost: float = Field(
        alias='totalCost',
        title='Total Cost',
        description='The total cost of the cart item',
        default=None
    )


class Cart(BaseModel):
    guid: UUID = Field(
        title='GUID',
        description='The ID of the cart',
    )
    items: List[CartItem] = Field(
        default=[],
        title='Cart items',
        description='The list of cart items',
    )
    total_cost: float = Field(
        alias='totalCost',
        title='Total Cost',
        description='The total cost of the cart item',
        default=None
    )
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        json_encoders = {
            datetime: serialize_time
        }
        from_attributes = True
        populate_by_name = True
