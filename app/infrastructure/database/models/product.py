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


class Menu(BaseModel):
    __tablename__ = 'menus'

    name = Column(String(255), index=True, nullable=False)
    dishes = relationship('Dish', back_populates='menu')


class Parameters(BaseModel):
    __tablename__ = 'parameters'

    name = Column(String(255), index=True, nullable=False)
    values = relationship('DishParameter', back_populates='key')


class Dish(BaseModel):
    __tablename__ = 'dishes'

    name = Column(String(255), index=True, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    price = Column(Float, nullable=False)
    menu_id = Column(Integer, ForeignKey('menus.id'), nullable=False)
    discounted_price = Column(Float, nullable=True, default=None)

    restaurant = relationship('Restaurant', back_populates='dishes')
    menu = relationship('Menu', back_populates='dishes')
    cart_items = relationship('CartItem', back_populates='dish')
    params = relationship('DishParameter', back_populates='dish')
    discount = relationship('Discount', back_populates='dish', uselist=False)


class DishParameter(BaseModel):
    __tablename__ = 'dish_parameters'

    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    key_id = Column(Integer, ForeignKey('parameters.id'), nullable=False)
    value = Column(String(255), nullable=False)

    dish = relationship('Dish', back_populates='params')
    key = relationship('Parameters', back_populates='values')


class Discount(BaseModel):
    __tablename__ = 'discounts'

    dish_id = Column(Integer, ForeignKey('dishes.id'), unique=True, nullable=False)
    start_date = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

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
