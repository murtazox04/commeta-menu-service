from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao import HolderDao

router = APIRouter(prefix="/cart-items", tags=["cart-items"])


@router.get("/", response_model=List[dto.CartItem])
async def get_cart_items(
        dao: HolderDao = Depends(dao_provider)
) -> List[dto.CartItem]:
    try:
        cart_items = await dao.cart_item.get_cart_items()
        if not cart_items:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart items not found")
        return cart_items
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=dto.CartItem)
async def create_cart_item(
        cart_item: schems.CartItemCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.CartItem:
    try:
        created_cart_item = await dao.cart_item.add_cart_item(cart_item)
        return created_cart_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{cart_item_id}", response_model=dto.CartItem)
async def get_cart_item(
        cart_item_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.CartItem:
    try:
        cart_item = await dao.cart_item.get_cart_item(cart_item_id)
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        return cart_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{cart_item_id}", response_model=dto.CartItem)
async def update_cart_item(
        cart_item_id: int,
        cart_item_update: schems.CartItemCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.CartItem:
    try:
        updated_cart_item = await dao.cart_item.update_cart_item(cart_item_id, cart_item_update)
        if not updated_cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        return updated_cart_item
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
        cart_item_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    try:
        deleted = await dao.cart_item.delete_cart_item(cart_item_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
        return JSONResponse(
            content={"message": "The cart item is successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
