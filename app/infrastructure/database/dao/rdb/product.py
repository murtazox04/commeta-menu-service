from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as
from sqlalchemy.orm import selectinload

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import Menu, Parameters, Dish, DishParameter, Discount, Restaurant


class MenuDAO(BaseDAO[Menu]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Menu, session)

    async def add_menu(
            self,
            menu: schems.MenuCreateUpdate
    ) -> dto.Menu:
        db_menu = Menu(**menu.dict())
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        return dto.Menu.model_validate(db_menu.__dict__, from_attributes=True)

    async def get_menu(
            self,
            menu_id: int
    ) -> Optional[dto.Menu]:
        query = select(Menu).options(selectinload(Menu.dishes)).where(Menu.id == menu_id)
        result = await self.session.execute(query)
        menu = result.scalar_one_or_none()
        return dto.Menu.model_validate(menu.__dict__, from_attributes=True) if menu else None

    async def get_menus(self) -> List[dto.Menu]:
        query = select(Menu).options(selectinload(Menu.dishes))
        result = await self.session.execute(query)
        menus = result.scalars().all()
        return parse_obj_as(List[dto.Menu], menus)

    async def update_menu(
            self,
            menu_id: int,
            menu_update: schems.MenuCreateUpdate
    ) -> Optional[dto.Menu]:
        db_menu = await self.session.get(Menu, menu_id)
        if not db_menu:
            return None
        for key, value in menu_update.dict(exclude_unset=True).items():
            setattr(db_menu, key, value)
        await self.session.commit()
        await self.session.refresh(db_menu)
        return dto.Menu.model_validate(db_menu.__dict__, from_attributes=True)

    async def delete_menu(
            self,
            menu_id: int
    ) -> bool:
        db_menu = await self.session.get(Menu, menu_id)
        if not db_menu:
            return False
        await self.session.delete(db_menu)
        await self.session.commit()
        return True


class ParametersDAO(BaseDAO[Parameters]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Parameters, session)

    async def add_parameter(
            self,
            parameter: schems.ParameterCreateUpdate
    ) -> dto.Parameter:
        db_parameter = Parameters(**parameter.dict())
        self.session.add(db_parameter)
        await self.session.commit()
        await self.session.refresh(db_parameter)
        return dto.Parameter.model_validate(db_parameter.__dict__, from_attributes=True)

    async def get_parameter(
            self,
            parameter_id: int
    ) -> Optional[dto.Parameter]:
        query = select(Parameters).options(selectinload(Parameters.values)).where(Parameters.id == parameter_id)
        result = await self.session.execute(query)
        parameter = result.scalar_one_or_none()
        return dto.Parameter.model_validate(parameter.__dict__, from_attributes=True) if parameter else None

    async def get_parameters(self) -> List[dto.Parameter]:
        query = select(Parameters).options(selectinload(Parameters.values))
        result = await self.session.execute(query)
        parameters = result.scalars().all()
        return parse_obj_as(List[dto.Parameter], parameters)

    async def update_parameter(
            self,
            parameter_id: int,
            parameter_update: schems.ParameterCreateUpdate
    ) -> Optional[dto.Parameter]:
        db_parameter = await self.session.get(Parameters, parameter_id)
        if not db_parameter:
            return None
        for key, value in parameter_update.dict(exclude_unset=True).items():
            setattr(db_parameter, key, value)
        await self.session.commit()
        await self.session.refresh(db_parameter)
        return dto.Parameter.model_validate(db_parameter.__dict__, from_attributes=True)

    async def delete_parameter(
            self,
            parameter_id: int
    ) -> bool:
        db_parameter = await self.session.get(Parameters, parameter_id)
        if not db_parameter:
            return False
        await self.session.delete(db_parameter)
        await self.session.commit()
        return True


class DishDAO(BaseDAO[Dish]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Dish, session)

    async def add_dish(
            self,
            dish: schems.DishCreateUpdate
    ) -> dto.Dish:
        restaurant = await self.session.get(Restaurant, dish.restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail=f"Restaurant with id {dish.restaurant_id} not found")
        db_dish = Dish(
            name=dish.name,
            price=dish.price,
            restaurant_id=dish.restaurant_id,
            menu_id=dish.menu_id
        )
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)

        return dto.Dish.model_validate(db_dish.__dict__, from_attributes=True)

    async def get_dish(
            self,
            dish_id: int
    ) -> Optional[dto.Dish]:
        query = select(Dish).options(
            selectinload(Dish.restaurant),
            selectinload(Dish.menu),
            selectinload(Dish.params).selectinload(DishParameter.key),
            selectinload(Dish.discount)
        ).where(Dish.id == dish_id)
        result = await self.session.execute(query)
        dish = result.scalar_one_or_none()
        return dto.Dish.model_validate(dish.__dict__, from_attributes=True) if dish else None

    async def get_dishes(self) -> List[dto.Dish]:
        query = select(Dish).options(
            selectinload(Dish.restaurant),
            selectinload(Dish.menu),
            selectinload(Dish.params).selectinload(DishParameter.key),
            selectinload(Dish.discount),
        )
        result = await self.session.execute(query)
        dishes = result.scalars().all()
        return parse_obj_as(List[dto.Dish], dishes)

    async def update_dish(
            self,
            dish_id: int,
            dish_update: schems.DishCreateUpdate
    ) -> Optional[dto.Dish]:
        restaurant = await self.session.get(Restaurant, dish_update.restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail=f"Restaurant with id {dish_update.restaurant_id} not found")
        db_dish = await self.session.get(Dish, dish_id)
        if not db_dish:
            return None
        for key, value in dish_update.dict(exclude_unset=True).items():
            setattr(db_dish, key, value)
        await self.session.commit()
        await self.session.refresh(db_dish)

        return dto.Dish.model_validate(db_dish.__dict__, from_attributes=True)

    async def delete_dish(
            self,
            dish_id: int
    ) -> bool:
        db_dish = await self.session.get(Dish, dish_id)
        if not db_dish:
            return False
        await self.session.delete(db_dish)
        await self.session.commit()
        return True


