"""create first revision.

Revision ID: 6414c769b1ba
Revises:
Create Date: 2024-07-04 22:13:41.735464
"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "6414c769b1ba"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade database."""
    pass


def downgrade() -> None:
    """Downgrade database."""
    pass
