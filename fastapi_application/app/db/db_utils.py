"""Database utils functions."""

from collections.abc import Sequence
from typing import Literal

from fastapi_app.app.models.base import Base
from loguru import logger
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select


def query_table_as_dataframe(db_session: Session, orm_query: Select) -> pd.DataFrame:
    """Execute sqlalchemy query and return pandas dataframe.

    Args:
        db_session: database session object
        orm_query: sqlalchemy query to execute

    Returns:
        Table data as a Pandas dataframe
    """
    try:
        return pd.read_sql_query(orm_query, db_session.bind)
    except SQLAlchemyError as err:
        logger.error(f"SQLAlchemy error {err}")
        return pd.DataFrame()


def query_column_as_list(db_session: Session, orm_query: Select) -> Sequence | None:
    """Execute sqlalchemy query and return the column as a sequence.

    The function verifies only one column is queried.

    Args:
        db_session: database session object
        orm_query: sqlalchemy query to execute

    Returns:
        Sequence of column values
    """
    # Check the number of columns in the query
    if len(orm_query.column_descriptions) != 1:
        raise ValueError("Query must retrieve exactly one column.")
    try:
        return db_session.execute(orm_query).scalars().all()
    except SQLAlchemyError as err:
        logger.error(f"SQLAlchemy error {err}")
        return None


def query_value_as_scalar(db_session: Session, orm_query: Select) -> int | float | None:
    """Execute sqlalchemy query and return the value as a scalar.

    Args:
        db_session: database session object
        orm_query: sqlalchemy query to execute

    Returns:
        Cell value as Scalar value
    """
    try:
        return db_session.execute(orm_query).scalar_one()
    except SQLAlchemyError as err:
        logger.error(f"SQLAlchemy error {err}")
        return None


def insert_dataframe_into_db(
    db_session: Session,
    orm_model: Base,
    df: pd.DataFrame,
    if_exists_behaviour: Literal["fail", "replace", "append"] = "append",
) -> bool:
    """Insert dataframe into the database using the specified ORM model.

    Args:
        db_session: database session object
        orm_model: sqlalchemy query to execute
        df: dataframe to insert into the table
        if_exists_behaviour: behaviour if the table exists, defaults is 'append'

             How to behave if the table already exists.
            * fail: Raise a ValueError.
            * replace: Drop the table before inserting new values.
            * append: Insert new values to the existing table.

    Returns:
        boolean value - True if successful, False otherwise
    """
    try:
        df.to_sql(
            orm_model.__tablename__,
            con=db_session.connection(),
            if_exists=if_exists_behaviour,
            index=False,
            chunksize=10000,
            method="multi",
        )
        db_session.commit()
        return True
    except SQLAlchemyError as err:
        logger.error(f"SQLAlchemy error {err}")
        return False
