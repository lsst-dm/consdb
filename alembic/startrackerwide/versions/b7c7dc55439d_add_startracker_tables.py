"""Add startracker tables

Revision ID: b7c7dc55439d
Revises:
Create Date: 2024-11-12 18:36:00.641218+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql, postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7c7dc55439d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "exposure",
        sa.Column(
            "exposure_id",
            sa.BIGINT().with_variant(mysql.BIGINT(), "mysql").with_variant(sa.BIGINT(), "postgresql"),
            nullable=False,
            comment="Unique identifier.",
        ),
        sa.Column(
            "day_obs",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=False,
            comment="Day of observation.",
        ),
        sa.Column(
            "seq_num",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=False,
            comment="Sequence number.",
        ),
        sa.Column(
            "s_ra",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="Central Spatial Position in ICRS; Right ascension of targeted focal plane center.",
        ),
        sa.Column(
            "s_dec",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="Central Spatial Position in ICRS; Declination of targeted focal plane center.",
        ),
        sa.Column(
            "sky_rotation",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="Targeted sky rotation angle.",
        ),
        sa.Column(
            "azimuth_start",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Azimuth of focal plane center at the start of the exposure.",
        ),
        sa.Column(
            "azimuth_end",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Azimuth of focal plane center at the end of the exposure.",
        ),
        sa.Column(
            "azimuth",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Azimuth of focal plane center at the middle of the exposure.",
        ),
        sa.Column(
            "altitude_start",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Altitude of focal plane center at the start of the exposure.",
        ),
        sa.Column(
            "altitude_end",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Altitude of focal plane center at the end of the exposure.",
        ),
        sa.Column(
            "altitude",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Altitude of focal plane center at the middle of the exposure.",
        ),
        sa.Column(
            "zenith_distance_start",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Zenith distance at the start of the exposure.",
        ),
        sa.Column(
            "zenith_distance_end",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Zenith distance at the end of the exposure.",
        ),
        sa.Column(
            "zenith_distance",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Zenith distance at the middle of the exposure.",
        ),
        sa.Column(
            "airmass",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Airmass of the observed line of sight at the middle of the exposure.",
        ),
        sa.Column(
            "exp_midpt",
            sa.TIMESTAMP()
            .with_variant(mysql.DATETIME(fsp=6), "mysql")
            .with_variant(postgresql.TIMESTAMP(precision=6), "postgresql"),
            nullable=True,
            comment="Midpoint time for exposure at the fiducial center of the focal plane. array. TAI, accurate to 10ms.",
        ),
        sa.Column(
            "exp_midpt_mjd",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="Midpoint time for exposure at the fiducial center of the focal plane. array in MJD. TAI, accurate to 10ms.",
        ),
        sa.Column(
            "obs_start",
            sa.TIMESTAMP()
            .with_variant(mysql.DATETIME(fsp=6), "mysql")
            .with_variant(postgresql.TIMESTAMP(precision=6), "postgresql"),
            nullable=True,
            comment="Start time of the exposure at the fiducial center of the focal plane. array, TAI, accurate to 10ms.",
        ),
        sa.Column(
            "obs_start_mjd",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="Start of the exposure in MJD, TAI, accurate to 10ms.",
        ),
        sa.Column(
            "obs_end",
            sa.TIMESTAMP()
            .with_variant(mysql.DATETIME(fsp=6), "mysql")
            .with_variant(postgresql.TIMESTAMP(precision=6), "postgresql"),
            nullable=True,
            comment="End time of the exposure at the fiducial center of the focal plane. array, TAI, accurate to 10ms.",
        ),
        sa.Column(
            "obs_end_mjd",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="End of the exposure in MJD, TAI, accurate to 10ms.",
        ),
        sa.Column(
            "exp_time",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Spatially-averaged duration of exposure, accurate to 10ms.",
        ),
        sa.Column(
            "img_type",
            sa.VARCHAR(length=64)
            .with_variant(mysql.VARCHAR(length=64), "mysql")
            .with_variant(sa.VARCHAR(length=64), "postgresql"),
            nullable=True,
            comment="Type of exposure taken.",
        ),
        sa.Column(
            "target_name",
            sa.VARCHAR(length=64)
            .with_variant(mysql.VARCHAR(length=64), "mysql")
            .with_variant(sa.VARCHAR(length=64), "postgresql"),
            nullable=True,
            comment="Target of the observation.",
        ),
        sa.Column(
            "air_temp",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Outside air temperature in degC.",
        ),
        sa.Column(
            "pressure",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Outside air pressure.",
        ),
        sa.Column(
            "humidity",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Outside relative humidity.",
        ),
        sa.Column(
            "wind_speed",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Outside wind speed.",
        ),
        sa.Column(
            "wind_dir",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Wind direction.",
        ),
        sa.Column(
            "dimm_seeing",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Seeing as measured by external DIMM (FWHM).",
        ),
        sa.Column(
            "dome_azimuth",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Dome azimuth.",
        ),
        sa.Column(
            "vignette",
            sa.VARCHAR(length=10)
            .with_variant(mysql.VARCHAR(length=10), "mysql")
            .with_variant(sa.VARCHAR(length=10), "postgresql"),
            nullable=True,
            comment="Instrument blocked from the sky: UNKNOWN, NO, PARTIALLY, FULLY.",
        ),
        sa.Column(
            "vignette_min",
            sa.VARCHAR(length=10)
            .with_variant(mysql.VARCHAR(length=10), "mysql")
            .with_variant(sa.VARCHAR(length=10), "postgresql"),
            nullable=True,
            comment="Lowest amount of instrument vignetting detected during the exposure: UNKNOWN, NO, PARTIALLY, FULLY.",
        ),
        sa.PrimaryKeyConstraint("exposure_id"),
        sa.UniqueConstraint("day_obs", "seq_num", name="un_day_obs_seq_num"),
        schema="cdb_startrackerwide",
        mysql_engine="MyISAM",
    )
    op.create_table(
        "exposure_flexdata_schema",
        sa.Column(
            "key",
            sa.VARCHAR(length=128)
            .with_variant(mysql.VARCHAR(length=128), "mysql")
            .with_variant(sa.VARCHAR(length=128), "postgresql"),
            nullable=False,
            comment="Name of key.",
        ),
        sa.Column(
            "dtype",
            sa.VARCHAR(length=64)
            .with_variant(mysql.VARCHAR(length=64), "mysql")
            .with_variant(sa.VARCHAR(length=64), "postgresql"),
            nullable=False,
            comment="Name of the data type of the value, one of bool, int, float, str.",
        ),
        sa.Column(
            "doc",
            sa.TEXT().with_variant(mysql.LONGTEXT(), "mysql").with_variant(sa.TEXT(), "postgresql"),
            nullable=False,
            comment="Documentation string.",
        ),
        sa.Column(
            "unit",
            sa.VARCHAR(length=128)
            .with_variant(mysql.VARCHAR(length=128), "mysql")
            .with_variant(sa.VARCHAR(length=128), "postgresql"),
            nullable=True,
            comment="Unit for the value. Should be from the IVOA (https://www.ivoa.net/documents/VOUnits/) or astropy.",
        ),
        sa.Column(
            "ucd",
            sa.VARCHAR(length=128)
            .with_variant(mysql.VARCHAR(length=128), "mysql")
            .with_variant(sa.VARCHAR(length=128), "postgresql"),
            nullable=True,
            comment="IVOA Unified Content Descriptor (https://www.ivoa.net/documents/UCD1+/).",
        ),
        sa.PrimaryKeyConstraint("key"),
        schema="cdb_startrackerwide",
        mysql_engine="MyISAM",
    )
    op.create_table(
        "exposure_flexdata",
        sa.Column(
            "obs_id",
            sa.BIGINT().with_variant(mysql.BIGINT(), "mysql").with_variant(sa.BIGINT(), "postgresql"),
            nullable=False,
            comment="Unique identifier.",
        ),
        sa.Column(
            "key",
            sa.VARCHAR(length=128)
            .with_variant(mysql.VARCHAR(length=128), "mysql")
            .with_variant(sa.VARCHAR(length=128), "postgresql"),
            nullable=False,
            comment="Name of key.",
        ),
        sa.Column(
            "value",
            sa.TEXT().with_variant(mysql.LONGTEXT(), "mysql").with_variant(sa.TEXT(), "postgresql"),
            nullable=True,
            comment="Content of value as a string.",
        ),
        sa.ForeignKeyConstraint(
            ["key"], ["cdb_startrackerwide.exposure_flexdata_schema.key"], name="fk_exposure_flexdata_key"
        ),
        sa.ForeignKeyConstraint(
            ["obs_id"], ["cdb_startrackerwide.exposure.exposure_id"], name="fk_exposure_flexdata_obs_id"
        ),
        sa.PrimaryKeyConstraint("obs_id", "key"),
        schema="cdb_startrackerwide",
        mysql_engine="MyISAM",
    )
    op.create_table(
        "exposure_quicklook",
        sa.Column(
            "exposure_id",
            sa.BIGINT().with_variant(mysql.BIGINT(), "mysql").with_variant(sa.BIGINT(), "postgresql"),
            nullable=False,
            comment="Unique identifier.",
        ),
        sa.Column(
            "ra",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="Central Spatial Position in ICRS; Right ascension of fitted WCS.",
        ),
        sa.Column(
            "dec",
            sa.DOUBLE()
            .with_variant(mysql.DOUBLE(asdecimal=True), "mysql")
            .with_variant(sa.DOUBLE_PRECISION(), "postgresql"),
            nullable=True,
            comment="Central Spatial Position in ICRS; Declination of fitted WCS.",
        ),
        sa.Column(
            "astrom_offset_mean",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Mean offset of astrometric calibration matches.",
        ),
        sa.Column(
            "astrom_offset_std",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Standard deviation of offsets of astrometric calibration matches.",
        ),
        sa.Column(
            "mean_var",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Mean of the variance plane.",
        ),
        sa.Column(
            "n_psf_star",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Number of stars used for PSF model.",
        ),
        sa.Column(
            "psf_area",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF area.",
        ),
        sa.Column(
            "psf_ixx",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF Ixx moment.",
        ),
        sa.Column(
            "psf_ixy",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF Ixy moment.",
        ),
        sa.Column(
            "psf_iyy",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF Iyy moment",
        ),
        sa.Column(
            "psf_sigma",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="PSF sigma.",
        ),
        sa.Column(
            "psf_star_delta_e1_median",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Median E1 residual (starE1 - psfE1) for PSF stars.",
        ),
        sa.Column(
            "psf_star_delta_e1_scatter",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Scatter (via MAD) of E1 residual (starE1 - psfE1) for PSF stars.",
        ),
        sa.Column(
            "psf_star_delta_e2_median",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Median E2 residual (starE2 - psfE2) for PSF stars.",
        ),
        sa.Column(
            "psf_star_delta_e2_scatter",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Scatter (via MAD) of E2 residual (starE2 - psfE2) for PSF stars.",
        ),
        sa.Column(
            "psf_star_delta_size_median",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Median size residual (starSize - psfSize) for PSF stars.",
        ),
        sa.Column(
            "psf_star_delta_size_scatter",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Scatter (via MAD) of size residual (starSize - psfSize) for stars.",
        ),
        sa.Column(
            "psf_star_scaled_delta_size_scatter",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Scatter (via MAD) of size residual scaled by median size squared.",
        ),
        sa.Column(
            "psf_trace_radius_delta",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Delta (max - min) of model PSF trace radius values evaluated on a grid of unmasked pixels.",
        ),
        sa.Column(
            "sky_bg",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="Average sky background.",
        ),
        sa.Column(
            "sky_noise",
            sa.FLOAT().with_variant(mysql.FLOAT(), "mysql").with_variant(sa.FLOAT(), "postgresql"),
            nullable=True,
            comment="RMS noise of the sky background.",
        ),
        sa.Column(
            "source_count",
            sa.INTEGER().with_variant(mysql.INTEGER(), "mysql").with_variant(sa.INTEGER(), "postgresql"),
            nullable=True,
            comment="Count of sources.",
        ),
        sa.ForeignKeyConstraint(
            ["exposure_id"], ["cdb_startrackerwide.exposure.exposure_id"], name="fk_exposure_quicklook_obs_id"
        ),
        sa.PrimaryKeyConstraint("exposure_id"),
        schema="cdb_startrackerwide",
        mysql_engine="MyISAM",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("exposure_quicklook", schema="cdb_startrackerwide")
    op.drop_table("exposure_flexdata", schema="cdb_startrackerwide")
    op.drop_table("exposure_flexdata_schema", schema="cdb_startrackerwide")
    op.drop_table("exposure", schema="cdb_startrackerwide")
    # ### end Alembic commands ###
