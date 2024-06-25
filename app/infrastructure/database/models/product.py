from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

from .base import BaseModel


class MenuCategory(BaseModel):
    __tablename__ = 'menu_categories'

    name = Column(String, index=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("Restaurant", back_populates="menu_categories")
    dishes = relationship("Dish", back_populates="category")


class Dish(BaseModel):
    __tablename__ = 'dishes'

    name = Column(String, index=True)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('menu_categories.id'))
    category = relationship("MenuCategory", back_populates="dishes")
    parameters = relationship("ProductParameter", back_populates="dish")
    discounts = relationship("Discount", back_populates="dish")
    order_items = relationship("OrderItem", back_populates="dish")


class ProductParameter(BaseModel):
    __tablename__ = 'product_parameters'

    dish_id = Column(Integer, ForeignKey('dishes.id'))
    key = Column(String)
    value = Column(String)
    dish = relationship("Dish", back_populates="parameters")
