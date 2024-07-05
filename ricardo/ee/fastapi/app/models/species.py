from sqlalchemy import Column, ForeignKey, Integer, String

from ricardo.ee.fastapi.app.db.base import Base


class Species(Base):
    species_id = Column(Integer, primary_key=True, index=True)
    common_name = Column(String(100), nullable=False)
    scientific_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    habitat = Column(String(100), nullable=False)
    park_id = Column(Integer, ForeignKey("parks.park_id"), nullable=False)
