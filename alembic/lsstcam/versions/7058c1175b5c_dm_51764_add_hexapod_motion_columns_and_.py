"""DM-51764 Add hexapod motion columns and fix missing column

Revision ID: 7058c1175b5c
Revises: ab5ec8a5f784
Create Date: 2025-07-23 19:42:56.815376+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "7058c1175b5c"
down_revision: str | None = "ab5ec8a5f784"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "exposure_quicklook",
        sa.Column(
            "mount_motion_image_degradation_el",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Image degradation due to mount motion in elevation.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "exposure_quicklook",
        sa.Column(
            "mount_jitter_rms_cam_hexapod",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="The RMS image motion due to movement of the camera hexapod.",
        ),
        schema="cdb_lsstcam",
    )
    op.add_column(
        "exposure_quicklook",
        sa.Column(
            "mount_jitter_rms_m2_hexapod",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="The RMS image motion due to movement of the M2 hexapod.",
        ),
        schema="cdb_lsstcam",
    )


def downgrade() -> None:
    op.drop_column("exposure_quicklook", "mount_jitter_rms_m2_hexapod", schema="cdb_lsstcam")
    op.drop_column("exposure_quicklook", "mount_jitter_rms_cam_hexapod", schema="cdb_lsstcam")
    op.drop_column("exposure_quicklook", "mount_motion_image_degradation_el", schema="cdb_lsstcam")
