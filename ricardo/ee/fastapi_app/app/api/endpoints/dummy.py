"""FastAPI endpoints."""

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ricardo.ee.fastapi_app.app.db.db_utils import query_table_as_dataframe
from ricardo.ee.fastapi_app.app.db.session import get_db_session_dep
from ricardo.ee.fastapi_app.app.models.dummy_orm import Dummy
from ricardo.ee.fastapi_app.app.schemas.schemas import VisitorsSchema

dummy_router = APIRouter()

# Module-level variable for the dependency
# The Depends() is passed in the API function as a variable to comply with the B008
db_session_dependency = Depends(get_db_session_dep)


@dummy_router.get(
    "/dummy",
    status_code=status.HTTP_200_OK,
    summary="Get database from the database.",
    response_model=VisitorsSchema,
)
def get_dummy_data(db_session: Session = db_session_dependency) -> Response:
    """Return the content of the Dummy table in json format.

    Args:
        db_session: database session object

    Returns:
        json file with dummy data
    """
    dummy_query = select(Dummy)
    dummy_df = query_table_as_dataframe(db_session=db_session, orm_query=dummy_query)

    return Response(
        dummy_df.to_json(orient="records"),
        media_type="application/json",
    )
