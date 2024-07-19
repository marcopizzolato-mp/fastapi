"""Application entry point with FastAPI instance and routes."""

import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from ricardo.ee.fastapi_app.app import api_utils
from ricardo.ee.fastapi_app.app.api.routers.routers import api_router
from ricardo.ee.fastapi_app.app.models.base import init_db


def init_app() -> FastAPI:
    """Initialise the FastAPI app."""
    app = FastAPI(
        title="Parks and Protected areas data API",
        version="0.0.1",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Remove the default handler and add a new one with log level set to INFO
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    # Get an instance of the ApiLogHandler and add this handler as a sink
    api_log_handler = api_utils.ApiLogHandler()
    logger.add(
        api_log_handler,
        level="INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        ),
    )

    return app


# Initialise the database
init_db()
# Initialise FastAPI App
app = init_app()
app.include_router(api_router, prefix="/api")


@app.get("/live")
def liveness() -> dict:
    """Check API is live."""
    return {"status": "okay"}


# uvicorn ricardo.ee.fastapi_app.app.main:app --reload
