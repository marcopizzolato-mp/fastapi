from sqlalchemy import Column, Date, Float, Integer, String, Unicode
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi.app.db.base import Base


class Parks(Base):
    park_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    area = Column(Float, nullable=False)
    established_date = Column(Date, nullable=False)
    description = Column(Unicode(500))
    type = Column(String(50), nullable=False)

    # Relationships
    park_species_rel = relationship("ParksSpecies", back_populates="park_rel")
    visits_rel = relationship("ParkVisits", back_populates="park_rel")
    conservation_efforts_rel = relationship(
        "ConservationEfforts", back_populates="park_rel"
    )
    facilities_rel = relationship("ParkFacilities", back_populates="park_rel")
