"""shorten constraint names

Revision ID: 18c147c52a26
Revises: 08383dba5e85
Create Date: 2026-05-14 23:22:47.950723+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "18c147c52a26"
down_revision: Union[str, None] = "08383dba5e85"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure"
        " RENAME CONSTRAINT un_ccdexposure_ccdexposure_id_day_obs_seq_num_detector"
        " TO un_ccdexposure_ccdexposure_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure"
        " RENAME CONSTRAINT un_exposure_day_obs_seq_num"
        " TO un_exposure_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure"
        " RENAME CONSTRAINT un_exposure_exposure_id_day_obs_seq_num"
        " TO un_exposure_exposure_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_flexdata"
        " RENAME CONSTRAINT un_exposure_flexdata_day_obs_seq_num_key"
        " TO un_exposure_flexdata_ds_key"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_day_obs_seq_num"
        " TO fk_ccdexposure_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_exposure_id_day_obs_seq_num"
        " TO fk_ccdexposure_exposure_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_day_obs_seq_num_detector"
        " TO fk_ccdexposure_camera_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_ccdexposure_id_day_obs_seq_num_detector"
        " TO fk_ccdexposure_camera_ccdexposure_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_day_obs_seq_num_detector"
        " TO fk_ccdexposure_flexdata_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_obs_id_day_obs_seq_num_detector"
        " TO fk_ccdexposure_flexdata_obs_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_quicklook"
        " RENAME CONSTRAINT fk_ccdexposure_quicklook_day_obs_seq_num_detector"
        " TO fk_ccdexposure_quicklook_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_day_obs_seq_num_detector"
        " TO fk_ccdvisit1_quicklook_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_ccdvisit_id_day_obs_seq_num_detector"
        " TO fk_ccdvisit1_quicklook_ccdvisit_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_day_obs_seq_num"
        " TO fk_exposure_flexdata_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_obs_id_day_obs_seq_num"
        " TO fk_exposure_flexdata_obs_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_day_obs_seq_num"
        " TO fk_exposure_quicklook_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_exposure_id_day_obs_seq_num"
        " TO fk_exposure_quicklook_exposure_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.visit1_quicklook"
        " RENAME CONSTRAINT fk_visit1_quicklook_day_obs_seq_num"
        " TO fk_visit1_quicklook_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.visit1_quicklook"
        " RENAME CONSTRAINT fk_visit1_quicklook_visit_id_day_obs_seq_num"
        " TO fk_visit1_quicklook_visit_id_ds"
    )
    op.alter_column(
        "exposure",
        "dimm_seeing",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Seeing as measured by external DIMM (FWHM).",
        existing_comment="Atmospheric seeing as measured by external DIMM (FWHM).",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )


def downgrade() -> None:
    op.alter_column(
        "exposure",
        "dimm_seeing",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Atmospheric seeing as measured by external DIMM (FWHM).",
        existing_comment="Seeing as measured by external DIMM (FWHM).",
        existing_nullable=True,
        schema="cdb_lsstcam",
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.visit1_quicklook"
        " RENAME CONSTRAINT fk_visit1_quicklook_visit_id_ds"
        " TO fk_visit1_quicklook_visit_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.visit1_quicklook"
        " RENAME CONSTRAINT fk_visit1_quicklook_ds"
        " TO fk_visit1_quicklook_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_exposure_id_ds"
        " TO fk_exposure_quicklook_exposure_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_ds"
        " TO fk_exposure_quicklook_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_obs_id_ds"
        " TO fk_exposure_flexdata_obs_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_ds"
        " TO fk_exposure_flexdata_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_ccdvisit_id_dsd"
        " TO fk_ccdvisit1_quicklook_ccdvisit_id_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_dsd"
        " TO fk_ccdvisit1_quicklook_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_quicklook"
        " RENAME CONSTRAINT fk_ccdexposure_quicklook_dsd"
        " TO fk_ccdexposure_quicklook_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_obs_id_dsd"
        " TO fk_ccdexposure_flexdata_obs_id_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_dsd"
        " TO fk_ccdexposure_flexdata_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_ccdexposure_id_dsd"
        " TO fk_ccdexposure_camera_ccdexposure_id_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_dsd"
        " TO fk_ccdexposure_camera_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_exposure_id_ds"
        " TO fk_ccdexposure_exposure_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_ds"
        " TO fk_ccdexposure_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure_flexdata"
        " RENAME CONSTRAINT un_exposure_flexdata_ds_key"
        " TO un_exposure_flexdata_day_obs_seq_num_key"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure"
        " RENAME CONSTRAINT un_exposure_exposure_id_ds"
        " TO un_exposure_exposure_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.exposure"
        " RENAME CONSTRAINT un_exposure_ds"
        " TO un_exposure_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcam.ccdexposure"
        " RENAME CONSTRAINT un_ccdexposure_ccdexposure_id_dsd"
        " TO un_ccdexposure_ccdexposure_id_day_obs_seq_num_detector"
    )
