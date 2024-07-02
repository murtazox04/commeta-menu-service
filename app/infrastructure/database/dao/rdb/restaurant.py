from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import dto
from app.api import schems
from .base import BaseDAO
from app.infrastructure.database.models import Restaurant


class RestaurantDAO(BaseDAO[Restaurant]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Restaurant, session)

    async def add_restaurant(
            self,
            restaurant: schems.RestaurantCreateUpdate
    ) -> dto.Restaurant:
        db_restaurant = Restaurant(**restaurant.dict())
        self.session.add(db_restaurant)
        await self.session.commit()
        await self.session.refresh(db_restaurant)
        return dto.Restaurant.model_validate(db_restaurant.__dict__, from_attributes=True)

    async def get_restaurant_by_name(self, name: str) -> List[dto.Restaurant]:
        search = f"%{name}%"
        query = select(Restaurant).options(selectinload(Restaurant.dishes)).filter(Restaurant.name.like(search))
        result = await self.session.execute(query)
        restaurants = result.scalars().all()
        print(restaurants)
        return [dto.Restaurant.model_validate(restaurant.__dict__, from_attributes=True) for restaurant in restaurants]

    async def get_restaurant(
            self,
            restaurant_id: int
    ) -> Optional[dto.Restaurant]:
        query = select(Restaurant).options(selectinload(Restaurant.dishes)).where(Restaurant.id == restaurant_id)
        result = await self.session.execute(query)
        restaurant = result.scalar_one_or_none()
        return dto.Restaurant.model_validate(restaurant.__dict__, from_attributes=True) if restaurant else None

    async def get_restaurants(self) -> List[dto.Restaurant]:
        query = select(Restaurant).options(selectinload(Restaurant.dishes))
        result = await self.session.execute(query)
        restaurants = result.scalars().all()
        return [dto.Restaurant.model_validate(restaurant.__dict__, from_attributes=True) for restaurant in restaurants]

    async def update_restaurant(
            self,
            restaurant_id: int,
            restaurant_update: schems.RestaurantCreateUpdate
    ) -> Optional[dto.Restaurant]:
        db_restaurant = await self.session.get(Restaurant, restaurant_id)
        if not db_restaurant:
            return None
        for key, value in restaurant_update.dict(exclude_unset=True).items():
            setattr(db_restaurant, key, value)
        await self.session.commit()
        await self.session.refresh(db_restaurant)
        return dto.Restaurant.model_validate(db_restaurant.__dict__, from_attributes=True)

    async def delete_restaurant(
            self,
            restaurant_id: int
    ) -> bool:
        db_restaurant = await self.session.get(Restaurant, restaurant_id)
        if not db_restaurant:
            return False
        await self.session.delete(db_restaurant)
        await self.session.commit()
        return True
