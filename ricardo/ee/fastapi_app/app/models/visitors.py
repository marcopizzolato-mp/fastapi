"""ORM Model."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi_app.app.models.base import Base


class Visitors(Base):
    """ORM Model for Visitors table."""

    visitor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    visits_rel = relationship("ParkVisits", back_populates="visitor_rel")
