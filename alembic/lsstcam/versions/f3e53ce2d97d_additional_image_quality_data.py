"""Additional image quality data.

Revision ID: f3e53ce2d97d
Revises: f49cf86ea2bd
Create Date: 2026-09-07 19:25:57.229360+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql, postgresql

# revision identifiers, used by Alembic.
revision: str = "f3e53ce2d97d"
down_revision: str | None = "f49cf86ea2bd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "ccdvisit1_quicklook",
        sa.Column(
            "z4_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic defocus (Z4) in OCS in microns.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "ccdvisit1_quicklook",
        sa.Column(
            "z11_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic primary spherical (Z11) in OCS in microns.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "ccdvisit1_quicklook",
        sa.Column(
            "z22_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic secondary spherical (Z22) in OCS in microns.",
        ),
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z4",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total defocus (Z4) in OCS, in microns.",
        existing_comment="Estimated defocus (Z4), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z5",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique primary astigmatism (Z5) in OCS, in microns.",
        existing_comment="Estimated oblique primary astigmatism (Z5), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z6",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical primary astigmatism (Z6) in OCS, in microns.",
        existing_comment="Estimated vertical primary astigmatism (Z6), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z7",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical primary coma (Z7) in OCS, in microns.",
        existing_comment="Estimated vertical primary coma (Z7), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z8",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total horizontal primary coma (Z8) in OCS, in microns.",
        existing_comment="Estimated horizontal primary coma (Z8), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z9",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical trefoil (Z9) in OCS, in microns.",
        existing_comment="Estimated vertical trefoil (Z9), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z10",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique trefoil (Z10) in OCS, in microns.",
        existing_comment="Estimated horizontal trefoil (Z10), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z11",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total primary spherical (Z11) in OCS, in microns.",
        existing_comment="Estimated primary spherical (Z11), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z12",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary astigmatism (Z12) in OCS, in microns.",
        existing_comment="Estimated vertical secondary astigmatism (Z12), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z13",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique secondary astigmatism (Z13) in OCS, in microns.",
        existing_comment="Estimated oblique secondary astigmatism (Z13), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z14",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical quadrafoil (Z14) in OCS, in microns.",
        existing_comment="Estimated vertical quadrafoil (Z14), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z15",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique quadrafoil (Z15) in OCS, in microns.",
        existing_comment="Estimated horizontal quadrafoil (Z15), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z16",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total horizontal secondary coma (Z16) in OCS, in microns.",
        existing_comment="Estimated horizontal secondary coma (Z16), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z17",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary coma (Z17) in OCS, in microns.",
        existing_comment="Estimated vertical secondary coma (Z17), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z18",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique secondary trefoil (Z18) in OCS, in microns.",
        existing_comment="Estimated oblique secondary trefoil (Z18), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z19",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary trefoil (Z19) in OCS, in microns.",
        existing_comment="Estimated vertical secondary trefoil (Z19), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z20",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique pentafoil (Z20) in OCS, in microns.",
        existing_comment="Estimated oblique pentafoil (Z20), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z21",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical pentafoil (Z21) in OCS, in microns.",
        existing_comment="Estimated vertical pentafoil (Z21), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z22",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total secondary spherical (Z22) in OCS, in microns.",
        existing_comment="Estimated secondary spherical (Z22), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z23",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total tertiary astigmatism (Z23) in OCS, in microns.",
        existing_comment="Estimated tertiary astimgatism (Z23), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z24",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total tertiary astigmatism (Z24) in OCS, in microns.",
        existing_comment="Estimated tertiary astimgatism (Z24), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z25",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique secondary quadrafoil (Z25) in OCS, in microns.",
        existing_comment="Estimated oblique secondary quadrafoil (Z25), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z26",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary quadrafoil (Z26) in OCS, in microns.",
        existing_comment="Estimated vertical secondary quadrafoil (Z26), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z27",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total hexafoil (Z27) in OCS, in microns.",
        existing_comment="Estimated hexafoil (Z27), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z28",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total hexafoil (Z28) in OCS, in microns.",
        existing_comment="Estimated hexafoil (Z28), in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.add_column(
        "exposure_quicklook",
        sa.Column(
            "ra_package_versions",
            sa.TEXT()
            .with_variant(mysql.LONGTEXT(), "mysql")
            .with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql"),
            nullable=True,
            comment="Packages such as ts_wep, donut_viz, tarts, danish versions used for processing.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "exposure_quicklook",
        sa.Column(
            "mtaos_package_versions",
            sa.TEXT()
            .with_variant(mysql.LONGTEXT(), "mysql")
            .with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql"),
            nullable=True,
            comment="mtaos package versions used.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_sigma_95",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF sigma (95% across all detectors).",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_sigma_05",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF sigma (5% across all detectors).",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_fwhm_x_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF FWHM X Gradient calculated as Z2,fwhm in OCS in arcsec/deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_fwhm_y_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF FWHM Y Gradient calculated as Z3,fwhm in OCS in arcsec/deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_fwhm_radial_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF FWHM radial gradient, calculated as Z4,fwhm in arcsec/deg2.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_ellipticity_median",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Ellipticity median across all detectors.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_ellipticity_95",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Ellipticity 95% across all detectors.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_ellipticity_05",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Ellipticity 5% across all detectors.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_e1_x_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF e1 X Gradient calculated as Z2,e1 in OCS in 1/deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_e1_y_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF e1 Y Gradient calculated as Z3,e1 in OCS in 1/deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_e1_radial_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF e1 radial gradient, calculated as Z4,e1 in 1/deg2.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_e2_x_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF e2 X Gradient calculated as Z2,e2 in OCS in 1/deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_e2_y_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF e2 Y Gradient calculated as Z3,e2 in OCS in 1/deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "psf_e2_radial_gradient",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF e2 radial gradient, calculated as Z4,e2 in 1/deg2.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z4_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic defocus (Z4) in OCS, mean across four corners in microns.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z11_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic primary spherical (Z11) in OCS, mean across four corners in microns.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z22_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic secondary spherical (Z22) in OCS, mean across four corners in microns.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_8_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic double zernike k=2, j=8 in OCS.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_7_intrinsic",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Intrinsic double zernike k=3, j=7 in OCS.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_4",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=4 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_5",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=5 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_6",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=6 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_7",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=7 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_8",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=8 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_9",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=9 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_10",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=10 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_11",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=11 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_12",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=12 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_13",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=13 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_14",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=14 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_15",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=15 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_16",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=16 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_17",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=17 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_18",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=18 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_19",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=19 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_20",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=20 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_21",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=21 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_22",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=22 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_23",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=23 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_24",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=24 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_25",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=25 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_26",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=26 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_27",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=27 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z2_28",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=2, j=28 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_4",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=4 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_5",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=5 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_6",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=6 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_7",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=7 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_8",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=8 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_9",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=9 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_10",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=10 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_11",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=11 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_12",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=12 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_13",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=13 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_14",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=14 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_15",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=15 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_16",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=16 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_17",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=17 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_18",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=18 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_19",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=19 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_20",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=20 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_21",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=21 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_22",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=22 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_23",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=23 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_24",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=24 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_25",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=25 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_26",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=26 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_27",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=27 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "z3_28",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Double zernike k=3, j=28 in OCS in microns for field radius 1.75 deg.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "guider_l0",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Outer scale L0 in meters calculated by the guider.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "shapelet_score_median",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Median shapelet score across the FOV.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "shapelet_score_max",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Maximum shapelet score across the FOV.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "shapelet_score_min",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Minimum shapelet score across the FOV.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "visit1_quicklook",
        sa.Column(
            "last_correction_visit_id",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Visit ID from which the last applied AOS corrections were calculated.",
        ),
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z4",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total defocus (Z4) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated defocus (Z4), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z5",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique primary astigmatism (Z5) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated oblique primary astigmatism (Z5), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z6",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical primary astigmatism (Z6) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical primary astigmatism (Z6), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z7",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical primary coma (Z7) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical primary coma (Z7), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z8",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total horizontal primary coma (Z8) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated horizontal primary coma (Z8), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z9",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical trefoil (Z9) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical trefoil (Z9), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z10",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique trefoil (Z10) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated horizontal trefoil (Z10), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z11",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total primary spherical (Z11) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated primary spherical (Z11), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z12",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary astigmatism (Z12) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical secondary astigmatism (Z12), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z13",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique secondary astigmatism (Z13) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated oblique secondary astigmatism (Z13), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z14",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical quadrafoil (Z14) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical quadrafoil (Z14), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z15",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique quadrafoil (Z15) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated horizontal quadrafoil (Z15), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z16",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total horizontal secondary coma (Z16) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated horizontal secondary coma (Z16), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z17",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary coma (Z17) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical secondary coma (Z17), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z18",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique secondary trefoil (Z18) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated oblique secondary trefoil (Z18), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z19",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary trefoil (Z19) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical secondary trefoil (Z19), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z20",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique pentafoil (Z20) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated oblique pentafoil (Z20), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z21",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical pentafoil (Z21) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical pentafoil (Z21), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z22",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total secondary spherical (Z22) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated secondary spherical (Z22), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z23",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total tertiary astigmatism (Z23) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated tertiary astimgatism (Z23), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z24",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total tertiary astigmatism (Z24) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated tertiary astimgatism (Z24), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z25",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total oblique secondary quadrafoil (Z25) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated oblique secondary quadrafoil (Z25), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z26",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total vertical secondary quadrafoil (Z26) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated vertical secondary quadrafoil (Z26), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z27",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total hexafoil (Z27) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated hexafoil (Z27), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z28",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated total hexafoil (Z28) in OCS, mean estimated across four corners in microns.",
        existing_comment="Estimated hexafoil (Z28), mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )


def downgrade() -> None:
    op.alter_column(
        "visit1_quicklook",
        "z28",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated hexafoil (Z28), mean estimated across four corners in microns.",
        existing_comment="Estimated total hexafoil (Z28) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z27",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated hexafoil (Z27), mean estimated across four corners in microns.",
        existing_comment="Estimated total hexafoil (Z27) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z26",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary quadrafoil (Z26), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical secondary quadrafoil (Z26) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z25",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique secondary quadrafoil (Z25), mean estimated across four corners in microns.",
        existing_comment="Estimated total oblique secondary quadrafoil (Z25) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z24",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated tertiary astimgatism (Z24), mean estimated across four corners in microns.",
        existing_comment="Estimated total tertiary astigmatism (Z24) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z23",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated tertiary astimgatism (Z23), mean estimated across four corners in microns.",
        existing_comment="Estimated total tertiary astigmatism (Z23) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z22",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated secondary spherical (Z22), mean estimated across four corners in microns.",
        existing_comment="Estimated total secondary spherical (Z22) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z21",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical pentafoil (Z21), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical pentafoil (Z21) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z20",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique pentafoil (Z20), mean estimated across four corners in microns.",
        existing_comment="Estimated total oblique pentafoil (Z20) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z19",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary trefoil (Z19), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical secondary trefoil (Z19) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z18",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique secondary trefoil (Z18), mean estimated across four corners in microns.",
        existing_comment="Estimated total oblique secondary trefoil (Z18) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z17",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary coma (Z17), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical secondary coma (Z17) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z16",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal secondary coma (Z16), mean estimated across four corners in microns.",
        existing_comment="Estimated total horizontal secondary coma (Z16) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z15",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal quadrafoil (Z15), mean estimated across four corners in microns.",
        existing_comment="Estimated total oblique quadrafoil (Z15) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z14",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical quadrafoil (Z14), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical quadrafoil (Z14) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z13",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique secondary astigmatism (Z13), mean estimated across four corners in microns.",
        existing_comment="Estimated total oblique secondary astigmatism (Z13) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z12",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary astigmatism (Z12), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical secondary astigmatism (Z12) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z11",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated primary spherical (Z11), mean estimated across four corners in microns.",
        existing_comment="Estimated total primary spherical (Z11) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z10",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal trefoil (Z10), mean estimated across four corners in microns.",
        existing_comment="Estimated total oblique trefoil (Z10) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z9",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical trefoil (Z9), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical trefoil (Z9) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z8",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal primary coma (Z8), mean estimated across four corners in microns.",
        existing_comment="Estimated total horizontal primary coma (Z8) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z7",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical primary coma (Z7), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical primary coma (Z7) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z6",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical primary astigmatism (Z6), mean estimated across four corners in microns.",
        existing_comment="Estimated total vertical primary astigmatism (Z6) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z5",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique primary astigmatism (Z5), mean estimated across four corners in microns.",
        existing_comment="Estimated total oblique primary astigmatism (Z5) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "visit1_quicklook",
        "z4",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated defocus (Z4), mean estimated across four corners in microns.",
        existing_comment="Estimated total defocus (Z4) in OCS, mean estimated across four corners in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.drop_column("visit1_quicklook", "last_correction_visit_id", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "shapelet_score_min", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "shapelet_score_max", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "shapelet_score_median", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "guider_l0", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_28", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_27", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_26", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_25", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_24", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_23", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_22", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_21", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_20", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_19", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_18", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_17", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_16", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_15", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_14", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_13", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_12", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_11", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_10", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_9", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_8", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_7", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_6", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_5", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_4", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_28", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_27", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_26", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_25", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_24", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_23", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_22", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_21", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_20", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_19", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_18", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_17", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_16", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_15", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_14", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_13", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_12", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_11", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_10", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_9", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_8", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_7", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_6", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_5", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_4", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z3_7_intrinsic", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z2_8_intrinsic", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z22_intrinsic", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z11_intrinsic", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "z4_intrinsic", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_e2_radial_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_e2_y_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_e2_x_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_e1_radial_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_e1_y_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_e1_x_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_ellipticity_05", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_ellipticity_95", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_ellipticity_median", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_fwhm_radial_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_fwhm_y_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_fwhm_x_gradient", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_sigma_05", schema="cdb_lsstcam")
    op.drop_column("visit1_quicklook", "psf_sigma_95", schema="cdb_lsstcam")
    op.drop_column("exposure_quicklook", "mtaos_package_versions", schema="cdb_lsstcam")
    op.drop_column("exposure_quicklook", "ra_package_versions", schema="cdb_lsstcam")
    op.alter_column(
        "ccdvisit1_quicklook",
        "z28",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated hexafoil (Z28), in microns.",
        existing_comment="Estimated total hexafoil (Z28) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z27",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated hexafoil (Z27), in microns.",
        existing_comment="Estimated total hexafoil (Z27) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z26",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary quadrafoil (Z26), in microns.",
        existing_comment="Estimated total vertical secondary quadrafoil (Z26) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z25",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique secondary quadrafoil (Z25), in microns.",
        existing_comment="Estimated total oblique secondary quadrafoil (Z25) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z24",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated tertiary astimgatism (Z24), in microns.",
        existing_comment="Estimated total tertiary astigmatism (Z24) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z23",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated tertiary astimgatism (Z23), in microns.",
        existing_comment="Estimated total tertiary astigmatism (Z23) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z22",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated secondary spherical (Z22), in microns.",
        existing_comment="Estimated total secondary spherical (Z22) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z21",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical pentafoil (Z21), in microns.",
        existing_comment="Estimated total vertical pentafoil (Z21) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z20",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique pentafoil (Z20), in microns.",
        existing_comment="Estimated total oblique pentafoil (Z20) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z19",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary trefoil (Z19), in microns.",
        existing_comment="Estimated total vertical secondary trefoil (Z19) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z18",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique secondary trefoil (Z18), in microns.",
        existing_comment="Estimated total oblique secondary trefoil (Z18) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z17",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary coma (Z17), in microns.",
        existing_comment="Estimated total vertical secondary coma (Z17) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z16",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal secondary coma (Z16), in microns.",
        existing_comment="Estimated total horizontal secondary coma (Z16) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z15",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal quadrafoil (Z15), in microns.",
        existing_comment="Estimated total oblique quadrafoil (Z15) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z14",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical quadrafoil (Z14), in microns.",
        existing_comment="Estimated total vertical quadrafoil (Z14) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z13",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique secondary astigmatism (Z13), in microns.",
        existing_comment="Estimated total oblique secondary astigmatism (Z13) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z12",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical secondary astigmatism (Z12), in microns.",
        existing_comment="Estimated total vertical secondary astigmatism (Z12) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z11",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated primary spherical (Z11), in microns.",
        existing_comment="Estimated total primary spherical (Z11) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z10",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal trefoil (Z10), in microns.",
        existing_comment="Estimated total oblique trefoil (Z10) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z9",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical trefoil (Z9), in microns.",
        existing_comment="Estimated total vertical trefoil (Z9) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z8",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated horizontal primary coma (Z8), in microns.",
        existing_comment="Estimated total horizontal primary coma (Z8) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z7",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical primary coma (Z7), in microns.",
        existing_comment="Estimated total vertical primary coma (Z7) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z6",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated vertical primary astigmatism (Z6), in microns.",
        existing_comment="Estimated total vertical primary astigmatism (Z6) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z5",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated oblique primary astigmatism (Z5), in microns.",
        existing_comment="Estimated total oblique primary astigmatism (Z5) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "z4",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Estimated defocus (Z4), in microns.",
        existing_comment="Estimated total defocus (Z4) in OCS, in microns.",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.drop_column("ccdvisit1_quicklook", "z22_intrinsic", schema="cdb_lsstcam")
    op.drop_column("ccdvisit1_quicklook", "z11_intrinsic", schema="cdb_lsstcam")
    op.drop_column("ccdvisit1_quicklook", "z4_intrinsic", schema="cdb_lsstcam")
