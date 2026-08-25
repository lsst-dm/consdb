"""Add astrometric RA and Dec to quicklook tables

Revision ID: 07d289e251ec
Revises: 42cf2352803d
Create Date: 2026-02-05 20:10:24.844899+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "07d289e251ec"
down_revision: str | None = "42cf2352803d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "exposure",
        "s_ra",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; right ascension of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_comment="Central Spatial Position in ICRS; Right ascension of targeted focal plane center.",
        existing_nullable=True,
        schema="cdb_lsstcomcamsim",
    )
    op.alter_column(
        "exposure",
        "s_dec",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; declination of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_comment="Central Spatial Position in ICRS; Declination of targeted focal plane center.",
        existing_nullable=True,
        schema="cdb_lsstcomcamsim",
    )


def downgrade() -> None:
    op.alter_column(
        "exposure",
        "s_dec",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; Declination of targeted focal plane center.",
        existing_comment="Central Spatial Position in ICRS; declination of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_nullable=True,
        schema="cdb_lsstcomcamsim",
    )
    op.alter_column(
        "exposure",
        "s_ra",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; Right ascension of targeted focal plane center.",
        existing_comment="Central Spatial Position in ICRS; right ascension of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_nullable=True,
        schema="cdb_lsstcomcamsim",
    )
