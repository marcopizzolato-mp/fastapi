"""FastAPI endpoints for Visitors."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ricardo.ee.fastapi_app.app.db.db_utils import query_table_as_dataframe
from ricardo.ee.fastapi_app.app.db.session import get_db_session_dep
from ricardo.ee.fastapi_app.app.models.visitors import Visitors
from ricardo.ee.fastapi_app.app.schemas.schemas import VisitorsSchema

visitors_router = APIRouter()

# Module-level variable for the dependency
# The Depends() is passed in the API function as a variable to comply with the B008
db_session_dependency = Depends(get_db_session_dep)


@visitors_router.get(
    "/visitors",
    status_code=status.HTTP_200_OK,
    summary="Get information on the visitors",
    response_model=VisitorsSchema,
)
def get_all_visitors(db_session: Session = db_session_dependency) -> Response:
    """Return the content of the Visitors table in json format.

    Args:
        db_session: database session object

    Returns:
        json file with visitors data
    """
    visitors_query = select(Visitors)
    visitors_df = query_table_as_dataframe(
        db_session=db_session, orm_query=visitors_query
    )

    return Response(
        visitors_df.to_json(orient="records"),
        media_type="application/json",
    )
