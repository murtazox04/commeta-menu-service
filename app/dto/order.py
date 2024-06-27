from pydantic import Field
from typing import List, Optional

from .base import Base


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


class Cart(Base):
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
    qr_code: Optional[str] = Field(
        alias='qrCode',
        title='QR Code',
        description='The QR Code of the cart',
        default=None
    )
