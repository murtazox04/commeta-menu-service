from typing import List, Optional

from .base import Base
from .product import Dish, Discount


class OrderItem(Base):
    order_id: int
    dish_id: int
    quantity: int
    price: float
    discount: Optional[Discount]
    dish: Dish


class Order(Base):
    table_number: int
    status: str
    items: List[OrderItem]
