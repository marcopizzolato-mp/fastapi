"""Base class for SQLAlchemy models."""

from fastapi_app.app.db.session import engine
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    @declared_attr
    def __tablename__(cls):  # noqa ANN204
        """Automatically generate the `__tablename__` attribute from the class name.

        This  eliminates the need to manually specify the `__tablename__` attribute
        in each model class.
        You can still specify the `__tablename__` attribute in each model

        Args:
                cls: The class for which the table name is being generated.

        Returns:
                str: The table name derived from the class name, converted to lowercase.
        """
        return cls.__name__.lower()

    # @declared_attr
    # def __table_args__(cls):  # ANN204
    #     """Set the schema for the table.
    #
    #     If the database is SQLite it will ignore the schema.
    #
    #     Args:
    #         cls: The class for which the schema is being set.
    #
    #     Returns:
    #         dict: A dictionary containing the schema name.
    #     """
    #     print(engine.dialect.name)
    #
    #     if engine.dialect.name != "sqlite":
    #         return {"schema": "public"}  # Specify schema for non-SQLite engines
    #     else:
    #         return {}  # No schema for SQLite
    #     # return {"schema": "public"}  # Specify the schema here


def init_db() -> None:
    """Initialize the database using the Metadata creating tables if they don't exist.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)
