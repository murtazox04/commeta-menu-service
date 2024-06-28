from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter()


@router.get(
    '/menu-category',
    description='Get all menu categories'
)
async def get_menu_categories(dao: HolderDao = Depends(dao_provider)) -> List[dto.MenuCategory]:
    return await dao.menu_category.get_menu_categories()


@router.get('/menu-category/{category_id}', response_model=dto.MenuCategory)
async def get_menu_category(
        category_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.MenuCategory:
    return await dao.menu_category.get_menu_category_by_id(category_id)


@router.post('/menu-category', response_model=dto.MenuCategory)
async def create_menu_category(
        category: schems.MenuCategoryCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.MenuCategory:
    return await dao.menu_category.add_menu_category(category)


@router.put('/menu-category/{category_id}', response_model=dto.MenuCategory)
async def update_menu_category(
        category_id: int,
        category: schems.MenuCategoryCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.MenuCategory:
    return await dao.menu_category.update_menu_category(category_id, category)


@router.delete('/menu-category/{category_id}')
async def delete_menu_category(
        category_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> bool:
    return await dao.menu_category.delete_menu_category(category_id)


# DISH
@router.get(
    '/dishes',
    description='Get all dishes'
)
async def get_dishes(
        dao: HolderDao = Depends(dao_provider)
) -> List[dto.Dish]:
    return await dao.dish.get_dishes()


@router.get(
    '/dishes/{dish_id}',
    description='Get a specific dish'
)
async def get_dish(
        dish_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    data = await dao.dish.get_dish_by_id(dish_id)
    return data


@router.post(
    '/dishes',
    description='Create a new dish'
)
async def create_dish(
        dish: schems.DishCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    data = await dao.dish.add_dish(dish)
    return data


@router.put(
    '/dishes/{dish_id}',
    description='Update a dish'
)
async def update_dish(
        dish_id: int,
        dish: schems.DishCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    return await dao.dish.update_dish(dish_id, dish)


@router.delete(
    '/dishes/{dish_id}',
    description='Delete a dish',
)
async def delete_dish(
        dish_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    return await dao.dish.delete_dish(dish_id)


# Product Params

@router.get(
    '/product-params',
    description='Get all Product Parameters'
)
async def get_product_params(dao: HolderDao = Depends(dao_provider)) -> List[dto.DishParameter]:
    return await dao.dish_parameter.get_product_parameters()


@router.get(
    '/product-params/{product_param_id}',
    description='Get a specific Product Parameters'
)
async def get_product_param(
        product_param_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.DishParameter:
    return await dao.dish_parameter.get_product_parameter_by_id(product_param_id)


@router.post(
    '/product-params',
    description='Add product parameter'
)
async def add_product_param(
        product_param: schems.DishParameterCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.DishParameter:
    return await dao.dish_parameter.add_product_parameter(product_param)


@router.put(
    '/product-params/{product_param_id}',
    description='Update product parameter'
)
async def update_product_params(
        product_param_id: int,
        product_params: schems.DishParameterCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.DishParameter:
    return await dao.dish_parameter.update_product_parameter(product_param_id, product_params)


@router.delete(
    '/product-params/{product_param_id}',
    description='Delete product parameter',
)
async def delete_product_param(
        product_param_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    return await dao.dish_parameter.delete_product_parameter(product_param_id)


# Discount

@router.get(
    '/discounts',
    description='Get all Discounts'
)
async def get_discounts(dao: HolderDao = Depends(dao_provider)) -> List[dto.Discount]:
    return await dao.discount.get_discounts()


@router.get(
    '/discounts/{discount_id}',
    description='Get a specific Discount'
)
async def get_discount(
        discount_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    discount = await dao.discount.get_discount_by_id(discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount


@router.post(
    '/discounts',
    description='Create a new Discount'
)
async def create_discount(
        discount: schems.DiscountCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    return await dao.discount.add_discount(discount)


@router.put(
    '/discounts/{discount_id}',
    description='Update a Discount'
)
async def update_discount(
        discount_id: int,
        discount_update: schems.DiscountCreateUpdate,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Discount:
    updated_discount = await dao.discount.update_discount(discount_id, discount_update)
    if not updated_discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return updated_discount


@router.delete(
    '/discounts/{discount_id}',
    description='Delete a Discount',
)
async def delete_discount(
        discount_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    success = await dao.discount.delete_discount(discount_id)
    if not success:
        raise HTTPException(status_code=404, detail="Discount not found")
    return success
