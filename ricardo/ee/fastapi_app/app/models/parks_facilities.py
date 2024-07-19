"""ORM Model."""

from sqlalchemy import Column, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi_app.app.models.base import Base
from ricardo.ee.fastapi_app.app.models.parks import Parks


class ParkFacilities(Base):
    """ORM Model for parks facilities table."""

    __tablename__ = "park_facilities"

    facility_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey(Parks.park_id), nullable=False)
    facility_type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Unicode(500))

    # Relationships
    park_rel = relationship("Parks", back_populates="facilities_rel")