class DishParameterDAO(BaseDAO[DishParameter]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DishParameter, session)

    async def add_dish_parameter(
            self,
            dish_parameter: schems.DishParameterCreateUpdate
    ) -> dto.DishParameter:
        dish = await self.session.get(Dish, dish_parameter.dish_id)
        if not dish:
            raise HTTPException(status_code=404, detail=f"Dish with id {dish_parameter.dish_id} not found")

        db_param = DishParameter(
            dish_id=dish_parameter.dish_id,
            key_id=dish_parameter.key_id,
            value=dish_parameter.value
        )
        self.session.add(db_param)
        await self.session.commit()
        await self.session.refresh(db_param)

        return dto.DishParameter.model_validate(db_param.__dict__, from_attributes=True)

    async def get_dish_parameter(
            self,
            dish_parameter_id: int
    ) -> Optional[dto.DishParameter]:
        query = select(DishParameter).options(
            selectinload(DishParameter.dish),
            selectinload(DishParameter.key)
        ).where(DishParameter.id == dish_parameter_id)
        result = await self.session.execute(query)
        dish_parameter = result.scalar_one_or_none()
        return dto.DishParameter.model_validate(
            dish_parameter.__dict__, from_attributes=True) if dish_parameter else None

    async def get_dish_parameters(self) -> List[dto.DishParameter]:
        query = select(DishParameter).options(
            selectinload(DishParameter.dish),
            selectinload(DishParameter.key)
        )
        result = await self.session.execute(query)
        dish_parameters = result.scalars().all()
        return parse_obj_as(List[dto.DishParameter], dish_parameters)

    async def update_dish_parameter(
            self,
            dish_parameter_id: int,
            dish_parameter_update: schems.DishParameterCreateUpdate
    ) -> Optional[dto.DishParameter]:
        dish = await self.session.get(Dish, dish_parameter_update.dish_id)
        if not dish:
            raise HTTPException(status_code=404, detail=f"Dish with id {dish_parameter_update.dish_id} not found")

        db_dish_parameter = await self.session.get(DishParameter, dish_parameter_id)
        if not db_dish_parameter:
            return None
        for key, value in dish_parameter_update.dict(exclude_unset=True).items():
            setattr(db_dish_parameter, key, value)
        await self.session.commit()
        await self.session.refresh(db_dish_parameter)
        return dto.DishParameter.model_validate(db_dish_parameter.__dict__, from_attributes=True)

    async def delete_dish_parameter(
            self,
            dish_parameter_id: int
    ) -> bool:
        db_dish_parameter = await self.session.get(DishParameter, dish_parameter_id)
        if not db_dish_parameter:
            return False
        await self.session.delete(db_dish_parameter)
        await self.session.commit()
        return True


class DiscountDAO(BaseDAO[Discount]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Discount, session)

    async def add_discount(
            self,
            discount: schems.DiscountCreateUpdate
    ) -> dto.Discount:
        db_discount = Discount(**discount.dict())
        self.session.add(db_discount)
        await self.session.commit()
        await self.session.refresh(db_discount)
        return dto.Discount.model_validate(db_discount.__dict__, from_attributes=True)

    async def get_discount(
            self,
            discount_id: int
    ) -> Optional[dto.Discount]:
        query = select(Discount).options(selectinload(Discount.dish)).where(Discount.id == discount_id)
        result = await self.session.execute(query)
        discount = result.scalar_one_or_none()
        return dto.Discount.model_validate(discount.__dict__, from_attributes=True) if discount else None

    async def get_discounts(self) -> List[dto.Discount]:
        query = select(Discount).options(selectinload(Discount.dish))
        result = await self.session.execute(query)
        discounts = result.scalars().all()
        return parse_obj_as(List[dto.Discount], discounts)

    async def update_discount(
            self,
            discount_id: int,
            discount_update: schems.DiscountCreateUpdate
    ) -> Optional[dto.Discount]:
        db_discount = await self.session.get(Discount, discount_id)
        if not db_discount:
            return None
        for key, value in discount_update.dict(exclude_unset=True).items():
            setattr(db_discount, key, value)
        await self.session.commit()
        await self.session.refresh(db_discount)
        return dto.Discount.model_validate(db_discount.__dict__, from_attributes=True)

    async def delete_discount(
            self,
            discount_id: int
    ) -> bool:
        db_discount = await self.session.get(Discount, discount_id)
        if not db_discount:
            return False
        await self.session.delete(db_discount)
        await self.session.commit()
        return True
