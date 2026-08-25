"""Add truss temperature

Revision ID: 32db1f589156
Revises: f0e8602d7819
Create Date: 2026-02-02 17:14:04.823186+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "32db1f589156"
down_revision: str | None = "f0e8602d7819"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "exposure_efd",
        sa.Column(
            "mt_salindex122_temperature_6",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="M2-ESS02, temperature item 6, plus X plus Y Truss Structure",
        ),
        schema="efd_lsstcam",
    )
    op.add_column(
        "exposure_efd",
        sa.Column(
            "mt_salindex122_temperature_7",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="M2-ESS02, temperature item 7, minus X minus Y Truss Structure",
        ),
        schema="efd_lsstcam",
    )
    op.add_column(
        "visit1_efd",
        sa.Column(
            "mt_salindex122_temperature_6",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="M2-ESS02, temperature item 6, plus X plus Y Truss Structure",
        ),
        schema="efd_lsstcam",
    )
    op.add_column(
        "visit1_efd",
        sa.Column(
            "mt_salindex122_temperature_7",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="M2-ESS02, temperature item 7, minus X minus Y Truss Structure",
        ),
        schema="efd_lsstcam",
    )


def downgrade() -> None:
    op.drop_column("visit1_efd", "mt_salindex122_temperature_7", schema="efd_lsstcam")
    op.drop_column("visit1_efd", "mt_salindex122_temperature_6", schema="efd_lsstcam")
    op.drop_column("exposure_efd", "mt_salindex122_temperature_7", schema="efd_lsstcam")
    op.drop_column("exposure_efd", "mt_salindex122_temperature_6", schema="efd_lsstcam")
