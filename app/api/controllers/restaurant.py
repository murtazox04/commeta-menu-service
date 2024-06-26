from typing import List
from fastapi.responses import Response
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter()


@router.get(
    '/restaurants',
    description='Get all restaurants',
)
async def get_restaurants(dao: HolderDao = Depends(dao_provider)) -> List[dto.Restaurant]:
    data = await dao.restaurant.get_restaurants()
    return data


@router.get(
    '/restaurants/{restaurant_id}',
    description='Get restaurant',
)
async def get_restaurant(restaurant_id: int, dao: HolderDao = Depends(dao_provider)) -> dto.Restaurant:
    return await dao.restaurant.get_restaurant_by_id(restaurant_id)


@router.post(
    '/restaurants',
    description='Create restaurant',
)
async def create_restaurant(
        restaurant: schems.RestaurantCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Restaurant:
    return await dao.restaurant.add_restaurant(restaurant)


@router.put(
    '/restaurants/{restaurant_id}',
    description='Update restaurant'
)
async def update_restaurant(
        restaurant_id: int,
        restaurant: schems.RestaurantCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Restaurant:
    return await dao.restaurant.update_restaurant(restaurant_id, restaurant)


@router.delete('/restaurants/{restaurant_id}', description='Delete restaurant')
async def delete_restaurant(
        restaurant_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    deleted = await dao.restaurant.delete_restaurant(restaurant_id)
    if deleted:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

