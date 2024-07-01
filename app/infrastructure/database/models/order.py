from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, Float, ForeignKey, Table, UniqueConstraint

from .base import BaseModel

cart_items = Table(
    'cart_cart_items',
    BaseModel.metadata,
    Column('cart_id', UUID(as_uuid=True), ForeignKey('carts.guid')),
    Column('cartitem_id', Integer, ForeignKey('cart_items.id'))
)


class CartItem(BaseModel):
    __tablename__ = 'cart_items'

    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_cost = Column(Float, nullable=True, default=None)

    dish = relationship('Dish', back_populates='cart_items')
    carts = relationship('Cart', secondary=cart_items, back_populates='items')


class Cart(BaseModel):
    __tablename__ = 'carts'

    guid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    total_cost = Column(Float, default=0.0, nullable=False)
    items = relationship('CartItem', secondary=cart_items, back_populates='carts')

    __table_args__ = (
        UniqueConstraint('guid', name='uq_cart_guid'),
    )

    def calculate_total_cost(self) -> float:
        return sum(item.total_cost if item.total_cost is not None else 0.0 for item in self.items)
