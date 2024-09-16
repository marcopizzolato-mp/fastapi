"""ORM Model."""

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models.base import Base


class Visitors(Base):
    """ORM Model for Visitors table."""

    __table_args__ = {"schema": "natural_parks_schema"}  # noqa RUF012

    visitor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    marketing_consent = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    visits_rel = relationship("ParkVisits", back_populates="visitor_rel")
