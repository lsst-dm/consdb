"""add vignetting

Revision ID: b801850c5cc9
Revises: 535c454d7311
Create Date: 2024-06-25 09:42:17.989898+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision: str = "b801850c5cc9"
down_revision: Union[str, None] = "535c454d7311"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ccdvisit1_quicklook",
        "eff_time_psf_sky_bg_scale",
        new_column_name="eff_time_sky_bg_scale",
        comment="Scale factor for effective exposure time based on sky background.",
        schema="cdb_latiss",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "eff_time_psf_zero_point_scale",
        new_column_name="eff_time_zero_point_scale",
        comment="Scale factor for effective exposure time based on zero point.",
        schema="cdb_latiss",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "eff_time_psf_sigma_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Scale factor for effective exposure time based on PSF sigma.",
        existing_comment="Effective exposure time, PSF sigma scale.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.add_column(
        "exposure",
        sa.Column(
            "vignette",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Instrument blocked from the sky: Unknown = 0, No = 1, Partially = 2, Fully = 3.",
        ),
        schema="cdb_latiss",
    )
    op.add_column(
        "exposure",
        sa.Column(
            "vignette_min",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Minimum value of vignette during the exposure.",
        ),
        schema="cdb_latiss",
    )
    op.alter_column(
        "visit1_quicklook",
        "eff_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Effective exposure time calculated from PSF sigma, sky background, and zero point.",
        existing_comment="Effective exposure time.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "visit1_quicklook",
        "eff_time_psf_sigma_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Scale factor for effective exposure time based on PSF sigma.",
        existing_comment="Effective exposure time, PSF sigma scale.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "visit1_quicklook",
        "eff_time_sky_bg_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Scale factor for effective exposure time based on sky background.",
        existing_comment="Effective exposure time, sky background scale.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "visit1_quicklook",
        "eff_time_zero_point_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Scale factor for effective exposure time based on zero point.",
        existing_comment="Effective exposure time, zero point scale.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "visit1_quicklook",
        "eff_time_zero_point_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Effective exposure time, zero point scale.",
        existing_comment="Scale factor for effective exposure time based on zero point.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "visit1_quicklook",
        "eff_time_sky_bg_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Effective exposure time, sky background scale.",
        existing_comment="Scale factor for effective exposure time based on sky background.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "visit1_quicklook",
        "eff_time_psf_sigma_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Effective exposure time, PSF sigma scale.",
        existing_comment="Scale factor for effective exposure time based on PSF sigma.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "visit1_quicklook",
        "eff_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Effective exposure time.",
        existing_comment="Effective exposure time calculated from PSF sigma, sky background, and zero point.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.drop_column("exposure", "vignette_min", schema="cdb_latiss")
    op.drop_column("exposure", "vignette", schema="cdb_latiss")
    op.alter_column(
        "ccdvisit1_quicklook",
        "eff_time_zero_point_scale",
        new_column_name="eff_time_psf_zero_point_scale",
        comment="Effective exposure time, zero point scale.",
        schema="cdb_latiss",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "eff_time_sky_bg_scale",
        new_column_name="eff_time_psf_sky_bg_scale",
        comment="Effective exposure time, sky backgroundscale.",
        schema="cdb_latiss",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "eff_time_psf_sigma_scale",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Effective exposure time, PSF sigma scale.",
        existing_comment="Scale factor for effective exposure time based on PSF sigma.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    # ### end Alembic commands ###