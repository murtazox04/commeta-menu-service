from sqlalchemy import Column, String, Boolean, Float

from .base import BaseModel


class Restaurant(BaseModel):
    __tablename__ = 'restaurants'

    name = Column(String, index=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    working_time = Column(String, nullable=True)
    description = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
