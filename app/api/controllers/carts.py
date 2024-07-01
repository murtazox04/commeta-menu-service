from uuid import UUID
from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao


router = APIRouter(prefix="/carts", tags=["carts"])


@router.get("/", response_model=List[dto.Cart])
async def get_carts(dao: HolderDao = Depends(dao_provider)) -> List[dto.Cart]:
    try:
        carts = await dao.cart.get_carts()
        if not carts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carts not found")
        return carts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.Cart)
async def create_cart(cart: schems.CartCreateUpdate, dao: HolderDao = Depends(dao_provider)) -> dto.Cart:
    try:
        created_cart = await dao.cart.add_cart(cart)
        return created_cart
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{cart_id}", response_model=dto.Cart)
async def get_cart(cart_id: UUID, dao: HolderDao = Depends(dao_provider)) -> dto.Cart:
    try:
        cart = await dao.cart.get_cart(cart_id)
        if not cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
        return cart
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{cart_id}", response_model=dto.Cart)
async def update_cart(
        cart_id: UUID,
        cart_update: schems.CartCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Cart:
    try:
        updated_cart = await dao.cart.update_cart(cart_id, cart_update)
        if not updated_cart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
        return updated_cart
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: UUID, dao: HolderDao = Depends(dao_provider)):
    try:
        deleted = await dao.cart.delete_cart(cart_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
        return JSONResponse(
            content={"message": "The cart is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
