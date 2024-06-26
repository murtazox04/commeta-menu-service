from pydantic import Field
from typing import List, Optional

from .base import Base


class CartItem(Base):
    dish_id: int = Field(alias='dishId')
    quantity: int
    total_cost: float = Field(alias='totalCost', default=None)


class Cart(Base):
    # items: List[CartItem]
    total_cost: float = Field(alias='totalCost', default=None)
    qr_code: Optional[str] = Field(alias='qrCode', default=None)
