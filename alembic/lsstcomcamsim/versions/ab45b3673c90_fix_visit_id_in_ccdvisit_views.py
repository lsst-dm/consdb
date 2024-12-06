"""Fix visit_id in ccdvisit views.

Revision ID: ab45b3673c90
Revises: cb09b95e12fb
Create Date: 2024-12-05 00:56:55.551902+00:00

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ab45b3673c90"
down_revision: Union[str, None] = "cb09b95e12fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE cdb_lsstcomcamsim.ccdvisit1 RENAME COLUMN exposure_id TO visit_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE cdb_lsstcomcamsim.ccdvisit1 RENAME COLUMN visit_id TO exposure_id")
    # ### end Alembic commands ###
