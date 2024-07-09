"""Application entry point with FastAPI instance and routes."""

from api.api_v1.routers.routes import api_router

from fastapi import FastAPI

app = FastAPI(
    title="Parks and Protected areas data API",
    version="0.0.1",
)

app.include_router(api_router, prefix="/api")


@app.get("/live")
def liveness() -> dict:
    """Check API is live."""
    return {"status": "okay"}


# uvicorn ricardo.ee.fastapi.app.main:app --reload
