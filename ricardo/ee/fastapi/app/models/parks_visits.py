from sqlalchemy import Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi.app.db.base import Base


class ParkVisits(Base):
    """ORM Model for Park visits table."""

    __tablename__ = "parks_visits"

    visit_id = Column(Integer, primary_key=True, autoincrement=True)
    park_id = Column(Integer, ForeignKey("parks.park_id"), nullable=False)
    visitor_id = Column(Integer, ForeignKey("visitors.visitor_id"), nullable=False)
    visit_start_date = Column(Date, nullable=False)
    visit_end_date = Column(Date)

    # Relationship
    park_rel = relationship("Parks", back_populates="visits_rel")
    visitor_rel = relationship("Visitors", back_populates="visits_rel")
