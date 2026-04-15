"""Prepend psf_ in the higher moment PSF shape information

Revision ID: e9de48cfb6fc
Revises: 95626bd65229
Create Date: 2026-04-15 14:43:30.882317+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "e9de48cfb6fc"
down_revision: Union[str, None] = "95626bd65229"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    existing_type = sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql")

    op.alter_column(
        "ccdvisit1_quicklook",
        "coma_1",
        new_column_name="psf_coma_1",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="Coma-like higher-order moment combination, M30 + M12.",
        comment="PSF coma-like higher-order moment combination, M30 + M12.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "coma_2",
        new_column_name="psf_coma_2",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="Coma-like higher-order moment combination, M21 + M03.",
        comment="PSF coma-like higher-order moment combination, M21 + M03.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "trefoil_1",
        new_column_name="psf_trefoil_1",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="Trefoil-like higher-order moment combination, M30 - 3*M12.",
        comment="PSF trefoil-like higher-order moment combination, M30 - 3*M12.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "trefoil_2",
        new_column_name="psf_trefoil_2",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="Trefoil-like higher-order moment combination, 3*M21 - M03.",
        comment="PSF trefoil-like higher-order moment combination, 3*M21 - M03.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "kurtosis",
        new_column_name="psf_kurtosis",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="Kurtosis-like higher-order moment combination, M40 + 2*M22 + M04.",
        comment="PSF kurtosis-like higher-order moment combination, M40 + 2*M22 + M04.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "e4_1",
        new_column_name="psf_e4_1",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="Fourth-order ellipticity-like higher-order moment combination, M40 - M04.",
        comment="PSF fourth-order ellipticity-like higher-order moment combination, M40 - M04.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "e4_2",
        new_column_name="psf_e4_2",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="Fourth-order ellipticity-like higher-order moment combination, 2*(M31 + M13).",
        comment="PSF fourth-order ellipticity-like higher-order moment combination, 2*(M31 + M13).",
        schema="cdb_lsstcam",
    )


def downgrade() -> None:
    existing_type = sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql")

    op.alter_column(
        "ccdvisit1_quicklook",
        "psf_coma_1",
        new_column_name="coma_1",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="PSF coma-like higher-order moment combination, M30 + M12.",
        comment="Coma-like higher-order moment combination, M30 + M12.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "psf_coma_2",
        new_column_name="coma_2",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="PSF coma-like higher-order moment combination, M21 + M03.",
        comment="Coma-like higher-order moment combination, M21 + M03.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "psf_trefoil_1",
        new_column_name="trefoil_1",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="PSF trefoil-like higher-order moment combination, M30 - 3*M12.",
        comment="Trefoil-like higher-order moment combination, M30 - 3*M12.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "psf_trefoil_2",
        new_column_name="trefoil_2",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="PSF trefoil-like higher-order moment combination, 3*M21 - M03.",
        comment="Trefoil-like higher-order moment combination, 3*M21 - M03.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "psf_kurtosis",
        new_column_name="kurtosis",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="PSF kurtosis-like higher-order moment combination, M40 + 2*M22 + M04.",
        comment="Kurtosis-like higher-order moment combination, M40 + 2*M22 + M04.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "psf_e4_1",
        new_column_name="e4_1",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="PSF fourth-order ellipticity-like higher-order moment combination, M40 - M04.",
        comment="Fourth-order ellipticity-like higher-order moment combination, M40 - M04.",
        schema="cdb_lsstcam",
    )
    op.alter_column(
        "ccdvisit1_quicklook",
        "psf_e4_2",
        new_column_name="e4_2",
        existing_type=existing_type,
        existing_nullable=True,
        existing_comment="PSF fourth-order ellipticity-like higher-order moment combination, 2*(M31 + M13).",
        comment="Fourth-order ellipticity-like higher-order moment combination, 2*(M31 + M13).",
        schema="cdb_lsstcam",
    )
