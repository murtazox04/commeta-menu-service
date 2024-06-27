from typing import List
from pydantic import BaseModel, Field


class CartItemCreateUpdate(BaseModel):
    dish_id: int = Field(
        alias="dishId",
        title="Dish ID",
        description="The ID of the associated dish"
    )
    quantity: int = Field(
        title="Quantity",
        description="Quantity of the dish in the cart",
        ge=1
    )


class CartCreateUpdate(BaseModel):
    items: List[int] = []
