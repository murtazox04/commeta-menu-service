from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .order import router as order_router
from .product import router as product_router
from .restaurant import router as restaurant_router


def setup(app: FastAPI) -> None:
    app.include_router(
        router=order_router,
        tags=["orders"]
    )
    app.include_router(
        router=restaurant_router,
        tags=["restaurants"]
    )
    app.include_router(
        router=product_router,
        tags=["products"]
    )
    app.mount("/media", StaticFiles(directory="media"), name="media")
