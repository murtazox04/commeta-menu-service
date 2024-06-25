from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Float

from .base import BaseModel


class Restaurant(BaseModel):
    __tablename__ = 'restaurants'

    name = Column(String, index=True)
    is_verified = Column(Boolean, default=False)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    working_time = Column(String)
    description = Column(String)
    menu_categories = relationship("MenuCategory", back_populates="restaurant")
