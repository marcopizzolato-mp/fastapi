"""conftest fixtures."""

from collections.abc import Generator
from contextlib import contextmanager
import pathlib
from typing import TypeAlias

from fastapi.testclient import TestClient
from fastapi_app.app.db.session import get_db_session_dep
from fastapi_app.app.main import app, init_db
from fastapi_app.app.models.base import Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy.orm import sessionmaker

ROOT_DIR = pathlib.Path(__file__).parent
db_path_testing = pathlib.Path(ROOT_DIR, "testing_sqlite_db.db")
testing_connection_string = f"sqlite:///{db_path_testing}"
testing_engine = create_engine(
    testing_connection_string, connect_args={"check_same_thread": False}, echo=True
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=testing_engine
)

# Define Session as a type alias for SQLAlchemy Session
Session: TypeAlias = SQLAlchemySession


@contextmanager
def get_db_session_testing() -> Generator[Session, None, None]:
    """Fixture that manages the lifecycle of the session.

    Yields:
        A SQLAlchemy session object for testing.
    """
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=testing_engine)
    Base.metadata.create_all(bind=testing_engine)

    try:
        yield session
    except Exception as e:
        session.rollback()  # Rollback on error
        raise e
    finally:
        session.close()  # Close the session
        testing_engine.dispose()
        pathlib.Path(db_path_testing).unlink(missing_ok=True)


@pytest.fixture(scope="session")
def get_db_session_dep_testing() -> Generator[Session, None, None]:
    """Fixture to provide a session.

    Yields:
        SQLAlchemy session object.
    """
    with get_db_session_testing() as session:
        yield session


@pytest.fixture(scope="session")
def dummy_client(
    get_db_session_dep_testing: Session,
) -> Generator[TestClient, None, None]:
    """Fixture that yields a FastAPI test client.

    Args:
        get_db_session_dep_testing: Fixture to provide a new database session.

    Yields:
        A FastAPI test client with overridden database dependency.
    """

    def override_db_session_dependency():
        yield get_db_session_dep_testing

    def override_init_db():
        pass

    app.dependency_overrides[get_db_session_dep] = override_db_session_dependency
    app.dependency_overrides[init_db] = override_init_db
    with TestClient(app) as client:
        yield client
    del app.dependency_overrides[get_db_session_dep]
