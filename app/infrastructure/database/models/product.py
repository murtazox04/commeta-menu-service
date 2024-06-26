from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean

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
    discounted_price = Column(Float, nullable=True, default=0)

    category = relationship('MenuCategory', back_populates='dishes')
    discount = relationship('Discount', uselist=False, back_populates='dish', cascade="all, delete-orphan")
    cart_items = relationship('CartItem', back_populates='dish')

    @property
    def effective_price(self):
        if (self.discount and
                self.discount.start_date <= func.now <= self.discount.end_date and self.discount.is_active):
            return self.discount.price
        return self.price


class DishParameter(BaseModel):
    __tablename__ = 'dish_parameters'

    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)


class Discount(BaseModel):
    __tablename__ = 'discounts'

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'), unique=True, nullable=False)
    start_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    dish = relationship('Dish', back_populates='discount')
