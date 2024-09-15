"""Pydantic modules."""

from datetime import date

from pydantic import BaseModel


class DummySchema(BaseModel):
    """Response model for Dummy."""

    unique_id: int
    created_at: date
    modified_at: date


class ParksSchema(BaseModel):
    """Response model for Parks."""

    park_id: int
    name: str
    location: str
    established_date: date
    description: str | None
    type: str
    geometry_id: int
    created_at: date
    modified_at: date

    # Fields from the Relationships
    species_rel: list["SpeciesSchema"] | None
    visitors_rel: list["VisitorsSchema"] | None
    conservation_efforts_rel: list["ConservationEffortsSchema"] | None
    park_facilities_rel: list["ParkFacilitiesSchema"] | None
    park_geom_rel: list["ParkGeometrySchema"] | None


class SpeciesSchema(BaseModel):
    """Response model for Species."""

    species_id: int
    common_name: str
    scientific_name: str
    status: str
    habitat: str
    description: str


class VisitorsSchema(BaseModel):
    """Response model for Visitors."""

    visitor_id: int
    name: str
    email: str

    # Fields from the Relationships
    visits_rel: list["VisitsSchema"] | None


class VisitsSchema(BaseModel):
    """Response model for Visits."""

    visit_id: int
    visitor_id: int
    park_id: int
    visit_start_date: date
    visit_end_date: date


class ConservationEffortsSchema(BaseModel):
    """Response model for ConservationEffort."""

    effort_id: int
    park_id: int
    effort_name: str
    start_date: date
    end_date: date | None
    description: str | None
    created_at: date
    modified_at: date


class ParkFacilitiesSchema(BaseModel):
    """Response model for ParkFacilities."""

    facility_id: int
    park_id: int
    facility_type: str
    name: str
    description: str | None

    # class Config:
    #     orm_mode = True
