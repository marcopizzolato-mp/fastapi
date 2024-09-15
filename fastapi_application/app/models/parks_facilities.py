"""ORM Model."""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models.base import Base
from fastapi_application.app.models.parks import Parks


class ParkFacilities(Base):
    """ORM Model for parks facilities table."""

    __tablename__ = "park_facilities"
    __table_args__ = {"schema": "natural_parks_schema"}

    facility_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey(Parks.park_id), nullable=False)
    facility_type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    working = Column(Boolean, nullable=False)
    description = Column(Unicode(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    park_rel = relationship("Parks", back_populates="facilities_rel")
    facility_geom_rel = relationship(
        "GeometryFacilities", uselist=False, back_populates="facility_rel"
    )
