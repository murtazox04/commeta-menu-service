from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

from .base import BaseModel


class MenuCategory(BaseModel):
    __tablename__ = 'menu_categories'

    name = Column(String, index=True, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)

    dishes = relationship('Dish', back_populates='category')


class Dish(BaseModel):
    __tablename__ = 'dishes'

    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('menu_categories.id'), nullable=False)

    category = relationship('MenuCategory', back_populates='dishes')
    discounts = relationship('Discount', back_populates='dish')
    cart_items = relationship('CartItem', back_populates='dish')

    @property
    def get_price(self) -> float:
        for discount in self.discounts:
            if discount.start_date <= func.now() <= discount.end_date:
                return self.price - discount.price
        return self.price


class DishParameter(BaseModel):
    __tablename__ = 'dish_parameters'

    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)


class Discount(BaseModel):
    __tablename__ = 'discounts'

    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)
    start_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Float, nullable=False)

    dish = relationship('Dish', back_populates='discounts')
