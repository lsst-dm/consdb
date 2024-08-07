"""fix vignetting

Revision ID: 59776480aa4d
Revises: b801850c5cc9
Create Date: 2024-06-25 21:29:10.680116+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql, oracle

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "59776480aa4d"
down_revision: Union[str, None] = "b801850c5cc9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "exposure",
        "vignette",
        existing_type=sa.INTEGER(),
        type_=sa.VARCHAR(length=10)
        .with_variant(mysql.VARCHAR(length=10), "mysql")
        .with_variant(oracle.VARCHAR2(length=10), "oracle")
        .with_variant(sa.VARCHAR(length=10), "postgresql"),
        comment="Instrument blocked from the sky: UNKNOWN, NO, PARTIALLY, FULLY.",
        existing_comment="Instrument blocked from the sky: Unknown = 0, No = 1, Partially = 2, Fully = 3.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "vignette_min",
        existing_type=sa.INTEGER(),
        type_=sa.VARCHAR(length=10)
        .with_variant(mysql.VARCHAR(length=10), "mysql")
        .with_variant(oracle.VARCHAR2(length=10), "oracle")
        .with_variant(sa.VARCHAR(length=10), "postgresql"),
        comment="Lowest amount of instrument vignetting detected during the exposure: UNKNOWN, NO, PARTIALLY, FULLY.",
        existing_comment="Minimum value of vignette during the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "exposure",
        "vignette_min",
        existing_type=sa.VARCHAR(length=10)
        .with_variant(mysql.VARCHAR(length=10), "mysql")
        .with_variant(oracle.VARCHAR2(length=10), "oracle")
        .with_variant(sa.VARCHAR(length=10), "postgresql"),
        type_=sa.INTEGER(),
        comment="Minimum value of vignette during the exposure.",
        existing_comment="Lowest amount of instrument vignetting detected during the exposure: UNKNOWN, NO, PARTIALLY, FULLY.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "vignette",
        existing_type=sa.VARCHAR(length=10)
        .with_variant(mysql.VARCHAR(length=10), "mysql")
        .with_variant(oracle.VARCHAR2(length=10), "oracle")
        .with_variant(sa.VARCHAR(length=10), "postgresql"),
        type_=sa.INTEGER(),
        comment="Instrument blocked from the sky: Unknown = 0, No = 1, Partially = 2, Fully = 3.",
        existing_comment="Instrument blocked from the sky: UNKNOWN, NO, PARTIALLY, FULLY.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    # ### end Alembic commands ###
