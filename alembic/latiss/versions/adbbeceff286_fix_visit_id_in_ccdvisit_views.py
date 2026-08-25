"""Fix visit_id in ccdvisit views.

Revision ID: adbbeceff286
Revises: 47c0b5ce839e
Create Date: 2024-12-05 00:56:52.135839+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "adbbeceff286"
down_revision: str | None = "47c0b5ce839e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE cdb_latiss.ccdvisit1 RENAME COLUMN exposure_id TO visit_id")


def downgrade() -> None:
    op.execute("ALTER TABLE cdb_latiss.ccdvisit1 RENAME COLUMN visit_id TO exposure_id")
