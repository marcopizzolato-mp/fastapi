"""Base class for SQLAlchemy models."""

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for SQLAlchemy models.

    This base class automatically generates the `__tablename__` attribute
    from the class name by converting it to lowercase. This eliminates the
    need to manually specify the `__tablename__` attribute in each model class.

    You can still specify the `__tablename__` attribute in each model
    class for custom names.
    """

    __name__: str

    # Generate __tablename__ automatically from the Class name
    @declared_attr
    def __tablename__(cls):  # noqa ANN204
        """Automatically generate the `__tablename__` attribute from the class name.

        Args:
            cls: The class for which the table name is being generated.

        Returns:
            str: The table name derived from the class name, converted to lowercase.
        """
        return cls.__name__.lower()
