from sqlalchemy import Column, Date, Float, Integer, String, Unicode

from ricardo.ee.fastapi.app.db.base import Base


class Park(Base):
    park_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    area = Column(Float, nullable=False)
    established_date = Column(Date, nullable=False)
    description = Column(Unicode(500))
    type = Column(String(50), nullable=False)
