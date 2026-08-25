"""Fix visit_id in ccdvisit views.

Revision ID: 913d10c6ed81
Revises: 12f0d22a2347
Create Date: 2024-12-05 00:56:53.875464+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "913d10c6ed81"
down_revision: str | None = "12f0d22a2347"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE cdb_lsstcomcam.ccdvisit1 RENAME COLUMN exposure_id TO visit_id")


def downgrade() -> None:
    op.execute("ALTER TABLE cdb_lsstcomcam.ccdvisit1 RENAME COLUMN visit_id TO exposure_id")
