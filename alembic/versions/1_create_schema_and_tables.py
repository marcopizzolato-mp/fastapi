"""Create schema and tables.

Revision ID: 1
Revises:
Create Date: 2024-09-15 22:06:36.388181

"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "44f3ffb16020"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade database."""
    op.create_table(
        "parks",
        sa.Column("park_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(length=100), nullable=False),
        sa.Column("established_date", sa.Date(), nullable=False),
        sa.Column("description", sa.Unicode(length=500), nullable=True),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("park_id"),
        schema="natural_parks_schema",
    )

    op.create_table(
        "species",
        sa.Column("species_id", sa.Integer(), nullable=False),
        sa.Column("common_name", sa.String(length=100), nullable=False),
        sa.Column("scientific_name", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("habitat", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Unicode(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("species_id"),
        schema="natural_parks_schema",
    )

    op.create_table(
        "visitors",
        sa.Column("visitor_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("marketing_consent", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("visitor_id"),
        schema="natural_parks_schema",
    )

    op.create_table(
        "conservation_efforts",
        sa.Column("effort_id", sa.Integer(), nullable=False),
        sa.Column("park_id", sa.Integer(), nullable=False),
        sa.Column("effort_name", sa.String(length=100), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sa.Unicode(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["park_id"],
            ["natural_parks_schema.parks.park_id"],
        ),
        sa.PrimaryKeyConstraint("effort_id"),
        schema="natural_parks_schema",
    )

    op.create_table(
        "geometry_parks",
        sa.Column("park_id", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(geometry_type="POLYGON", srid=4326),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["park_id"],
            ["natural_parks_schema.parks.park_id"],
        ),
        sa.PrimaryKeyConstraint("park_id"),
        schema="natural_parks_schema",
    )

    op.create_table(
        "park_facilities",
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("park_id", sa.Integer(), nullable=False),
        sa.Column("facility_type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("working", sa.Boolean(), nullable=False),
        sa.Column("description", sa.Unicode(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["park_id"],
            ["natural_parks_schema.parks.park_id"],
        ),
        sa.PrimaryKeyConstraint("facility_id"),
        schema="natural_parks_schema",
    )

    op.create_table(
        "parks_species",
        sa.Column("park_species_id", sa.Integer(), nullable=False),
        sa.Column("park_id", sa.Integer(), nullable=False),
        sa.Column("species_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["park_id"],
            ["natural_parks_schema.parks.park_id"],
        ),
        sa.ForeignKeyConstraint(
            ["species_id"],
            ["natural_parks_schema.species.species_id"],
        ),
        sa.PrimaryKeyConstraint("park_species_id"),
        schema="natural_parks_schema",
    )

    op.create_table(
        "parks_visits",
        sa.Column("visit_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("park_id", sa.Integer(), nullable=False),
        sa.Column("visitor_id", sa.Integer(), nullable=False),
        sa.Column("visit_start_date", sa.Date(), nullable=False),
        sa.Column("visit_end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["park_id"],
            ["natural_parks_schema.parks.park_id"],
        ),
        sa.ForeignKeyConstraint(
            ["visitor_id"],
            ["natural_parks_schema.visitors.visitor_id"],
        ),
        sa.PrimaryKeyConstraint("visit_id"),
        schema="natural_parks_schema",
    )
    op.create_table(
        "geometry_facilities",
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(geometry_type="POINT", srid=4326),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["natural_parks_schema.park_facilities.facility_id"],
        ),
        sa.PrimaryKeyConstraint("facility_id"),
        schema="natural_parks_schema",
    )


def downgrade() -> None:
    """Downgrade database."""
    op.drop_table("geometry_facilities", schema="natural_parks_schema")
    op.drop_table("parks_visits", schema="natural_parks_schema")
    op.drop_table("parks_species", schema="natural_parks_schema")
    op.drop_table("park_facilities", schema="natural_parks_schema")
    op.drop_table("geometry_parks", schema="natural_parks_schema")
    op.drop_table("conservation_efforts", schema="natural_parks_schema")
    op.drop_table("visitors", schema="natural_parks_schema")
    op.drop_table("species", schema="natural_parks_schema")
    op.drop_table("parks", schema="natural_parks_schema")

    # -- End Alembic commands
