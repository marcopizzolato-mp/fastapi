from sqlalchemy import Column, Date, Float, Integer, String, Unicode
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi.app.db.base import Base


class Park(Base):
    park_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    area = Column(Float, nullable=False)
    established_date = Column(Date, nullable=False)
    description = Column(Unicode(500))
    type = Column(String(50), nullable=False)

    # Relationships
    species = relationship("Species", back_populates="park")
    visitors = relationship("Visitor", back_populates="park")
    conservation_efforts = relationship("ConservationEffort", back_populates="park")
    facilities = relationship("Facility", back_populates="park")
