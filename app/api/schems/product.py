from pydantic import BaseModel, Field
from typing import Optional, List


class DiscountCreateUpdate(BaseModel):
    dish_id: int = Field(
        title="Dish ID",
        description="The ID of the associated dish"
    )
    start_date: Optional[str] = Field(
        title="Start Date",
        description="Start date of the discount validity"
    )
    end_date: Optional[str] = Field(
        title="End Date",
        description="End date of the discount validity"
    )
    price: float = Field(
        title="Price",
        description="Discounted price of the dish"
    )


class Discount(DiscountCreateUpdate):
    id: int = Field(
        title="ID",
        description="The unique identifier for the discount",
        ge=1
    )
    created_at: Optional[str] = Field(
        title="Created At",
        description="Timestamp indicating when the discount was created"
    )
    updated_at: Optional[str] = Field(
        title="Updated At",
        description="Timestamp indicating when the discount was last updated"
    )


class MenuCategoryCreateUpdate(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the menu category",
        min_length=1,
        max_length=100
    )
    restaurant_id: int = Field(
        title="Restaurant ID",
        description="The ID of the associated restaurant"
    )


class MenuCategory(MenuCategoryCreateUpdate):
    id: int = Field(
        title="ID",
        description="The unique identifier for the menu category",
        ge=1
    )
    created_at: Optional[str] = Field(
        title="Created At",
        description="Timestamp indicating when the menu category was created"
    )
    updated_at: Optional[str] = Field(
        title="Updated At",
        description="Timestamp indicating when the menu category was last updated"
    )


class DishCreateUpdate(BaseModel):
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
        description="The ID of the associated menu category"
    )


class Dish(DishCreateUpdate):
    id: int = Field(
        title="ID",
        description="The unique identifier for the dish",
        ge=1
    )
    created_at: Optional[str] = Field(
        title="Created At",
        description="Timestamp indicating when the dish was created"
    )
    updated_at: Optional[str] = Field(
        title="Updated At",
        description="Timestamp indicating when the dish was last updated"
    )
    category: MenuCategory = Field(
        title="Category",
        description="Menu category to which the dish belongs"
    )
    discount: Optional[List[Discount]] = Field(
        title="Discount",
        description="Discounts applied to the dish"
    )


class DishParameterCreateUpdate(BaseModel):
    dish_id: int = Field(
        title="Dish ID",
        description="The ID of the associated dish"
    )
    key: str = Field(
        title="Key",
        description="Key or name of the parameter",
        min_length=1,
        max_length=100
    )
    value: str = Field(
        title="Value",
        description="Value associated with the parameter",
        max_length=255
    )


class DishParameter(DishParameterCreateUpdate):
    id: int = Field(
        title="ID",
        description="The unique identifier for the dish parameter",
        ge=1
    )
    created_at: Optional[str] = Field(
        title="Created At",
        description="Timestamp indicating when the dish parameter was created"
    )
    updated_at: Optional[str] = Field(
        title="Updated At",
        description="Timestamp indicating when the dish parameter was last updated"
    )
