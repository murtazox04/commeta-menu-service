from uuid import UUID
from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import dto
from app.api import schems
from .base import BaseDAO
from app.infrastructure.database.models import CartItem, Cart


class CartItemDAO(BaseDAO[CartItem]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CartItem, session)

    async def add_cart_item(
            self,
            cart_item: schems.CartItemCreateUpdate
    ) -> dto.CartItem:
        db_cart_item = CartItem(**cart_item.dict())
        self.session.add(db_cart_item)
        await self.session.commit()
        await self.session.refresh(db_cart_item)
        return dto.CartItem.model_validate(db_cart_item.__dict__, from_attributes=True)

    async def get_cart_item(
            self,
            cart_item_id: int
    ) -> Optional[dto.CartItem]:
        query = select(CartItem).options(selectinload(CartItem.dish)).where(CartItem.id == cart_item_id)
        result = await self.session.execute(query)
        cart_item = result.scalar_one_or_none()
        return dto.CartItem.model_validate(cart_item.__dict__, from_attributes=True) if cart_item else None

    async def get_cart_items(self) -> List[dto.CartItem]:
        query = select(CartItem).options(selectinload(CartItem.dish))
        result = await self.session.execute(query)
        cart_items = result.scalars().all()
        return [dto.CartItem.model_validate(cart_item.__dict__, from_attributes=True) for cart_item in cart_items]

    async def update_cart_item(
            self,
            cart_item_id: int,
            cart_item_update: schems.CartItemCreateUpdate
    ) -> Optional[dto.CartItem]:
        db_cart_item = await self.session.get(CartItem, cart_item_id)
        if not db_cart_item:
            return None
        for key, value in cart_item_update.dict(exclude_unset=True).items():
            setattr(db_cart_item, key, value)
        await self.session.commit()
        await self.session.refresh(db_cart_item)
        return dto.CartItem.model_validate(db_cart_item.__dict__, from_attributes=True)

    async def delete_cart_item(
            self,
            cart_item_id: int
    ) -> bool:
        db_cart_item = await self.session.get(CartItem, cart_item_id)
        if not db_cart_item:
            return False
        await self.session.delete(db_cart_item)
        await self.session.commit()
        return True


class CartDAO(BaseDAO[Cart]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Cart, session)

    async def add_cart(
            self,
            cart: schems.CartCreateUpdate
    ) -> dto.Cart:
        cart_items = await self.session.execute(
            select(CartItem).where(CartItem.id.in_(cart.items)).options(selectinload(CartItem.dish))
        )
        cart_items = cart_items.scalars().all()

        if not cart_items:
            raise ValueError("No valid items found for the cart")

        db_cart = Cart()
        db_cart.items = cart_items

        self.session.add(db_cart)
        await self.session.flush()

        db_cart.total_cost = db_cart.calculate_total_cost()

        await self.session.commit()
        await self.session.refresh(db_cart)

        return dto.Cart.model_validate(db_cart.__dict__, from_attributes=True)

    async def get_cart(
            self,
            cart_id: UUID
    ) -> Optional[dto.Cart]:
        query = select(Cart).options(selectinload(Cart.items)).where(Cart.guid == cart_id)
        result = await self.session.execute(query)
        cart = result.scalar_one_or_none()
        return dto.Cart.model_validate(cart.__dict__, from_attributes=True) if cart else None

    async def get_carts(self) -> List[dto.Cart]:
        query = select(Cart).options(selectinload(Cart.items))
        result = await self.session.execute(query)
        carts = result.scalars().all()
        return [dto.Cart.model_validate(cart.__dict__, from_attributes=True) for cart in carts]

    async def update_cart(
            self,
            cart_id: UUID,
            cart_update: schems.CartCreateUpdate
    ) -> Optional[dto.Cart]:
        query = select(Cart).options(selectinload(Cart.items)).where(Cart.guid == cart_id)
        result = await self.session.execute(query)
        db_cart = result.scalar_one_or_none()
        if not db_cart:
            return None

        cart_items = await self.session.execute(
            select(CartItem).where(CartItem.id.in_(cart_update.items))
        )
        cart_items = cart_items.scalars().all()
        db_cart.items = cart_items

        db_cart.total_cost = db_cart.calculate_total_cost()

        await self.session.commit()
        await self.session.refresh(db_cart)

        return dto.Cart.model_validate(db_cart.__dict__, from_attributes=True)

    async def delete_cart(
            self,
            cart_id: UUID
    ) -> bool:
        query = select(Cart).where(Cart.guid == cart_id)
        result = await self.session.execute(query)
        db_cart = result.scalar_one_or_none()

        if not db_cart:
            return False

        await self.session.delete(db_cart)
        await self.session.commit()
        return True
