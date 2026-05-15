"""shorten constraint names

Revision ID: 8bc38ee0dadf
Revises: 50a15426960f
Create Date: 2026-05-14 23:22:35.088702+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8bc38ee0dadf"
down_revision: Union[str, None] = "50a15426960f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure"
        " RENAME CONSTRAINT un_ccdexposure_ccdexposure_id_day_obs_seq_num_detector"
        " TO un_ccdexposure_ccdexposure_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure"
        " RENAME CONSTRAINT un_exposure_day_obs_seq_num"
        " TO un_exposure_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure"
        " RENAME CONSTRAINT un_exposure_exposure_id_day_obs_seq_num"
        " TO un_exposure_exposure_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_flexdata"
        " RENAME CONSTRAINT un_exposure_flexdata_day_obs_seq_num_key"
        " TO un_exposure_flexdata_ds_key"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_day_obs_seq_num"
        " TO fk_ccdexposure_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_exposure_id_day_obs_seq_num"
        " TO fk_ccdexposure_exposure_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_day_obs_seq_num_detector"
        " TO fk_ccdexposure_camera_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_ccdexposure_id_day_obs_seq_num_detector"
        " TO fk_ccdexposure_camera_ccdexposure_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_day_obs_seq_num_detector"
        " TO fk_ccdexposure_flexdata_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_obs_id_day_obs_seq_num_detector"
        " TO fk_ccdexposure_flexdata_obs_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_quicklook"
        " RENAME CONSTRAINT fk_ccdexposure_quicklook_day_obs_seq_num_detector"
        " TO fk_ccdexposure_quicklook_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_day_obs_seq_num_detector"
        " TO fk_ccdvisit1_quicklook_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_ccdvisit_id_day_obs_seq_num_detector"
        " TO fk_ccdvisit1_quicklook_ccdvisit_id_dsd"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_day_obs_seq_num"
        " TO fk_exposure_flexdata_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_obs_id_day_obs_seq_num"
        " TO fk_exposure_flexdata_obs_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_day_obs_seq_num"
        " TO fk_exposure_quicklook_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_exposure_id_day_obs_seq_num"
        " TO fk_exposure_quicklook_exposure_id_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.visit1_quicklook"
        " RENAME CONSTRAINT fk_visit1_quicklook_day_obs_seq_num"
        " TO fk_visit1_quicklook_ds"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.visit1_quicklook"
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
        schema="cdb_lsstcomcam",
    )


def downgrade() -> None:
    op.alter_column(
        "exposure",
        "dimm_seeing",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Atmospheric seeing as measured by external DIMM (FWHM).",
        existing_comment="Seeing as measured by external DIMM (FWHM).",
        existing_nullable=True,
        schema="cdb_lsstcomcam",
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.visit1_quicklook"
        " RENAME CONSTRAINT fk_visit1_quicklook_visit_id_ds"
        " TO fk_visit1_quicklook_visit_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.visit1_quicklook"
        " RENAME CONSTRAINT fk_visit1_quicklook_ds"
        " TO fk_visit1_quicklook_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_exposure_id_ds"
        " TO fk_exposure_quicklook_exposure_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_quicklook"
        " RENAME CONSTRAINT fk_exposure_quicklook_ds"
        " TO fk_exposure_quicklook_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_obs_id_ds"
        " TO fk_exposure_flexdata_obs_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_flexdata"
        " RENAME CONSTRAINT fk_exposure_flexdata_ds"
        " TO fk_exposure_flexdata_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_ccdvisit_id_dsd"
        " TO fk_ccdvisit1_quicklook_ccdvisit_id_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdvisit1_quicklook"
        " RENAME CONSTRAINT fk_ccdvisit1_quicklook_dsd"
        " TO fk_ccdvisit1_quicklook_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_quicklook"
        " RENAME CONSTRAINT fk_ccdexposure_quicklook_dsd"
        " TO fk_ccdexposure_quicklook_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_obs_id_dsd"
        " TO fk_ccdexposure_flexdata_obs_id_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_flexdata"
        " RENAME CONSTRAINT fk_ccdexposure_flexdata_dsd"
        " TO fk_ccdexposure_flexdata_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_ccdexposure_id_dsd"
        " TO fk_ccdexposure_camera_ccdexposure_id_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure_camera"
        " RENAME CONSTRAINT fk_ccdexposure_camera_dsd"
        " TO fk_ccdexposure_camera_day_obs_seq_num_detector"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_exposure_id_ds"
        " TO fk_ccdexposure_exposure_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure"
        " RENAME CONSTRAINT fk_ccdexposure_ds"
        " TO fk_ccdexposure_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure_flexdata"
        " RENAME CONSTRAINT un_exposure_flexdata_ds_key"
        " TO un_exposure_flexdata_day_obs_seq_num_key"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure"
        " RENAME CONSTRAINT un_exposure_exposure_id_ds"
        " TO un_exposure_exposure_id_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.exposure"
        " RENAME CONSTRAINT un_exposure_ds"
        " TO un_exposure_day_obs_seq_num"
    )
    op.execute(
        "ALTER TABLE cdb_lsstcomcam.ccdexposure"
        " RENAME CONSTRAINT un_ccdexposure_ccdexposure_id_dsd"
        " TO un_ccdexposure_ccdexposure_id_day_obs_seq_num_detector"
    )
