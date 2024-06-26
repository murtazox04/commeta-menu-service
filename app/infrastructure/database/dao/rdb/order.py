from typing import Optional, List

from pydantic import parse_obj_as
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from .utils import generate_qr_code
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Cart, CartItem, Dish


class CartDAO(BaseDAO[Cart]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Cart, session)

    async def add_cart(self, cart: schems.CartCreateUpdate) -> dto.Cart:
        # Fetch all cart items in a single query
        cart_items = await self.session.execute(
            select(CartItem).where(CartItem.id.in_(cart.items))
        )
        cart_items = cart_items.scalars().all()

        if not cart_items:
            raise ValueError("No valid items found for the cart")

        # Create new Cart instance
        db_cart = Cart()

        # Add items to the cart
        db_cart.items = cart_items

        # Add cart to session and flush to get the ID
        self.session.add(db_cart)
        await self.session.flush()

        # Update total cost
        db_cart.total_cost = db_cart.calculate_total_cost()  # Call the method

        await self.session.commit()
        await self.session.refresh(db_cart)

        return db_cart

    async def get_cart(self, cart_id: int) -> Optional[dto.Cart]:
        query = select(Cart).options(
            selectinload(Cart.items).selectinload(CartItem.dish)
        ).where(Cart.id == cart_id)

        result = await self.session.execute(query)
        cart = result.scalar_one_or_none()

        if cart:
            return cart
        return None

    async def get_carts(self) -> List[dto.Cart]:
        query = select(Cart).options(selectinload(Cart.items))
        result = await self.session.execute(query)
        carts = result.scalars().all()
        if not carts:
            raise ValueError("No valid items found for the cart")
        return parse_obj_as(List[dto.Cart], carts)

    async def update_cart(self, cart_id: int, cart_update: schems.CartCreateUpdate) -> Optional[dto.Cart]:
        db_cart = await self.session.get(Cart, cart_id)
        if not db_cart:
            return None

        # Update cart items
        cart_items = await self.session.execute(
            select(CartItem).where(CartItem.id.in_(cart_update.items))
        )
        cart_items = cart_items.scalars().all()
        db_cart.items = cart_items

        # Update total cost
        db_cart.total_cost = db_cart.calculate_total_cost

        await self.session.commit()
        await self.session.refresh(db_cart)

        return db_cart

    async def delete_cart(self, cart_id: int) -> bool:
        db_cart = await self.session.get(Cart, cart_id)
        if not db_cart:
            return False

        await self.session.delete(db_cart)
        await self.session.commit()
        return True

    async def add_item_to_cart(self, cart_id: int, item: schems.CartItemCreateUpdate) -> Optional[dto.Cart]:
        db_cart = await self.session.get(Cart, cart_id)
        if not db_cart:
            return None

        new_item = CartItem(dish_id=item.dish_id, quantity=item.quantity)
        self.session.add(new_item)
        await self.session.flush()

        db_cart.items.append(new_item)
        db_cart.total_cost = db_cart.calculate_total_cost

        await self.session.commit()
        await self.session.refresh(db_cart)

        return db_cart

    async def remove_item_from_cart(self, cart_id: int, item_id: int) -> Optional[dto.Cart]:
        db_cart = await self.session.get(Cart, cart_id)
        if not db_cart:
            return None

        db_cart.items = [item for item in db_cart.items if item.id != item_id]
        db_cart.total_cost = db_cart.calculate_total_cost

        await self.session.commit()
        await self.session.refresh(db_cart)

        return db_cart


class CartItemDAO(BaseDAO[CartItem]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CartItem, session)

    async def add_cart_item(self, cart_item_data: schems.CartItemCreateUpdate) -> dto.CartItem:
        db_cart_item = CartItem(**cart_item_data.dict())

        dish_id = cart_item_data.dish_id
        dish = await self.session.get(Dish, dish_id)
        if not dish:
            raise ValueError("Dish not found")

        # Calculate total cost based on discounted_price or price
        if dish.discounted_price and dish.discounted_price > 0:
            db_cart_item.total_cost = dish.discounted_price * db_cart_item.quantity
        else:
            db_cart_item.total_cost = dish.price * db_cart_item.quantity

        self.session.add(db_cart_item)
        await self.session.commit()

        return db_cart_item

    async def get_cart_items(self):
        result = await self.session.execute(select(CartItem).options(joinedload(CartItem.dish)))
        return result.scalars().all()

    async def get_cart_item_by_id(self, cart_item_id: int):
        return await self.session.get(CartItem, cart_item_id)

    async def update_cart_item(self, cart_item_id: int, cart_item_data: dict) -> CartItem:
        cart_item = await self.session.get(CartItem, cart_item_id)
        if not cart_item:
            return None

        for key, value in cart_item_data.items():
            setattr(cart_item, key, value)

        await self.session.commit()
        return cart_item

    async def delete_cart_item(self, cart_item_id: int) -> bool:
        cart_item = await self.session.get(CartItem, cart_item_id)
        if not cart_item:
            return False

        await self.session.delete(cart_item)
        await self.session.commit()
        return True
