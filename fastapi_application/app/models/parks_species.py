"""ORM Model."""

from typing import ClassVar

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models.base import Base
from fastapi_application.app.models.parks import Parks
from fastapi_application.app.models.species import Species


class ParksSpecies(Base):
    """ORM Model for park species table."""

    __tablename__ = "parks_species"
    __table_args__: ClassVar[dict] = {"schema": "natural_parks_schema"}

    park_species_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey(Parks.park_id), nullable=False)
    species_id = Column(Integer, ForeignKey(Species.species_id), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    park_rel = relationship("Parks", back_populates="park_species_rel")
    park_species_rel = relationship("Species", back_populates="species_rel")
