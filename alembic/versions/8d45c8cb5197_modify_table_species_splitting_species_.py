"""modify table species splitting species_park in their own table

Revision ID: 8d45c8cb5197
Revises: 0176567ad929
Create Date: 2024-07-07 16:32:47.003977

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8d45c8cb5197"
down_revision: str | None = "0176567ad929"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("species", "park_id")
    op.add_column("species", sa.Column("description", sa.Unicode(500)))

    (
        op.create_table(
            "parks_species",
            sa.Column("park_species_id", sa.Integer, primary_key=True),
            sa.Column("park_id", sa.Integer, sa.ForeignKey("parks.park_id")),
            sa.Column(
                "species_id",
                sa.Integer,
                sa.ForeignKey("species.species_id"),
            ),
        )
    )


def downgrade() -> None:
    op.add_column("species", sa.Column("park_id", sa.Integer()))
    op.drop_column("species", "description")
    op.drop_table("parks_species")
