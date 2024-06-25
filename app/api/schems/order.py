from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DiscountBase(BaseModel):
    dish_id: int = Field(
        title="Dish ID",
        description="The ID of the dish to which the discount applies"
    )
    start_time: datetime = Field(
        title="Start Time",
        description="The start time of the discount period"
    )
    end_time: datetime = Field(
        title="End Time",
        description="The end time of the discount period"
    )
    discounted_price: float = Field(
        title="Discounted Price",
        description="The discounted price of the dish"
    )


class Discount(DiscountBase):
    id: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    order_id: int
    dish_id: int
    quantity: int = Field(
        title="Quantity",
        description="The quantity of the dish ordered",
        ge=1,
        default=1
    )
    price: float = Field(
        title="Price",
        description="The price of the dish at the time of ordering",
        ge=0,
        default=0.0
    )
    discount_id: Optional[int] = Field(
        title="Discount ID",
        description="The ID of the applied discount if any"
    )


class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    table_number: int = Field(
        title="Table Number",
        description="The number of the table making the order"
    )
    status: str = Field(
        title="Status",
        description="The status of the order",
        min_length=1,
        max_length=50
    )


class OrderCreate(OrderBase):
    items: List[OrderItemBase] = Field(
        title="Order Items",
        description="List of items in the order"
    )


class Order(OrderBase):
    id: int
    created_at: datetime = Field(
        title="Created At",
        description="The time when the order was created"
    )
    items: List[OrderItem] = Field(
        title="Order Items",
        description="List of items in the order"
    )

    class Config:
        orm_mode = True
