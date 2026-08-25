"""Restore single-column ID indexes dropped by multi-column primary keys

Revision ID: 6ce813602e40
Revises: 8bc38ee0dadf
Create Date: 2026-08-14 19:47:46.851800+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6ce813602e40"
down_revision: str | None = "8bc38ee0dadf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "idx_ccdexposure_camera_ccdexposure_id",
        "ccdexposure_camera",
        ["ccdexposure_id"],
        unique=False,
        schema="cdb_lsstcomcam",
    )
    op.create_index(
        "idx_ccdexposure_flexdata_obs_id_key",
        "ccdexposure_flexdata",
        ["obs_id", "key"],
        unique=False,
        schema="cdb_lsstcomcam",
    )
    op.create_index(
        "idx_ccdexposure_quicklook_ccdexposure_id",
        "ccdexposure_quicklook",
        ["ccdexposure_id"],
        unique=False,
        schema="cdb_lsstcomcam",
    )
    op.create_index(
        "idx_ccdvisit1_quicklook_ccdvisit_id",
        "ccdvisit1_quicklook",
        ["ccdvisit_id"],
        unique=False,
        schema="cdb_lsstcomcam",
    )


def downgrade() -> None:
    op.drop_index(
        "idx_ccdvisit1_quicklook_ccdvisit_id", table_name="ccdvisit1_quicklook", schema="cdb_lsstcomcam"
    )
    op.drop_index(
        "idx_ccdexposure_quicklook_ccdexposure_id",
        table_name="ccdexposure_quicklook",
        schema="cdb_lsstcomcam",
    )
    op.drop_index(
        "idx_ccdexposure_flexdata_obs_id_key", table_name="ccdexposure_flexdata", schema="cdb_lsstcomcam"
    )
    op.drop_index(
        "idx_ccdexposure_camera_ccdexposure_id", table_name="ccdexposure_camera", schema="cdb_lsstcomcam"
    )
