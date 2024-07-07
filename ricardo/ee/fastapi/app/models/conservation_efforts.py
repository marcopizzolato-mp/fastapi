from sqlalchemy import Column, Date, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi.app.db.base import Base


class ConservationEfforts(Base):
    __tablename__ = "conservation_efforts"

    effort_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey("parks.park_id"), nullable=False)
    effort_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Unicode(500))

    # Relationships
    park_rel = relationship("Parks", back_populates="conservation_efforts_rel")
