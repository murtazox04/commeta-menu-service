from typing import Optional
from pydantic import BaseModel, Field


class RestaurantCreateUpdate(BaseModel):
    name: str = Field(
        title="Name",
        description="The name of the restaurants",
        min_length=1,
        max_length=100
    )
    is_verified: Optional[bool] = Field(
        alias="isVerified",
        title="Is Verified",
        description="Verification status of the restaurants",
        default=False
    )
    address: Optional[str] = Field(
        title="Address",
        description="Address of the restaurants",
        max_length=255
    )
    latitude: Optional[float] = Field(
        title="Latitude",
        description="Latitude coordinate of the restaurants location"
    )
    longitude: Optional[float] = Field(
        title="Longitude",
        description="Longitude coordinate of the restaurants location"
    )
    working_time: Optional[str] = Field(
        alias="workingTime",
        title="Working Time",
        description="Working hours of the restaurants",
        max_length=100,
        default=None
    )
    description: str = Field(
        title="Description",
        description="Description of the restaurants",
        max_length=500
    )
    phone_number: str = Field(
        alias="phoneNumber",
        title="Phone Number",
        description="Contact phone number of the restaurants",
        max_length=20
    )
