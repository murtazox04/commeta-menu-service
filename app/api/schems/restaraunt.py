from pydantic import BaseModel, Field
from typing import Optional


class RestaurantCreateUpdate(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the restaurant",
        min_length=1,
        max_length=100
    )
    is_verified: Optional[bool] = Field(
        alias="isVerified",
        title="Is Verified",
        description="Verification status of the restaurant",
        default=False
    )
    address: Optional[str] = Field(
        title="Address",
        description="Address of the restaurant",
        max_length=255
    )
    latitude: Optional[float] = Field(
        title="Latitude",
        description="Latitude coordinate of the restaurant location"
    )
    longitude: Optional[float] = Field(
        title="Longitude",
        description="Longitude coordinate of the restaurant location"
    )
    working_time: Optional[str] = Field(
        alias="workingTime",
        title="Working Time",
        description="Working hours of the restaurant",
        max_length=100
    )
    description: str = Field(
        title="Description",
        description="Description of the restaurant",
        max_length=500
    )
    phone_number: str = Field(
        alias="phoneNumber",
        title="Phone Number",
        description="Contact phone number of the restaurant",
        max_length=20
    )


class Restaurant(RestaurantCreateUpdate):
    id: int = Field(
        title="ID",
        description="The unique identifier for the restaurant",
        ge=1
    )
    created_at: Optional[str] = Field(
        title="Created At",
        description="Timestamp indicating when the restaurant was created"
    )
    updated_at: Optional[str] = Field(
        title="Updated At",
        description="Timestamp indicating when the restaurant was last updated"
    )
