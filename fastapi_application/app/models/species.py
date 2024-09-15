"""ORM Model."""
from typing import ClassVar

from sqlalchemy import Column, DateTime, Integer, String, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models.base import Base


class Species(Base):
    """ORM Model for Species table."""

    __table_args__: ClassVar[dict] = {"schema": "natural_parks_schema"}

    species_id = Column(Integer, primary_key=True, index=True)
    common_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    habitat = Column(String(100), nullable=False)
    description = Column(Unicode(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    species_rel = relationship("ParksSpecies", back_populates="park_species_rel")
