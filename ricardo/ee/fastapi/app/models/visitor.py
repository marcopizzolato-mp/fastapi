from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ricardo.ee.fastapi.app.db.base import Base


class Visitor(Base):
    visitor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    visit_date = Column(Date, nullable=False)
    park_id = Column(Integer, ForeignKey("parks.park_id"), nullable=False)

    # Relationship
    park = relationship("Park", back_populates="visitors")
