"""ORM Model."""

from geoalchemy2 import Geometry
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models import ParkFacilities
from fastapi_application.app.models.base import Base


class GeometryFacilities(Base):
    """ORM Model for Facilities Geometry table."""

    __table_args__ = {"schema": "natural_parks_schema"}  # noqa RUF012

    facility_id = Column(
        Integer, ForeignKey(ParkFacilities.facility_id), primary_key=True
    )
    geometry = Column(Geometry("POINT"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    facility_rel = relationship("ParkFacilities", back_populates="facility_geom_rel")
