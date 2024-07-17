"""modify table visitors splitting visits in their own table.

Revision ID: 0176567ad929
Revises: 08ffd8f8878a
Create Date: 2024-07-07 13:50:49.479150

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0176567ad929"
down_revision: str | None = "08ffd8f8878a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade database."""
    # Remove columns from visitor table
    op.drop_column("visitors", "visit_start_date")
    op.drop_column("visitors", "visit_end_date")
    op.drop_column("visitors", "park_id")

    op.create_table(
        "visits",
        sa.Column("visit_id", sa.Integer, primary_key=True),
        sa.Column(
            "visitor_id",
            sa.Integer,
            sa.ForeignKey("visitors.visitor_id"),
            nullable=False,
        ),
        sa.Column(
            "park_id", sa.Integer, sa.ForeignKey("parks.park_id"), nullable=False
        ),
        sa.Column("visit_start_date", sa.Date, nullable=False),
        sa.Column("visit_end_date", sa.Date),
    )


def downgrade() -> None:
    """Downgrade database."""
    op.add_column("visitors", sa.Column("visit_start_date", sa.Date, nullable=False))
    op.add_column("visitors", sa.Column("visit_end_date", sa.Date))
    op.add_column(
        "visitors", sa.Column("park_id", sa.ForeignKey("parks.park_id"), nullable=False)
    )

    op.drop_table("visits")
