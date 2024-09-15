"""ORM Model."""

from fastapi_app.app.models.base import Base
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func


class Dummy(Base):
    """ORM Model for Dummy table."""

    unique_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
