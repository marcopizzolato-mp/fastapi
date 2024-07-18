"""ORM Model."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi.app.models.base import Base
from ricardo.ee.fastapi.app.models.parks import Parks
from ricardo.ee.fastapi.app.models.species import Species


class ParksSpecies(Base):
    """ORM Model for park species table."""

    __tablename__ = "parks_species"

    park_species_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey(Parks.park_id), nullable=False)
    species_id = Column(Integer, ForeignKey(Species.species_id), nullable=False)

    park_rel = relationship("Parks", back_populates="park_species_rel")
    park_species_rel = relationship("Species", back_populates="species_rel")
