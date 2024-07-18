"""API routing module."""

from fastapi import APIRouter

from ..endpoints.parks import parks_router
from ..endpoints.species import species_router
from ..endpoints.visitor import visitors_router

api_router = APIRouter()

api_router.include_router(visitors_router, prefix="/visitor_info")
api_router.include_router(parks_router, prefix="/park_info")
api_router.include_router(species_router, prefix="/species_info")
