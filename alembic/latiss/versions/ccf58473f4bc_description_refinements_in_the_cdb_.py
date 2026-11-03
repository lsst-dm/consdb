"""Description refinements in the CDB schemas.

Revision ID: ccf58473f4bc
Revises: 9e671b59d28f
Create Date: 2026-11-03 19:54:22.377682+00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ccf58473f4bc"
down_revision: str | None = "9e671b59d28f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "exposure",
        "s_ra",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; right ascension of focal plane center at the start of the exposure, derived from encoder readings and correcting for annual aberration, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_comment="Central Spatial Position in ICRS; right ascension of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "s_dec",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; declination of focal plane center at the start of the exposure, derived from encoder readings and correcting for annual aberration, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_comment="Central Spatial Position in ICRS; declination of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "sky_rotation",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Sky rotation angle at the start of the exposure, computed by the pointing component from the mount and rotator positions.",
        existing_comment="Targeted sky rotation angle.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "azimuth_start",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Azimuth axis position of the mount at the start of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_comment="Azimuth of focal plane center at the start of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "azimuth_end",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Azimuth axis position of the mount at the end of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_comment="Azimuth of focal plane center at the end of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "azimuth",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Azimuth of focal plane center at the middle of the exposure, computed from s_ra/s_dec at exp_midpt for the observatory location, without refraction. If s_ra/s_dec is unavailable, this is instead the average of the azimuth_start and azimuth_end mount positions.",
        existing_comment="Azimuth of focal plane center at the middle of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "altitude_start",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Elevation axis position of the mount at the start of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_comment="Altitude of focal plane center at the start of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "altitude_end",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Elevation axis position of the mount at the end of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_comment="Altitude of focal plane center at the end of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "altitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Altitude of focal plane center at the middle of the exposure, computed from s_ra/s_dec at exp_midpt for the observatory location, without refraction. If s_ra/s_dec is unavailable, this is instead the average of the altitude_start and altitude_end mount positions.",
        existing_comment="Altitude of focal plane center at the middle of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "zenith_distance_start",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="90 degrees minus altitude_start.",
        existing_comment="Zenith distance at the start of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "zenith_distance_end",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="90 degrees minus altitude_end.",
        existing_comment="Zenith distance at the end of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "zenith_distance",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Zenith distance at the middle of the exposure, computed from s_ra/s_dec at exp_midpt for the observatory location, without refraction. If s_ra/s_dec is unavailable, this is instead the average of the zenith_distance_start and zenith_distance_end mount positions.",
        existing_comment="Zenith distance at the middle of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "airmass",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Airmass of the target at the start of the exposure, as computed by the telescope pointing component.",
        existing_comment="Airmass of the observed line of sight at the middle of the exposure.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "exp_midpt",
        existing_type=postgresql.TIMESTAMP(),
        comment="Midpoint between obs_start and obs_end, TAI. Not corrected for shutter motion.",
        existing_comment="Midpoint time for exposure at the fiducial center of the focal plane. array. TAI, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "exp_midpt_mjd",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Midpoint between obs_start and obs_end, in MJD, TAI. Not corrected for shutter motion.",
        existing_comment="Midpoint time for exposure at the fiducial center of the focal plane. array in MJD. TAI, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_start",
        existing_type=postgresql.TIMESTAMP(),
        comment="Start of CCD integration (end of the last clear), TAI. Precedes the opening of the shutter.",
        existing_comment="Start time of the exposure at the fiducial center of the focal plane. array, TAI, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_start_mjd",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Start of CCD integration (end of the last clear), in MJD, TAI. Precedes the opening of the shutter.",
        existing_comment="Start of the exposure in MJD, TAI, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_end",
        existing_type=postgresql.TIMESTAMP(),
        comment="Start of CCD readout, TAI. Follows the closing of the shutter.",
        existing_comment="End time of the exposure at the fiducial center of the focal plane. array, TAI, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_end_mjd",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Start of CCD readout, in MJD, TAI. Follows the closing of the shutter.",
        existing_comment="End of the exposure in MJD, TAI, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "exp_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Requested exposure time.",
        existing_comment="Spatially-averaged duration of exposure, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "shut_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Shutter-open duration. Equal to exp_time.",
        existing_comment="Spatially-averaged shutter-open duration, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "dark_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Duration from last clear to readout.",
        existing_comment="Duration from last clear to readout, accurate to 10ms.",
        existing_nullable=True,
        schema="cdb_latiss",
    )


def downgrade() -> None:
    op.alter_column(
        "exposure",
        "dark_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Duration from last clear to readout, accurate to 10ms.",
        existing_comment="Duration from last clear to readout.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "shut_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Spatially-averaged shutter-open duration, accurate to 10ms.",
        existing_comment="Shutter-open duration. Equal to exp_time.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "exp_time",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Spatially-averaged duration of exposure, accurate to 10ms.",
        existing_comment="Requested exposure time.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_end_mjd",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="End of the exposure in MJD, TAI, accurate to 10ms.",
        existing_comment="Start of CCD readout, in MJD, TAI. Follows the closing of the shutter.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_end",
        existing_type=postgresql.TIMESTAMP(),
        comment="End time of the exposure at the fiducial center of the focal plane. array, TAI, accurate to 10ms.",
        existing_comment="Start of CCD readout, TAI. Follows the closing of the shutter.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_start_mjd",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Start of the exposure in MJD, TAI, accurate to 10ms.",
        existing_comment="Start of CCD integration (end of the last clear), in MJD, TAI. Precedes the opening of the shutter.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "obs_start",
        existing_type=postgresql.TIMESTAMP(),
        comment="Start time of the exposure at the fiducial center of the focal plane. array, TAI, accurate to 10ms.",
        existing_comment="Start of CCD integration (end of the last clear), TAI. Precedes the opening of the shutter.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "exp_midpt_mjd",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Midpoint time for exposure at the fiducial center of the focal plane. array in MJD. TAI, accurate to 10ms.",
        existing_comment="Midpoint between obs_start and obs_end, in MJD, TAI. Not corrected for shutter motion.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "exp_midpt",
        existing_type=postgresql.TIMESTAMP(),
        comment="Midpoint time for exposure at the fiducial center of the focal plane. array. TAI, accurate to 10ms.",
        existing_comment="Midpoint between obs_start and obs_end, TAI. Not corrected for shutter motion.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "airmass",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Airmass of the observed line of sight at the middle of the exposure.",
        existing_comment="Airmass of the target at the start of the exposure, as computed by the telescope pointing component.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "zenith_distance",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Zenith distance at the middle of the exposure.",
        existing_comment="Zenith distance at the middle of the exposure, computed from s_ra/s_dec at exp_midpt for the observatory location, without refraction. If s_ra/s_dec is unavailable, this is instead the average of the zenith_distance_start and zenith_distance_end mount positions.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "zenith_distance_end",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Zenith distance at the end of the exposure.",
        existing_comment="90 degrees minus altitude_end.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "zenith_distance_start",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Zenith distance at the start of the exposure.",
        existing_comment="90 degrees minus altitude_start.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "altitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Altitude of focal plane center at the middle of the exposure.",
        existing_comment="Altitude of focal plane center at the middle of the exposure, computed from s_ra/s_dec at exp_midpt for the observatory location, without refraction. If s_ra/s_dec is unavailable, this is instead the average of the altitude_start and altitude_end mount positions.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "altitude_end",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Altitude of focal plane center at the end of the exposure.",
        existing_comment="Elevation axis position of the mount at the end of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "altitude_start",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Altitude of focal plane center at the start of the exposure.",
        existing_comment="Elevation axis position of the mount at the start of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "azimuth",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Azimuth of focal plane center at the middle of the exposure.",
        existing_comment="Azimuth of focal plane center at the middle of the exposure, computed from s_ra/s_dec at exp_midpt for the observatory location, without refraction. If s_ra/s_dec is unavailable, this is instead the average of the azimuth_start and azimuth_end mount positions.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "azimuth_end",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Azimuth of focal plane center at the end of the exposure.",
        existing_comment="Azimuth axis position of the mount at the end of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "azimuth_start",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Azimuth of focal plane center at the start of the exposure.",
        existing_comment="Azimuth axis position of the mount at the start of the exposure, as reported by the mount control system. Raw axis reading, not corrected for the pointing model.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "sky_rotation",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Targeted sky rotation angle.",
        existing_comment="Sky rotation angle at the start of the exposure, computed by the pointing component from the mount and rotator positions.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "s_dec",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; declination of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_comment="Central Spatial Position in ICRS; declination of focal plane center at the start of the exposure, derived from encoder readings and correcting for annual aberration, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
    op.alter_column(
        "exposure",
        "s_ra",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        comment="Central Spatial Position in ICRS; right ascension of focal plane center derived from encoder readings and correcting for annual abberation, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_comment="Central Spatial Position in ICRS; right ascension of focal plane center at the start of the exposure, derived from encoder readings and correcting for annual aberration, precession-nutation, earth orientation, atmospheric refraction, and mount/flexure model, determined without reference to a plate solution.",
        existing_nullable=True,
        schema="cdb_latiss",
    )
