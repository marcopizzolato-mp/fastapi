"""SQLAlchemy Database Session."""

from collections.abc import Generator
from contextlib import contextmanager
import os
from typing import TypeAlias

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

db_host = os.getenv("DEFAULT_POSTGRES_HOST")
db_user = os.getenv("DEFAULT_POSTGRES_USER")
db_password = os.getenv("DEFAULT_POSTGRES_PASSWORD")
db_name = os.getenv("DEFAULT_DB_NAME")

# Database connection string
connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(
    connection_string,
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define Session as a type alias for SQLAlchemy Session
Session: TypeAlias = SQLAlchemySession


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Contextmnager function that provides a database session.

        This function manages the lifecycle of the session (opening, closing,
        and handling exceptions)

    Returns:
        Database session object
    """
    session = SessionLocal()
    logger.info("Database session opened.")
    try:
        yield session
    except Exception as e:
        logger.error(f"An error with the database occurred {e}.")
        session.rollback()  # Rollback on error
        raise
    finally:
        logger.info("Database session closed.")
        session.close()  # Close the session


def get_db_session_dep() -> Generator[Session, None, None]:
    """Generator function that uses the context manager.

    This function is used as a dependency in the API routes.
    The advantage of having this generator function wrapper around the contextmanager,
    and be able to use the Depends() in the APIs, makes it easier to create
    mocks when testing. Other advantages are consistency and reusability.

    Returns:
        Database session object

    """
    with get_db_session() as session:
        yield session
