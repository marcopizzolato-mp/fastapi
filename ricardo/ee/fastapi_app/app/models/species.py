"""ORM Model."""

from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi_app.app.models.base import Base


class Species(Base):
    """ORM Model for Species table."""

    species_id = Column(Integer, primary_key=True, index=True)
    common_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    habitat = Column(String(100), nullable=False)
    description = Column(Unicode(500), nullable=False)

    species_rel = relationship("ParksSpecies", back_populates="park_species_rel")
