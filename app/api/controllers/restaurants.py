from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.get("/", response_model=List[dto.Restaurant])
async def get_restaurants(search: str, dao: HolderDao = Depends(dao_provider)) -> List[dto.Restaurant]:
    try:
        if search:
            restaurants = await dao.restaurant.get_restaurant_by_name(search)
        else:
            restaurants = await dao.restaurant.get_restaurants()
        if not restaurants:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurants not found")
        return restaurants
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.Restaurant)
async def create_restaurant(
        restaurant: schems.RestaurantCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Restaurant:
    try:
        created_restaurant = await dao.restaurant.add_restaurant(restaurant)
        return created_restaurant
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{restaurant_id}", response_model=dto.Restaurant)
async def get_restaurant(restaurant_id: int, dao: HolderDao = Depends(dao_provider)) -> dto.Restaurant:
    try:
        restaurant = await dao.restaurant.get_restaurant(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        return restaurant
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{restaurant_id}", response_model=dto.Restaurant)
async def update_restaurant(
        restaurant_id: int,
        restaurant_update: schems.RestaurantCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Restaurant:
    try:
        updated_restaurant = await dao.restaurant.update_restaurant(restaurant_id, restaurant_update)
        if not updated_restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        return updated_restaurant
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(restaurant_id: int, dao: HolderDao = Depends(dao_provider)):
    try:
        deleted = await dao.restaurant.delete_restaurant(restaurant_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
        return JSONResponse(
            content={"message": "The restaurant is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


