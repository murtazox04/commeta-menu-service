from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, Table

from .base import BaseModel
from .utils import generate_qr_code

cart_items_association = Table(
    'cart_items_association',
    BaseModel.metadata,
    Column('cart_id', Integer, ForeignKey('carts.id'), primary_key=True),
    Column('cart_item_id', Integer, ForeignKey('cart_items.id'), primary_key=True)
)


class CartItem(BaseModel):
    __tablename__ = 'cart_items'

    dish_id = Column(Integer, ForeignKey('dishes.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    dish = relationship('Dish', back_populates='cart_items')
    carts = relationship('Cart', secondary=cart_items_association, back_populates='items')

    @property
    def total_cost(self):
        return self.quantity * self.dish.get_price


class Cart(BaseModel):
    __tablename__ = 'carts'

    qr_code = Column(String, unique=True, nullable=False)
    items = relationship('CartItem', secondary=cart_items_association, back_populates='carts')

    @property
    def total_cost(self) -> float:
        return sum(item.total_cost for item in self.items)

    async def save(self, session: AsyncSession):
        data = ""  # Fill this with relevant data for the QR code
        file_path = f"media/cart/{self.id}-qrcode.png"
        qr_code = generate_qr_code(data, file_path)
        self.qr_code = file_path
        await super().save(session)
