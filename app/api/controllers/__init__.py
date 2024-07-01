from fastapi import FastAPI

from .cart_items import router as cart_item_router
from .carts import router as carts_router
from .discounts import router as discount_router
from .dish import router as dish_router
from .dish_params import router as dish_params_router
from .menu import router as menu_router
from .params import router as params_router
from .restaurants import router as restaurant_router


def setup(app: FastAPI) -> None:
    app.include_router(
        router=cart_item_router,
    )
    app.include_router(
        router=carts_router,
    )
    app.include_router(
        router=restaurant_router,
    )
    app.include_router(
        router=discount_router,
    )
    app.include_router(
        router=dish_router,
    )
    app.include_router(
        router=dish_params_router,
    )
    app.include_router(
        router=menu_router,
    )
    app.include_router(
        router=params_router,
    )
