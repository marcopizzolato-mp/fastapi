"""ORM Model."""

from fastapi_app.app.models.base import Base
from fastapi_app.app.models.parks import Parks
from fastapi_app.app.models.species import Species
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class ParksSpecies(Base):
    """ORM Model for park species table."""

    __tablename__ = "parks_species"

    park_species_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey(Parks.park_id), nullable=False)
    species_id = Column(Integer, ForeignKey(Species.species_id), nullable=False)

    park_rel = relationship("Parks", back_populates="park_species_rel")
    park_species_rel = relationship("Species", back_populates="species_rel")
