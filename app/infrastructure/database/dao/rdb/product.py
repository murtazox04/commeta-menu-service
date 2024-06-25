from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import MenuCategory, Dish, ProductParameter


class MenuCategoryDAO(BaseDAO[MenuCategory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MenuCategory, session)

    async def add_menu_category(
            self,
            menu_category: schems.MenuCategoryBase
    ) -> dto.MenuCategory:
        db_menu_category = MenuCategory(**menu_category.dict())
        self.session.add(db_menu_category)
        await self.session.commit()
        await self.session.refresh(db_menu_category)
        return dto.MenuCategory.from_orm(db_menu_category)

    async def get_menu_categories(self) -> List[dto.MenuCategory]:
        result = await self.session.execute(select(MenuCategory))
        menu_categories = result.scalars().all()
        return [dto.MenuCategory.from_orm(menu_category) for menu_category in menu_categories]

    async def get_menu_category_by_id(self, menu_category_id: int) -> Optional[dto.MenuCategory]:
        result = await self.session.execute(select(MenuCategory).where(MenuCategory.id == menu_category_id))
        menu_category = result.scalar_one_or_none()
        if menu_category:
            return dto.MenuCategory.from_orm(menu_category)
        return None

    async def update_menu_category(
            self,
            menu_category_id: int,
            menu_category_update: schems.MenuCategoryBase
    ) -> Optional[dto.MenuCategory]:
        result = await self.session.execute(select(MenuCategory).where(MenuCategory.id == menu_category_id))
        db_menu_category = result.scalar_one_or_none()
        if db_menu_category:
            for key, value in menu_category_update.dict().items():
                setattr(db_menu_category, key, value)
            await self.session.commit()
            await self.session.refresh(db_menu_category)
            return dto.MenuCategory.from_orm(db_menu_category)
        return None

    async def delete_menu_category(self, menu_category_id: int) -> bool:
        result = await self.session.execute(select(MenuCategory).where(MenuCategory.id == menu_category_id))
        db_menu_category = result.scalar_one_or_none()
        if db_menu_category:
            await self.session.execute(delete(MenuCategory).where(MenuCategory.id == menu_category_id))
            await self.session.commit()
            return True
        return False


class DishDAO(BaseDAO[Dish]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Dish, session)

    async def add_dish(
            self,
            dish: schems.DishBase
    ) -> dto.Dish:
        db_dish = Dish(**dish.dict())
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)
        return dto.Dish.from_orm(db_dish)

    async def get_dishes(self) -> List[dto.Dish]:
        result = await self.session.execute(select(Dish))
        dishes = result.scalars().all()
        return [dto.Dish.from_orm(dish) for dish in dishes]

    async def get_dish_by_id(self, dish_id: int) -> Optional[dto.Dish]:
        result = await self.session.execute(select(Dish).where(Dish.id == dish_id))
        dish = result.scalar_one_or_none()
        if dish:
            return dto.Dish.from_orm(dish)
        return None

    async def update_dish(
            self,
            dish_id: int,
            dish_update: schems.DishBase
    ) -> Optional[dto.Dish]:
        result = await self.session.execute(select(Dish).where(Dish.id == dish_id))
        db_dish = result.scalar_one_or_none()
        if db_dish:
            for key, value in dish_update.dict().items():
                setattr(db_dish, key, value)
            await self.session.commit()
            await self.session.refresh(db_dish)
            return dto.Dish.from_orm(db_dish)
        return None

    async def delete_dish(self, dish_id: int) -> bool:
        result = await self.session.execute(select(Dish).where(Dish.id == dish_id))
        db_dish = result.scalar_one_or_none()
        if db_dish:
            await self.session.execute(delete(Dish).where(Dish.id == dish_id))
            await self.session.commit()
            return True
        return False


class ProductParameterDAO(BaseDAO[ProductParameter]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ProductParameter, session)

    async def add_product_parameter(
            self,
            product_parameter: schems.ProductParameterBase
    ) -> dto.ProductParameter:
        db_product_parameter = ProductParameter(**product_parameter.dict())
        self.session.add(db_product_parameter)
        await self.session.commit()
        await self.session.refresh(db_product_parameter)
        return dto.ProductParameter.from_orm(db_product_parameter)

    async def get_product_parameters(self) -> List[dto.ProductParameter]:
        result = await self.session.execute(select(ProductParameter))
        product_parameters = result.scalars().all()
        return [dto.ProductParameter.from_orm(product_parameter) for product_parameter in product_parameters]

    async def get_product_parameter_by_id(self, dish_parameter_id: int) -> Optional[dto.ProductParameter]:
        result = await self.session.execute(select(ProductParameter).where(ProductParameter.id == dish_parameter_id))
        product_parameter = result.scalar_one_or_none()
        if product_parameter:
            return dto.ProductParameter.from_orm(product_parameter)
        return None

    async def update_product_parameter(
            self,
            product_parameter_id: int,
            product_parameter_update: schems.ProductParameter
    ) -> Optional[dto.ProductParameter]:
        result = await self.session.execute(select(ProductParameter).where(ProductParameter.id == product_parameter_id))
        db_product_parameter = result.scalar_one_or_none()
        if db_product_parameter:
            for key, value in product_parameter_update.dict().items():
                setattr(db_product_parameter, key, value)
            await self.session.commit()
            await self.session.refresh(db_product_parameter)
            return dto.ProductParameter.from_orm(db_product_parameter)
        return None

    async def delete_dish_parameter(self, product_parameter_id: int) -> bool:
        result = await self.session.execute(select(ProductParameter).where(ProductParameter.id == product_parameter_id))
        db_product_parameter = result.scalar_one_or_none()
        if db_product_parameter:
            await self.session.execute(delete(ProductParameter).where(ProductParameter.id == product_parameter_id))
            await self.session.commit()
            return True
        return False
