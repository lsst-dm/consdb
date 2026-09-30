"""Restrict visit1 and ccdvisit1 views to can_see_sky

Revision ID: 16d80bcf2807
Revises: e9de48cfb6fc
Create Date: 2026-09-30 20:01:00.679170+00:00

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16d80bcf2807"
down_revision: str | None = "e9de48cfb6fc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("DROP VIEW IF EXISTS cdb_lsstcam.ccdvisit1")
    op.execute("DROP VIEW IF EXISTS cdb_lsstcam.visit1")
    op.execute(
        """
        CREATE OR REPLACE VIEW cdb_lsstcam.visit1 AS
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
        FROM cdb_lsstcam.exposure
        WHERE exposure.can_see_sky IS TRUE;
        """
    )
    op.execute("GRANT SELECT ON cdb_lsstcam.visit1 TO usdf;")
    op.execute("GRANT SELECT ON cdb_lsstcam.visit1 TO oods;")
    op.execute(
        """
        CREATE OR REPLACE VIEW cdb_lsstcam.ccdvisit1 AS
        SELECT
            ccdexposure.ccdexposure_id AS ccdvisit_id,
            ccdexposure.exposure_id AS visit_id,
            ccdexposure.day_obs,
            ccdexposure.seq_num,
            ccdexposure.detector,
            ccdexposure.s_region,
            ccdexposure.pgs_region
        FROM cdb_lsstcam.ccdexposure
            JOIN cdb_lsstcam.exposure ON ccdexposure.exposure_id = exposure.exposure_id
        WHERE exposure.can_see_sky IS TRUE;
        """
    )
    op.execute("GRANT SELECT ON cdb_lsstcam.ccdvisit1 TO usdf;")
    op.execute("GRANT SELECT ON cdb_lsstcam.ccdvisit1 TO oods;")


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS cdb_lsstcam.ccdvisit1")
    op.execute("DROP VIEW IF EXISTS cdb_lsstcam.visit1")
    op.execute(
        """
        CREATE VIEW cdb_lsstcam.ccdvisit1 AS
        SELECT *
        FROM cdb_lsstcam.ccdexposure
        """
    )
    op.execute(
        """
        CREATE VIEW cdb_lsstcam.visit1 AS
        SELECT *
        FROM cdb_lsstcam.exposure
        """
    )
    op.execute("ALTER TABLE cdb_lsstcam.ccdvisit1 RENAME COLUMN ccdexposure_id TO ccdvisit_id")
    op.execute("ALTER TABLE cdb_lsstcam.ccdvisit1 RENAME COLUMN exposure_id TO visit_id")
    op.execute("ALTER TABLE cdb_lsstcam.visit1 RENAME COLUMN exposure_id TO visit_id")
    op.execute("GRANT SELECT ON cdb_lsstcam.ccdvisit1 TO usdf")
    op.execute("GRANT SELECT ON cdb_lsstcam.ccdvisit1 TO oods")
    op.execute("GRANT SELECT ON cdb_lsstcam.visit1 TO usdf")
    op.execute("GRANT SELECT ON cdb_lsstcam.visit1 TO oods")
