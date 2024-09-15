"""FastAPI endpoints for Parks."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ricardo.ee.fastapi_app.app.db.db_utils import query_table_as_dataframe
from ricardo.ee.fastapi_app.app.db.session import get_db_session_dep
from ricardo.ee.fastapi_app.app.models.parks import Parks
from ricardo.ee.fastapi_app.app.schemas.schemas import ParksSchema

parks_router = APIRouter()

# Module-level variable for the dependency
# The Depends() is passed in the API function as a variable to comply with the B008
db_session_dependency = Depends(get_db_session_dep)


@parks_router.get(
    "/parks",
    status_code=status.HTTP_200_OK,
    summary="Get information on all the parks",
    response_model=ParksSchema,
)
def get_all_parks(session: Session = db_session_dependency) -> Response:
    """Return the content of the Parks table in json format.

    Parks details are returned as follows:
    {"ScenarioID": [1], "ScenarioName": ["dummy_scenario"]}

    Args:
        session: database session object

    Returns:
        json file with parks data
    """
    parks_query = select(Parks)
    parks_df = query_table_as_dataframe(db_session=session, orm_query=parks_query)
    return Response(
        parks_df.to_json(orient="records"),
        media_type="application/json",
    )


@parks_router.get(
    "/parks/{park_id}",
    status_code=status.HTTP_200_OK,
    summary="Get information on a specific park",
    response_model=ParksSchema,
)
def get_park_by_id(park_id: int, session: Session = db_session_dependency) -> Response:
    """Return the content of the Parks table in json format for a specific park.

    Parks details are returned as follows:
    {"ScenarioID": [1], "ScenarioName": ["dummy_scenario"]}

    Args:
        park_id: park id
        session: database session object

    Returns:
        json file with parks data
    """
    parks_query = select(Parks).filter_by(park_id=park_id)
    parks_df = query_table_as_dataframe(db_session=session, orm_query=parks_query)
    if parks_df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Park not found"
        )
    return Response(
        parks_df.to_json(orient="records"),
        media_type="application/json",
    )
