from pydantic import Field
from typing import Optional

from app.dto import Base


class Restaurant(Base):
    name: str = Field(
        title="Name",
        description="Restaurant Name",
    )
    is_verified: bool = Field(
        alias='isVerified',
        title="Is Verified",
        description="Is Restaurant Verified",
        default=False
    )
    address: str = Field(
        title="Address",
        description="Restaurant Address",
        examples=["88QM+HX4, Ziyolilar St 9, Tashkent, Uzbekistan"]
    )
    latitude: float = Field(
        title="Latitude",
        description="Restaurant Latitude",
    )
    longitude: float = Field(
        title="Longitude",
        description="Restaurant Longitude",
    )
    working_time: Optional[str] = Field(
        alias='workingTime',
        title="Working Time",
        description="Restaurant Working Time",
        default=None
    )
    description: str = Field(
        title="Description",
        description="Restaurant Description",
    )
    phone_number: str = Field(
        alias='phoneNumber',
        title="Phone Number",
        description="Restaurant Phone Number",
        default=None
    )
