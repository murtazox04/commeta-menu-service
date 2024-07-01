from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("/", response_model=List[dto.Menu])
async def get_menus(dao: HolderDao = Depends(dao_provider)) -> List[dto.Menu]:
    try:
        menus = await dao.menu.get_menus()
        if not menus:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menus not found")
        return menus
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.Menu)
async def create_menu(menu: schems.MenuCreateUpdate, dao: HolderDao = Depends(dao_provider)) -> dto.Menu:
    try:
        created_menu = await dao.menu.add_menu(menu)
        return created_menu
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{menu_id}", response_model=dto.Menu)
async def get_menu(menu_id: int, dao: HolderDao = Depends(dao_provider)) -> dto.Menu:
    try:
        menu = await dao.menu.get_menu(menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        return menu
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{menu_id}", response_model=dto.Menu)
async def update_menu(
        menu_id: int,
        menu_update: schems.MenuCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Menu:
    try:
        updated_menu = await dao.menu.update_menu(menu_id, menu_update)
        if not updated_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        return updated_menu
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(menu_id: int, dao: HolderDao = Depends(dao_provider)):
    try:
        deleted = await dao.menu.delete_menu(menu_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        return JSONResponse(
            content={"message": "The menu is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))