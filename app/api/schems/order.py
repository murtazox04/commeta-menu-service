from pydantic import BaseModel, Field
from typing import Optional, List

from .product import Dish


class CartItemCreateUpdate(BaseModel):
    dishId: int = Field(
        alias="dish_id",
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
    total_cost: Optional[float] = Field(
        title="Total Cost",
        description="Total cost of the cart item (computed property)"
    )
    dish: Dish = Field(
        title="Dish",
        description="Dish associated with the cart item"
    )


class CartCreateUpdate(BaseModel):
    qr_code: str = Field(
        title="QR Code",
        description="QR code associated with the cart",
        max_length=255
    )


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
        title="Total Cost",
        description="Total cost of all items in the cart (computed property)"
    )
