from typing import List
from fastapi.responses import  JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.get("/", response_model=List[dto.Dish])
async def get_dishes(
        dao: HolderDao = Depends(dao_provider)
) -> List[dto.Dish]:
    try:
        dishes = await dao.dish.get_dishes()
        if not dishes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dishes not found")
        return dishes
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.Dish)
async def create_dish(
        dish: schems.DishCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    try:
        created_dish = await dao.dish.add_dish(dish)
        return created_dish
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{dish_id}", response_model=dto.Dish)
async def get_dish(
        dish_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    try:
        dish = await dao.dish.get_dish(dish_id)
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return dish
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{dish_id}", response_model=dto.Dish)
async def update_dish(
        dish_id: int,
        dish_update: schems.DishCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    try:
        updated_dish = await dao.dish.update_dish(dish_id, dish_update)
        if not updated_dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return updated_dish
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(
        dish_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    try:
        deleted = await dao.dish.delete_dish(dish_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
        return JSONResponse(
            content={"message": "The dish is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
