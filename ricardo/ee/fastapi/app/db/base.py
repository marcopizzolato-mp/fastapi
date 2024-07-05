"""Contains the base class for SQLAlchemy models."""

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class Base:
    __name__: str

    # Generate __tablename__ automatically from the Class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
