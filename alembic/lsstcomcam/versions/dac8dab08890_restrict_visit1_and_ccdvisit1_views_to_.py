"""Restrict visit1 and ccdvisit1 views to can_see_sky

Revision ID: dac8dab08890
Revises: 6ce813602e40
Create Date: 2026-09-30 20:00:53.330503+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dac8dab08890"
down_revision: str | None = "6ce813602e40"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("DROP VIEW IF EXISTS cdb_lsstcomcam.ccdvisit1")
    op.execute("DROP VIEW IF EXISTS cdb_lsstcomcam.visit1")
    op.execute(
        """
        CREATE OR REPLACE VIEW cdb_lsstcomcam.visit1 AS
        SELECT
            exposure_id AS visit_id,
            exposure_name,
            controller,
            day_obs,
            seq_num,
            physical_filter,
            band,
            s_ra,
            s_dec,
            sky_rotation,
            azimuth_start,
            azimuth_end,
            azimuth,
            altitude_start,
            altitude_end,
            altitude,
            zenith_distance_start,
            zenith_distance_end,
            zenith_distance,
            airmass,
            exp_midpt,
            exp_midpt_mjd,
            obs_start,
            obs_start_mjd,
            obs_end,
            obs_end_mjd,
            exp_time,
            shut_time,
            dark_time,
            group_id,
            cur_index,
            max_index,
            img_type,
            emulated,
            science_program,
            observation_reason,
            target_name,
            air_temp,
            pressure,
            humidity,
            wind_speed,
            wind_dir,
            dimm_seeing,
            focus_z,
            simulated,
            vignette,
            vignette_min,
            scheduler_note,
            s_region,
            can_see_sky,
            pgs_region
        FROM cdb_lsstcomcam.exposure
        WHERE exposure.can_see_sky IS TRUE;
        """
    )
    op.execute("GRANT SELECT ON cdb_lsstcomcam.visit1 TO usdf;")
    op.execute("GRANT SELECT ON cdb_lsstcomcam.visit1 TO oods;")
    op.execute(
        """
        CREATE OR REPLACE VIEW cdb_lsstcomcam.ccdvisit1 AS
        SELECT
            ccdexposure.ccdexposure_id AS ccdvisit_id,
            ccdexposure.exposure_id AS visit_id,
            ccdexposure.day_obs,
            ccdexposure.seq_num,
            ccdexposure.detector,
            ccdexposure.s_region,
            ccdexposure.pgs_region
        FROM cdb_lsstcomcam.ccdexposure
            JOIN cdb_lsstcomcam.exposure ON ccdexposure.exposure_id = exposure.exposure_id
        WHERE exposure.can_see_sky IS TRUE;
        """
    )
    op.execute("GRANT SELECT ON cdb_lsstcomcam.ccdvisit1 TO usdf;")
    op.execute("GRANT SELECT ON cdb_lsstcomcam.ccdvisit1 TO oods;")


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS cdb_lsstcomcam.ccdvisit1")
    op.execute("DROP VIEW IF EXISTS cdb_lsstcomcam.visit1")
    op.execute(
        """
        CREATE VIEW cdb_lsstcomcam.ccdvisit1 AS
        SELECT *
        FROM cdb_lsstcomcam.ccdexposure
        """
    )
    op.execute(
        """
        CREATE VIEW cdb_lsstcomcam.visit1 AS
        SELECT *
        FROM cdb_lsstcomcam.exposure
        """
    )
    op.execute("ALTER TABLE cdb_lsstcomcam.ccdvisit1 RENAME COLUMN ccdexposure_id TO ccdvisit_id")
    op.execute("ALTER TABLE cdb_lsstcomcam.ccdvisit1 RENAME COLUMN exposure_id TO visit_id")
    op.execute("ALTER TABLE cdb_lsstcomcam.visit1 RENAME COLUMN exposure_id TO visit_id")
    op.execute("GRANT SELECT ON cdb_lsstcomcam.ccdvisit1 TO usdf")
    op.execute("GRANT SELECT ON cdb_lsstcomcam.ccdvisit1 TO oods")
    op.execute("GRANT SELECT ON cdb_lsstcomcam.visit1 TO usdf")
    op.execute("GRANT SELECT ON cdb_lsstcomcam.visit1 TO oods")
