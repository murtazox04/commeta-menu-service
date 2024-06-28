import pytz
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Boolean,
    func,
    event,
    update
)

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
    discounted_price = Column(Float, nullable=True, default=None)

    category = relationship('MenuCategory', back_populates='dishes')
    discount = relationship('Discount', uselist=False, back_populates='dish', cascade="all, delete-orphan")
    cart_items = relationship('CartItem', back_populates='dish')
    params = relationship('DishParameter', back_populates='dish')


class DishParameter(BaseModel):
    __tablename__ = 'dish_parameters'

    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    dish = relationship('Dish', back_populates='params')


class Discount(BaseModel):
    __tablename__ = 'discounts'

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'), unique=True, nullable=False)
    start_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    dish = relationship('Dish', back_populates='discount')


# Event for automatically calculating discounted_price
def update_discounted_price(mapper, connection, target):
    try:
        tashkent_tz = pytz.timezone('Asia/Tashkent')
        now = datetime.now(tashkent_tz)
        start_date = target.start_date.astimezone(
            tashkent_tz) if target.start_date.tzinfo else target.start_date.replace(tzinfo=tashkent_tz)
        end_date = target.end_date.astimezone(tashkent_tz) if target.end_date.tzinfo else target.end_date.replace(
            tzinfo=tashkent_tz)

        if target.is_active and start_date <= now <= end_date:
            stmt = (
                update(Dish)
                .where(Dish.id == target.dish_id)
                .values(discounted_price=(Dish.price - target.price))
            )
            connection.execute(stmt)
        else:
            stmt = (
                update(Dish)
                .where(Dish.id == target.dish_id)
                .values(discounted_price=None)
            )
            connection.execute(stmt)
    except Exception as e:
        print(f"Error in update_discounted_price: {e}")


def remove_discounted_price(mapper, connection, target):
    try:
        stmt = (
            update(Dish)
            .where(Dish.id == target.dish_id)
            .values(discounted_price=None)
        )
        connection.execute(stmt)
    except Exception as e:
        print(f"Error in remove_discounted_price: {e}")


event.listen(Discount, 'after_insert', update_discounted_price)
event.listen(Discount, 'after_update', update_discounted_price)
event.listen(Discount, 'after_delete', remove_discounted_price)
