from pydantic import BaseModel, Field


class RestaurantBase(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the restaurant",
        min_length=1,
        max_length=100
    )
    is_verified: bool = Field(
        title="Is Verified",
        description="Verification status of the restaurant",
        default=False
    )
    address: str = Field(
        title="Address",
        description="The address of the restaurant",
        min_length=1,
        max_length=200
    )
    latitude: float = Field(
        title="Latitude",
        description="The latitude of the restaurant location"
    )
    longitude: float = Field(
        title="Longitude",
        description="The longitude of the restaurant location"
    )
    working_time: str = Field(
        title="Working Time",
        description="The working hours of the restaurant",
        min_length=1,
        max_length=50
    )
    description: str = Field(
        title="Description",
        description="The description of the restaurant",
        min_length=1,
        max_length=500
    )


class Restaurant(RestaurantBase):
    id: int

    class Config:
        orm_mode = True
