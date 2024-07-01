from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/parameters", tags=["parameters"])


@router.get("/", response_model=List[dto.Parameter])
async def get_parameters(dao: HolderDao = Depends(dao_provider)) -> List[dto.Parameter]:
    try:
        parameters = await dao.parameters.get_parameters()
        if not parameters:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parameters not found")
        return parameters
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.Parameter)
async def create_parameter(
        parameter: schems.ParameterCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Parameter:
    try:
        created_parameter = await dao.parameters.add_parameter(parameter)
        return created_parameter
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{parameter_id}", response_model=dto.Parameter)
async def get_parameter(parameter_id: int, dao: HolderDao = Depends(dao_provider)) -> dto.Parameter:
    try:
        parameter = await dao.parameters.get_parameter(parameter_id)
        if not parameter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parameter not found")
        return parameter
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{parameter_id}", response_model=dto.Parameter)
async def update_parameter(
        parameter_id: int,
        parameter_update: schems.ParameterCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Parameter:
    try:
        updated_parameter = await dao.parameters.update_parameter(parameter_id, parameter_update)
        if not updated_parameter:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parameter not found")
        return updated_parameter
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{parameter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parameter(parameter_id: int, dao: HolderDao = Depends(dao_provider)):
    try:
        deleted = await dao.parameters.delete_parameter(parameter_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parameter not found")
        return JSONResponse(
            content={"message": "The parameter is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
