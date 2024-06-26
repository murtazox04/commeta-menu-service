from typing import List
from fastapi import APIRouter, Depends

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


@router.get(
    '/menu-category/{category_id}',
    description='Get a specific menu category'
)
async def get_menu_category(
        category_id: int,
        dao: HolderDao = Depends(dao_provider)
) -> dto.MenuCategory:
    return await dao.menu_category.get_menu_category_by_id(category_id)


@router.get('/menu-category', response_model=List[dto.MenuCategory])
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
    print(data)
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
    print("----------------")
    print(data)
    print("----------------")
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
