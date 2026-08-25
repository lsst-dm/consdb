"""Fix visit_id in ccdvisit views.

Revision ID: ab45b3673c90
Revises: cb09b95e12fb
Create Date: 2024-12-05 00:56:55.551902+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ab45b3673c90"
down_revision: str | None = "cb09b95e12fb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE cdb_lsstcomcamsim.ccdvisit1 RENAME COLUMN exposure_id TO visit_id")


def downgrade() -> None:
    op.execute("ALTER TABLE cdb_lsstcomcamsim.ccdvisit1 RENAME COLUMN visit_id TO exposure_id")
