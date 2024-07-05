from sqlalchemy import Column, ForeignKey, Integer, String, Unicode

from ricardo.ee.fastapi.app.db.base import Base


class ParkFacility(Base):
    facility_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey("parks.park_id"), nullable=False)
    facility_type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Unicode(500))
