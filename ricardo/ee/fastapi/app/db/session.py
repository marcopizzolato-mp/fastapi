"""Database Session."""

from contextlib import contextmanager
import os

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

db_host = os.getenv("DEFAULT_POSTGRES_HOST")
db_user = os.getenv("DEFAULT_POSTGRES_USER")
db_password = os.getenv("DEFAULT_POSTGRES_PASSWORD")
db_name = os.getenv("DEFAULT_DB_NAME")


@contextmanager
def get_db_session():
    connection_string = (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )
    print(connection_string)
    engine = create_engine(
        connection_string,
        # connect_args={"check_same_thread": False}, # This is only for SQLLite
        echo=True,
    )
    metadata = MetaData()
    db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = db_session()
    logger.info("Database session opened.")
    print("Database session opened.")
    try:
        yield session
    except Exception as e:
        logger.error(f"An error with the database occurred {e}.")
    finally:
        logger.info("Database session closed.")
        print("Database session closed.")
        session.close()
