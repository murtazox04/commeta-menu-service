from pydantic import BaseModel, Field
from typing import Optional, List

from .product import Dish


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


class CartItem(CartItemCreateUpdate):
    id: int = Field(
        title="ID",
        description="The unique identifier for the cart item",
        ge=1
    )
    created_at: Optional[str] = Field(
        title="Created At",
        description="Timestamp indicating when the cart item was created"
    )
    updated_at: Optional[str] = Field(
        title="Updated At",
        description="Timestamp indicating when the cart item was last updated"
    )
    total_cost: float = Field(
        alias="totalCost",
        title="Total Cost",
        description="Total cost of the cart item (computed property)"
    )
    dish: Dish = Field(
        title="Dish",
        description="Dish associated with the cart item"
    )


class CartCreateUpdate(BaseModel):
    # items: List[int] = Field(
    #     title="Items",
    #     description="List of dish IDs associated with the cart",
    #     default=[]
    # )
    items: List[int] = []


class Cart(CartCreateUpdate):
    id: int = Field(
        title="ID",
        description="The unique identifier for the cart",
        ge=1
    )
    created_at: Optional[str] = Field(
        title="Created At",
        description="Timestamp indicating when the cart was created"
    )
    updated_at: Optional[str] = Field(
        title="Updated At",
        description="Timestamp indicating when the cart was last updated"
    )
    items: Optional[List[CartItem]] = Field(
        title="Items",
        description="List of cart items associated with the cart"
    )
    total_cost: Optional[float] = Field(
        alias="totalCost",
        title="Total Cost",
        description="Total cost of all items in the cart (computed property)"
    )
