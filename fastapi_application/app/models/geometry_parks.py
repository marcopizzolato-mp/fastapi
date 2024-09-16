"""ORM Model."""

from geoalchemy2 import Geometry
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models import Parks
from fastapi_application.app.models.base import Base


class GeometryParks(Base):
    """ORM Model for Parks Geometry table."""

    __table_args__ = {"schema": "natural_parks_schema"}  # noqa RUF012

    park_id = Column(Integer, ForeignKey(Parks.park_id), primary_key=True)
    geometry = Column(Geometry("POLYGON"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    park_rel = relationship("Parks", back_populates="park_geom_rel")
