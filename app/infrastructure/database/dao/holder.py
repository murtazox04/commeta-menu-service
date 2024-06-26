from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.rdb import (
    BaseDAO,
    RestaurantDAO,
    MenuCategoryDAO,
    DishDAO,
    DishParameterDAO
)


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
        self.restaurant = RestaurantDAO(self.session)
        self.menu_category = MenuCategoryDAO(self.session)
        self.dish = DishDAO(self.session)
        self.dish_parameter = DishParameterDAO(self.session)
        # self.discount = DiscountDAO(self.session)
        # self.order_item = OrderItemDAO(self.session)
        # self.order = OrderDAO(self.session)
