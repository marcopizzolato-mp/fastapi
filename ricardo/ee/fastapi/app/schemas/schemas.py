from datetime import date

from pydantic import BaseModel


class ParksSchema(BaseModel):
    """Response model for Parks."""

    park_id: int
    name: str
    location: str
    area: float
    established_date: date
    description: str | None
    type: str

    # Fields from the Relationships
    species_rel: list["Species"] | None
    visitors_rel: list["Visitors"] | None
    conservation_efforts_rel: list["ConservationEfforts"] | None
    park_facilities_rel: list["ParkFacilities"] | None


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
    visits_rel: list["Visits"] | None


class VisitsSchema(BaseModel):
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


class ParkFacilitiesSchema(BaseModel):
    """Response model for ParkFacilities."""

    facility_id: int
    park_id: int
    facility_type: str
    name: str
    description: str | None
