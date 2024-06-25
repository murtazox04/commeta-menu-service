from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao.holder import HolderDao


router = APIRouter()


@router.post(
    path="/orders",
    description="Create a new order"
)
async def add_order(
        order: schems.OrderCreate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Order:
    return await dao.order.add_order(order)


@router.get(
    path="/orders",
    description="Get all orders"
)
async def get_orders(dao: HolderDao = Depends(dao_provider)) -> List[dto.Order]:
    return await dao.order.get_orders()


@router.get(
    path="/orders/{order_id}",
    description="Get a specific order"
)
async def get_order(order_id: int, dao: HolderDao = Depends(dao_provider)) -> dto.Order:
    order = await dao.order.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put(
    path="/orders/{order_id}",
    description="Update a specific order"
)
async def update_order(
        order_id: int,
        order: schems.OrderBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Order:
    updated_order = await dao.order.update_order(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order


@router.delete(
    path="/orders/{order_id}",
    description="Delete a specific order"
)
async def delete_order(
        order_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dict:
    success = await dao.order.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {"message": "Order deleted successfully"}


# order items
@router.post(
    "/order-items",
    response_model=dto.OrderItem,
    description="Create a new order item",
)
async def create_order_item(
        order_item: schems.OrderItemBase,
        dao: HolderDao = Depends(dao_provider),
) -> dto.OrderItem:
    created_order_item = await dao.order_item.create_order_item(order_item)
    return dto.OrderItem.from_orm(created_order_item)


@router.get(
    "/order-items/{order_item_id}",
    response_model=dto.OrderItem,
    description="Get a specific order item",
)
async def read_order_item(
        order_item_id: int,
        dao: HolderDao = Depends(dao_provider),
) -> dto.OrderItem:
    order_item = await dao.order_item.get_order_item_by_id(order_item_id)
    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    return dto.OrderItem.from_orm(order_item)


@router.put(
    "/order-items/{order_item_id}",
    response_model=dto.OrderItem,
    description="Update a specific order item",
)
async def update_order_item(
        order_item_id: int,
        order_item: schems.OrderItemBase,
        dao: HolderDao = Depends(dao_provider),
) -> dto.OrderItem:
    updated_order_item = await dao.order_item.update_order_item(order_item_id, order_item)
    if not updated_order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    return dto.OrderItem.from_orm(updated_order_item)


@router.delete(
    "/order-items/{order_item_id}",
    response_model=dict,
    description="Delete a specific order item",
)
async def delete_order_item(
        order_item_id: int,
        dao: HolderDao = Depends(dao_provider),
) -> dict:
    success = await dao.order_item.delete_order_item(order_item_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order item not found")
    return {"message": "Order item deleted successfully"}


@router.get(
    "/order-items",
    response_model=List[dto.OrderItem],
    description="Get all order items",
)
async def read_all_order_items(
        dao: HolderDao = Depends(dao_provider),
) -> List[dto.OrderItem]:
    order_items = await dao.order_item.get_all_order_items()
    return [dto.OrderItem.from_orm(order_item) for order_item in order_items]


# discount
@router.post(
    path="/discounts",
    description="Create a new discount"
)
async def add_discount(
        discount: schems.DiscountBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    return await dao.discount.add_discount(discount)


@router.get(
    path="/discounts",
    description="Get all discounts"
)
async def get_discounts(dao: HolderDao = Depends(dao_provider)) -> List[dto.Discount]:
    return await dao.discount.get_discounts()


@router.get(
    path="/discounts/{discount_id}",
    description="Get a specific discount"
)
async def get_discount(discount_id: int, dao: HolderDao = Depends(dao_provider)) -> dto.Discount:
    discount = await dao.discount.get_discount_by_id(discount_id)
    if not discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
    return discount


@router.put(
    path="/discounts/{discount_id}",
    description="Update a specific discount"
)
async def update_discount(
        discount_id: int,
        discount: schems.DiscountBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    updated_discount = await dao.discount.update_discount(discount_id, discount)
    if not updated_discount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
    return updated_discount


@router.delete(
    path="/discounts/{discount_id}",
    description="Delete a specific discount"
)
async def delete_discount(
        discount_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dict:
    success = await dao.discount.delete_discount(discount_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discount not found")
    return {"message": "Discount deleted successfully"}
