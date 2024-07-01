from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/dish-parameters", tags=["dish-parameters"])


@router.get("/", response_model=List[dto.DishParameter])
async def get_dish_parameters(dao: HolderDao = Depends(dao_provider)) -> List[dto.DishParameter]:
    try:
        dish_parameters = await dao.dish_parameter.get_dish_parameters()
        if not dish_parameters:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish parameters not found")
        return dish_parameters
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.DishParameter)
async def create_dish_parameter(
        dish_parameter: schems.DishParameterCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.DishParameter:
    try:
        created_dish_parameter = await dao.dish_parameter.add_dish_parameter(dish_parameter)
        return created_dish_parameter
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{dish_parameter_id}", response_model=dto.DishParameter)
async def get_dish_parameter(
        dish_parameter_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.DishParameter:
    try:
        dish_parameter = await dao.dish_parameter.get_dish_parameter(dish_parameter_id)
        if not dish_parameter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish parameter not found")
        return dish_parameter
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{dish_parameter_id}", response_model=dto.DishParameter)
async def update_dish_parameter(
        dish_parameter_id: int,
        dish_parameter_update: schems.DishParameterCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.DishParameter:
    try:
        updated_dish_parameter = await dao.dish_parameter.update_dish_parameter(
            dish_parameter_id, dish_parameter_update
        )
        if not updated_dish_parameter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish parameter not found")
        return updated_dish_parameter
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{dish_parameter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish_parameter(
        dish_parameter_id: int,
        dao: HolderDao = Depends(dao_provider)):
    try:
        deleted = await dao.dish_parameter.delete_dish_parameter(dish_parameter_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish parameter not found")
        return JSONResponse(
            content={"message": "The dish parameter is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
