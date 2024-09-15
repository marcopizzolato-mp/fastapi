"""modify table visitors adding strt and end date for the visit.

Revision ID: 08ffd8f8878a
Revises: 3220c42dd31e
Create Date: 2024-07-06 15:40:09.144451

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "08ffd8f8878a"
down_revision: str | None = "3220c42dd31e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade database."""
    # Remove the visit_date column
    op.drop_column("visitors", "visit_date")

    # Add the new visit_start_date and visit_end_date columns
    op.add_column("visitors", sa.Column("visit_start_date", sa.Date, nullable=False))
    op.add_column("visitors", sa.Column("visit_end_date", sa.Date))


def downgrade() -> None:
    """Downgrade database."""
    # Remove the new columns
    op.drop_column("visitors", "visit_start_date")
    op.drop_column("visitors", "visit_end_date")

    # Add the old visit_date column back
    op.add_column("visitors", sa.Column("visit_date", sa.Date, nullable=False))
