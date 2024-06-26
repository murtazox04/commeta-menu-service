from pydantic import Field

from app.dto import Base


class Restaurant(Base):
    name: str
    address: str
    is_verified: bool = Field(alias='isVerified', default=False)
    address: str
    latitude: float
    longitude: float
    working_time: str = Field(alias='workingTime', default=None)
    description: str
    phone_number: str = Field(alias='phoneNumber', default=None)
