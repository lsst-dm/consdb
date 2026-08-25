"""Add foreign keys and unique constraint for exposure.exposure_id

Revision ID: 0490d793fc1a
Revises: 67319407b5fc
Create Date: 2024-09-25 21:37:22.445341+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0490d793fc1a"
down_revision: str | None = "67319407b5fc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "un_ccdexposure_exposure_id_detector",
        "ccdexposure",
        ["exposure_id", "detector"],
        schema="cdb_lsstcomcam",
    )
    op.create_foreign_key(
        "fk_ccdexposure_exposure_id",
        "ccdexposure",
        "exposure",
        ["exposure_id"],
        ["exposure_id"],
        source_schema="cdb_lsstcomcam",
        referent_schema="cdb_lsstcomcam",
    )
    op.create_foreign_key(
        "fk_exposure_flexdata_obs_id",
        "exposure_flexdata",
        "exposure",
        ["obs_id"],
        ["exposure_id"],
        source_schema="cdb_lsstcomcam",
        referent_schema="cdb_lsstcomcam",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_exposure_flexdata_obs_id", "exposure_flexdata", schema="cdb_lsstcomcam", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_ccdexposure_exposure_id", "ccdexposure", schema="cdb_lsstcomcam", type_="foreignkey"
    )
    op.drop_constraint(
        "un_ccdexposure_exposure_id_detector", "ccdexposure", schema="cdb_lsstcomcam", type_="unique"
    )
