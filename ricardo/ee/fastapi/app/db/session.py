"""Database Session."""

import os

from loguru import logger
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

db_host = os.getenv("DEFAULT_POSTGRES_HOST")
db_user = os.getenv("DEFAULT_POSTGRES_USER")
db_password = os.getenv("DEFAULT_POSTGRES_PASSWORD")
db_name = os.getenv("DEFAULT_DB_NAME")

connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(
    connection_string,
    connect_args={"check_same_thread": False},
    echo=True,
)
metadata = MetaData()
database_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db_session():
    db_session = database_session()
    logger.info("Database session opened.")
    try:
        yield db_session
    except Exception as e:
        logger.error(f"An error with the database occurred {e}.")
    finally:
        logger.error("Database session closed.")
        db_session.close()
