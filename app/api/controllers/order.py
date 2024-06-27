from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter()


@router.get("/carts")
async def get_cart(dao: HolderDao = Depends(dao_provider)) -> List[dto.Cart]:
    carts = await dao.cart.get_carts()
    if not carts:
        raise HTTPException(status_code=404, detail="Data not found")
    return carts


@router.get("/carts/{cart_id}", response_model=dto.Cart)
async def get_cart(cart_id: int, dao: HolderDao = Depends(dao_provider)):
    carts = await dao.cart.get_carts()
    if not carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    return carts


@router.post("/carts")
async def get_cart(
        cart: schems.CartCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Cart:
    return await dao.cart.add_cart(cart)


@router.put("/carts/{cart_id}", response_model=dto.Cart)
async def update_cart(
        cart_id: int,
        cart: schems.CartCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Cart:
    cart = await dao.cart.update_cart(cart_id, cart)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.delete("/carts/{cart_id}")
async def delete_cart(
        cart_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    cart = await dao.cart.delete_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/carts/{cart_id}/items", response_model=dto.Cart)
async def add_item_to_cart(
        cart_id: int,
        item: schems.CartItemCreateUpdate,
        dao: HolderDao = Depends(dao_provider),
):
    cart = await dao.cart.add_item_to_cart(cart_id, item)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return cart


@router.delete("/carts/{cart_id}/items/{item_id}", response_model=dto.Cart)
async def remove_item_from_cart(
        cart_id: int,
        item_id: int,
        dao: HolderDao = Depends(dao_provider),
):
    cart = await dao.cart.remove_item_from_cart(cart_id, item_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart or item not found")
    return cart


# Cart Item
@router.get('/cart-items', description="Get all cart items")
async def get_cart_items(dao: HolderDao = Depends(dao_provider)) -> List[dto.CartItem]:
    return await dao.cart_item.get_cart_items()


@router.get('/cart-items/{cart_id}', description="Get cart item by id")
async def get_cart_item_by_id(
        cart_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.CartItem:
    cart_item = await dao.cart_item.get_cart_item_by_id(cart_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item


@router.post('/cart-items', description="Create cart item")
async def create_cart_item(
        cart_item: schems.CartItemCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.CartItem:
    return await dao.cart_item.add_cart_item(cart_item)


@router.put('/cart-items/{cart_id}', description="Update cart item")
async def update_cart_item(
        cart_id: int,
        cart_update: schems.CartItemCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.CartItem:
    updated_cart_item = await dao.cart_item.update_cart_item(cart_id, cart_update)
    if not updated_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_cart_item


@router.delete('/cart-items/{cart_id}', description="Delete cart item")
async def delete_cart_item(
        cart_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    success = await dao.cart_item.delete_cart_item(cart_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return success
