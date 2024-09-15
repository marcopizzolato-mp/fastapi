"""ORM Model."""

from typing import ClassVar

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from fastapi_application.app.models.base import Base
from fastapi_application.app.models.parks import Parks


class ConservationEfforts(Base):
    """ORM Model for conservation efforts table."""

    __tablename__ = "conservation_efforts"
    __table_args__: ClassVar[dict] = {"schema": "natural_parks_schema"}

    effort_id = Column(Integer, primary_key=True, index=True)
    park_id = Column(Integer, ForeignKey(Parks.park_id), nullable=False)
    effort_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    description = Column(Unicode(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    park_rel = relationship("Parks", back_populates="conservation_efforts_rel")
