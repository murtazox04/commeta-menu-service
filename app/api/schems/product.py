from pydantic import BaseModel, Field


class MenuCategoryBase(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the menu category",
        min_length=1,
        max_length=100
    )
    restaurant_id: int = Field(
        title="Restaurant ID",
        description="The ID of the restaurant to which the menu category belongs"
    )


class MenuCategory(MenuCategoryBase):
    id: int

    class Config:
        orm_mode = True


class DishBase(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the dish",
        min_length=1,
        max_length=100
    )
    price: float = Field(
        title="Price",
        description="The price of the dish"
    )
    category_id: int = Field(
        title="Category ID",
        description="The ID of the menu category to which the dish belongs"
    )


class Dish(DishBase):
    id: int

    class Config:
        orm_mode = True


class ProductParameterBase(BaseModel):
    dish_id: int = Field(
        title="Dish ID",
        description="The ID of the dish to which the parameter belongs"
    )
    key: str = Field(
        title="Key",
        description="The parameter key",
        min_length=1,
        max_length=50
    )
    value: str = Field(
        title="Value",
        description="The parameter value",
        min_length=1,
        max_length=100
    )


class ProductParameter(ProductParameterBase):
    id: int

    class Config:
        orm_mode = True
