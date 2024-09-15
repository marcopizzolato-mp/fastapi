"""ORM Model."""

from typing import ClassVar

from sqlalchemy import Column, Date, DateTime, Integer, String, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models.base import Base


class Parks(Base):
    """ORM Model for Parks table."""

    __table_args__: ClassVar[dict] = {"schema": "natural_parks_schema"}

    park_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    established_date = Column(Date, nullable=False)
    description = Column(Unicode(500))
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    park_species_rel = relationship("ParksSpecies", back_populates="park_rel")
    visits_rel = relationship("ParkVisits", back_populates="park_rel")
    conservation_efforts_rel = relationship(
        "ConservationEfforts", back_populates="park_rel"
    )
    facilities_rel = relationship("ParkFacilities", back_populates="park_rel")
    park_geom_rel = relationship(
        "GeometryParks", uselist=False, back_populates="park_rel"
    )
