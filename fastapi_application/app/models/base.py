"""Base class for SQLAlchemy models."""

import re

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
                str: The table name derived from the class name, converted to lowercase
                and concerted from CamelCase to snake_case.
        """
        # Detect CamelCase and replace with underscores
        camel_case_pattern = re.compile(r"(?<!^)(?=[A-Z])")
        formatted_name = camel_case_pattern.sub("_", cls.__name__).lower()
        return formatted_name

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
    #     return {"schema": "public"}  # Specify the schema here
