"""create tables parks species visitors conservation facilities

Revision ID: 3220c42dd31e
Revises: 6414c769b1ba
Create Date: 2024-07-04 22:35:15.759824

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3220c42dd31e"
down_revision: str | None = "6414c769b1ba"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "parks",
        sa.Column("park_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("location", sa.String(100), nullable=False),
        sa.Column("area", sa.Float, nullable=False),
        sa.Column("established_date", sa.Date, nullable=False),
        sa.Column("description", sa.Unicode(500)),
        sa.Column("type", sa.String(50), nullable=False),
    )

    op.create_table(
        "species",
        sa.Column("species_id", sa.Integer, primary_key=True),
        sa.Column("common_name", sa.String(100), nullable=False),
        sa.Column("scientific_name", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("habitat", sa.String(100), nullable=False),
        sa.Column(
            "park_id", sa.Integer, sa.ForeignKey("parks.park_id"), nullable=False
        ),
    )

    op.create_table(
        "visitors",
        sa.Column("visitor_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("visit_date", sa.Date, nullable=False),
        sa.Column(
            "park_id", sa.Integer, sa.ForeignKey("parks.park_id"), nullable=False
        ),
    )

    op.create_table(
        "conservation_efforts",
        sa.Column("effort_id", sa.Integer, primary_key=True),
        sa.Column(
            "park_id", sa.Integer, sa.ForeignKey("parks.park_id"), nullable=False
        ),
        sa.Column("effort_name", sa.String(100), nullable=False),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date),
        sa.Column("description", sa.Unicode(500)),
    )

    op.create_table(
        "park_facilities",
        sa.Column("facility_id", sa.Integer, primary_key=True),
        sa.Column(
            "park_id", sa.Integer, sa.ForeignKey("parks.park_id"), nullable=False
        ),
        sa.Column("facility_type", sa.String(50), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Unicode(500)),
    )


def downgrade() -> None:
    op.drop_table("park_facilities")
    op.drop_table("conservation_efforts")
    op.drop_table("visitors")
    op.drop_table("species")
    op.drop_table("parks")
