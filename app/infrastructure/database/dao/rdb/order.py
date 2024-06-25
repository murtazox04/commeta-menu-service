from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Discount, Order, OrderItem


class DiscountDAO(BaseDAO[Discount]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Discount, session)

    async def add_discount(
            self,
            discount: schems.DiscountBase
    ) -> dto.Discount:
        db_discount = Discount(**discount.dict())
        self.session.add(db_discount)
        await self.session.commit()
        await self.session.refresh(db_discount)
        return dto.Discount.from_orm(db_discount)

    async def get_discounts(self) -> List[dto.Discount]:
        result = await self.session.execute(select(Discount))
        discounts = result.scalars().all()
        return [dto.Discount.from_orm(discount) for discount in discounts]

    async def get_discount_by_id(self, discount_id: int) -> Optional[dto.Discount]:
        result = await self.session.execute(select(Discount).where(Discount.id == discount_id))
        discount = result.scalar_one_or_none()
        if discount:
            return dto.Discount.from_orm(discount)
        return None

    async def update_discount(
            self,
            discount_id: int,
            discount_update: schems.DiscountBase
    ) -> Optional[dto.Discount]:
        result = await self.session.execute(select(Discount).where(Discount.id == discount_id))
        db_discount = result.scalar_one_or_none()
        if db_discount:
            for key, value in discount_update.dict().items():
                setattr(db_discount, key, value)
            await self.session.commit()
            await self.session.refresh(db_discount)
            return dto.Discount.from_orm(db_discount)
        return None

    async def delete_discount(self, discount_id: int) -> bool:
        result = await self.session.execute(select(Discount).where(Discount.id == discount_id))
        db_discount = result.scalar_one_or_none()
        if db_discount:
            await self.session.execute(delete(Discount).where(Discount.id == discount_id))
            await self.session.commit()
            return True
        return False


class OrderDAO(BaseDAO[Order]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Order, session)

    async def add_order(self, order: schems.OrderCreate) -> dto.Order:
        db_order = Order(
            table_number=order.table_number,
            status=order.status,
            created_at=datetime.now()
        )
        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)

        order_items = []
        for item in order.items:
            discount = await self._get_active_discount(item.dish_id)
            discounted_price = discount.discounted_price if discount else None

            db_order_item = OrderItem(
                dish_id=item.dish_id,
                order_id=db_order.id,
                discount=discount
            )
            self.session.add(db_order_item)
            await self.session.commit()
            await self.session.refresh(db_order_item)
            order_items.append(db_order_item)

        db_order.items = order_items
        return dto.Order.from_orm(db_order)

    async def _get_active_discount(self, dish_id: int) -> Optional[dto.Discount]:
        now = datetime.now()
        result = await self.session.execute(
            select(Discount).where(
                Discount.dish_id == dish_id,
                Discount.start_time <= now,
                Discount.end_time >= now
            )
        )
        discount = result.scalar_one_or_none()
        return dto.Discount.from_orm(discount) if discount else None

    async def get_orders(self) -> List[dto.Order]:
        result = await self.session.execute(select(Order).options(joinedload(Order.items)))
        orders = result.scalars().all()
        return [dto.Order.from_orm(order) for order in orders]

    async def get_order_by_id(self, order_id: int) -> Optional[dto.Order]:
        result = await self.session.execute(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items).selectinload(OrderItem.dish))
        )
        order = result.scalar_one_or_none()
        if order:
            return dto.Order.from_orm(order)
        return None

    async def update_order(
            self,
            order_id: int,
            order_update: schems.OrderBase
    ) -> Optional[dto.Order]:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        db_order = result.scalar_one_or_none()
        if db_order:
            for key, value in order_update.dict().items():
                setattr(db_order, key, value)
            await self.session.commit()
            await self.session.refresh(db_order)
            return dto.Order.from_orm(db_order)
        return None

    async def delete_order(self, order_id: int) -> bool:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        db_order = result.scalar_one_or_none()
        if db_order:
            await self.session.execute(delete(Order).where(Order.id == order_id))
            await self.session.commit()
            return True
        return False


class OrderItemDAO:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_order_item(self, order_item: schems.OrderItem) -> dto.OrderItem:
        db_order_item = OrderItem(**order_item.dict())
        self.session.add(db_order_item)
        await self.session.commit()
        await self.session.refresh(db_order_item)
        return db_order_item

    async def get_order_item_by_id(self, order_item_id: int) -> Optional[dto.OrderItem]:
        result = await self.session.execute(select(OrderItem).where(OrderItem.id == order_item_id))
        order_item = result.scalars().first()
        return order_item

    async def update_order_item(self, order_item_id: int, order_item: schems.OrderItem) -> Optional[OrderItem]:
        result = await self.session.execute(select(OrderItem).where(OrderItem.id == order_item_id))
        db_order_item = result.scalars().first()
        if db_order_item:
            for field, value in order_item:
                setattr(db_order_item, field, value)
            await self.session.commit()
            await self.session.refresh(db_order_item)
            return db_order_item
        return None

    async def delete_order_item(self, order_item_id: int) -> bool:
        result = await self.session.execute(select(OrderItem).where(OrderItem.id == order_item_id))
        db_order_item = result.scalars().first()
        if db_order_item:
            self.session.delete(db_order_item)
            await self.session.commit()
            return True
        return False

    async def get_order_items_by_order_id(self, order_id: int) -> List[dto.OrderItem]:
        result = await self.session.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        order_items = result.scalars().all()
        return order_items
