from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Restaurant


class RestaurantDAO(BaseDAO[Restaurant]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Restaurant, session)

    async def add_restaurant(
            self,
            restaurant: schems.RestaurantBase
    ) -> dto.Restaurant:
        db_restaurant = Restaurant(**restaurant.dict())
        self.session.add(db_restaurant)
        await self.session.commit()
        await self.session.refresh(db_restaurant)
        return dto.Restaurant.from_orm(db_restaurant)

    async def get_restaurants(self) -> List[dto.Restaurant]:
        result = await self.session.execute(select(Restaurant))
        restaurants = result.scalars().all()
        return [dto.Restaurant.from_orm(restaurant) for restaurant in restaurants]

    async def get_restaurant_by_id(self, restaurant_id: int) -> Optional[dto.Restaurant]:
        result = await self.session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
        restaurant = result.scalar_one_or_none()
        if restaurant:
            return dto.Restaurant.from_orm(restaurant)
        return None

    async def update_restaurant(
            self,
            restaurant_id: int,
            restaurant_update: schems.RestaurantBase
    ) -> Optional[dto.Restaurant]:
        result = await self.session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
        db_restaurant = result.scalar_one_or_none()
        if db_restaurant:
            for key, value in restaurant_update.dict().items():
                setattr(db_restaurant, key, value)
            await self.session.commit()
            await self.session.refresh(db_restaurant)
            return dto.Restaurant.from_orm(db_restaurant)
        return None

    async def delete_restaurant(self, restaurant_id: int) -> bool:
        result = await self.session.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
        db_restaurant = result.scalar_one_or_none()
        if db_restaurant:
            await self.session.execute(delete(Restaurant).where(Restaurant.id == restaurant_id))
            await self.session.commit()
            return True
        return False
