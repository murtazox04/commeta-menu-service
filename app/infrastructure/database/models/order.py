from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

from .base import BaseModel


class Discount(BaseModel):
    __tablename__ = 'discounts'

    dish_id = Column(Integer, ForeignKey('dishes.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    discounted_price = Column(Float)
    dish = relationship("Dish", back_populates="discounts")


class OrderItem(BaseModel):
    __tablename__ = 'order_items'

    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)
    discount_id = Column(Integer, ForeignKey('discounts.id'), nullable=True)

    order = relationship("Order", back_populates="items")
    dish = relationship("Dish")
    discount = relationship("Discount", back_populates="order_items")


class Order(BaseModel):
    __tablename__ = 'orders'

    table_number = Column(Integer, nullable=True)
    status = Column(String)
    items = relationship("OrderItem", back_populates="order")
