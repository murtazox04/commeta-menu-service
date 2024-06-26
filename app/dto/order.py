from pydantic import Field
from typing import List

from .base import Base


class CartItem(Base):
    dishId: int = Field(alias='dish_id')
    quantity: int
    totalCost: float = Field(alias='total_cost')


class Cart(Base):
    items: List[CartItem]
    qrCode: str = Field(alias='qr_code')
    totalCost: float = Field(alias='total_cost')

