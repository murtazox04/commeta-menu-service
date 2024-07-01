from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.rdb import (
    BaseDAO,
    RestaurantDAO,
    MenuDAO,
    DiscountDAO,
    DishDAO,
    DishParameterDAO,
    CartDAO,
    CartItemDAO,
    ParametersDAO
)


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
        self.restaurant = RestaurantDAO(self.session)
        self.menu = MenuDAO(self.session)
        self.parameters = ParametersDAO(self.session)
        self.dish = DishDAO(self.session)
        self.dish_parameter = DishParameterDAO(self.session)
        self.discount = DiscountDAO(self.session)
        self.cart = CartDAO(self.session)
        self.cart_item = CartItemDAO(self.session)
