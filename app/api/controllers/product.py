from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider
from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter()


@router.get(
    '/menu-category',
    description='Get all menu categories',
    response_model=List[schems.MenuCategory]
)
async def get_menu_categories(dao: HolderDao = Depends(dao_provider)) -> List[dto.MenuCategory]:
    return await dao.menu_category.get_menu_categories()


@router.get(
    '/menu-category/{category_id}',
    description='Get a specific menu category',
    response_model=schems.MenuCategory
)
async def get_menu_category(category_id: int, dao: HolderDao = Depends(dao_provider)) -> dto.MenuCategory:
    return await dao.menu_category.get_menu_category_by_id(category_id)


@router.post(
    '/menu-category',
    description='Create a new menu category',
    response_model=schems.MenuCategory,
)
async def create_menu_category(
        category: schems.MenuCategoryBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.MenuCategory:
    return await dao.menu_category.add_menu_category(category)


@router.put(
    '/menu-category/{category_id}',
    description='Update a menu category',
    response_model=schems.MenuCategory
)
async def update_menu_category(
        category_id: int,
        category: schems.MenuCategoryBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.MenuCategory:
    return await dao.menu_category.update_menu_category(category_id, category)


@router.delete(
    '/menu-category/{category_id}',
    description='Delete a menu category',
)
async def delete_menu_category(
        category_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    return await dao.menu_category.delete_menu_category(category_id)


# DISH
@router.get(
    '/dishes',
    description='Get all dishes',
    response_model=List[schems.Dish]
)
async def get_dishes(
        dao: HolderDao = Depends(dao_provider)
) -> List[dto.Dish]:
    return await dao.dish.get_dishes()


@router.get(
    '/dishes/{dish_id}',
    description='Get a specific dish',
    response_model=schems.Dish
)
async def get_dish(
        dish_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    data = await dao.dish.get_dish_by_id(dish_id)
    print(data)
    return data


@router.post(
    '/dishes',
    description='Create a new dish',
    response_model=schems.Dish
)
async def create_dish(
        dish: schems.DishBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.Dish:
    return await dao.dish.add_dish(dish)


@router.put(
    '/dishes/{dish_id}',
    description='Update a dish',
    response_model=schems.Dish
)
async def update_dish(
        dish_id: int,
        dish: schems.DishBase,
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
    description='Get all Product Parameters',
    response_model=List[schems.ProductParameter]
)
async def get_product_params(dao: HolderDao = Depends(dao_provider)) -> List[dto.ProductParameter]:
    return await dao.product_parameter.get_product_parameters()


@router.get(
    '/product-params/{product_param_id}',
    description='Get a specific Product Parameters',
    response_model=schems.ProductParameter
)
async def get_product_param(
        product_param_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.ProductParameter:
    return await dao.product_parameter.get_product_parameter_by_id(product_param_id)


@router.post(
    '/product-params',
    description='Add product parameter',
    response_model=schems.ProductParameter
)
async def add_product_param(
        product_param: schems.ProductParameterBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.ProductParameter:
    return await dao.product_parameter.add_product_parameter(product_param)


@router.put(
    '/product-params/{product_param_id}',
    description='Update product parameter',
    response_model=schems.ProductParameter
)
async def update_product_params(
        product_param_id: int,
        product_params: schems.ProductParameterBase,
        dao: HolderDao = Depends(dao_provider)
) -> dto.ProductParameter:
    return await dao.product_parameter.update_product_parameter(product_param_id, product_params)


@router.delete(
    '/product-params/{product_param_id}',
    description='Delete product parameter',
)
async def delete_product_param(
        product_param_id: int,
        dao: HolderDao = Depends(dao_provider)
):
    return await dao.product_parameter.delete_product_parameter(product_param_id)
