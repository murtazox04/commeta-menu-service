from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, event, select

from .base import BaseModel

cart_items_association = Table(
    'cart_items_association',
    BaseModel.metadata,
    Column('cart_id', Integer, ForeignKey('carts.id'), primary_key=True),
    Column('cart_item_id', Integer, ForeignKey('cart_items.id'), primary_key=True)
)


class CartItem(BaseModel):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    total_cost = Column(Float, nullable=True)

    dish = relationship('Dish', back_populates='cart_items')
    carts = relationship('Cart', secondary=cart_items_association, back_populates='items')


class Cart(BaseModel):
    __tablename__ = 'carts'

    qr_code = Column(String, nullable=True, default="media/logo.png")
    total_cost = Column(Float, nullable=True, default=0.0)
    items = relationship('CartItem', secondary=cart_items_association, back_populates='carts')

    def calculate_total_cost(self):
        return sum(item.total_cost for item in self.items)


# @event.listens_for(CartItem, 'after_insert')
# @event.listens_for(CartItem, 'after_update')
# @event.listens_for(CartItem, 'after_delete')
# def update_cart_total_cost(mapper, connection, target):
#     cart_item_id = target.id
#     cart_associations = connection.execute(
#         cart_items_association.select().where(cart_items_association.c.cart_item_id == cart_item_id)
#     ).fetchall()
#
#     for cart_association in cart_associations:
#         cart_id = cart_association.cart_id
#         if cart_id:
#             cart = connection.execute(select(Cart).where(Cart.id == cart_id)).scalar_one_or_none()
#             if cart:
#                 cart.calculate_total_cost()
#                 connection.execute(
#                     Cart.__table__.update()
#                     .where(Cart.id == cart_id)
#                     .values(total_cost=cart.total_cost)
#                 )
