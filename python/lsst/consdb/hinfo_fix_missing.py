import re
from math import radians, sin
from typing import Any

import sqlalchemy as sa
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from sqlalchemy.orm import Session

from .utils import setup_logging, setup_postgres


class Fixer:
    """A collection of functions that try to patch up missing data columns."""

    def __init__(self, exposure_rec: dict[str, Any], logger=None):
        """Calls all fixup methods.

        Given an `exposure_rec` dictionary, apply all fixup methods to the
        dictionary in one go. Call this to apply the fixup methods. To add
        more fixup methods, just add them to this class, make sure the
        method name starts with "fix_", and make sure the signature matches:
            def fix_whatever(self, exposure_rec: dict[str, Any])
        The method should return a dictionary with keys to update.

        """
        self.logger = logger if logger is not None else setup_logging("hinfo_fix_missing")
        self.updates: dict[str, Any]
        self.updates = {}
        for attr_name in dir(self):
            if attr_name.startswith("fix_"):
                attr = getattr(self, attr_name)
                self.updates = {**self.updates, **attr(exposure_rec)}

    def fix_telescope_position(self, exposure_rec: dict[str, Any]) -> dict[str, Any]:
        """Attempts to fill in missing sky position columns.

        It relies on s_ra and s_dec being present, and does
        calculations to obtain altitude, azimuth and zenith
        distance for the beginning, middle, and end of the
        exposure as well as airmass.

        It modifies the `exposure_rec` dictionary and returns nothing.

        Parameters
        ----------
        exposure_rec : `dict[str, Any]`
            The exposure record dictionary, (almost) ready to
            be copied into consolidated database exposure
            table.

        Returns
        -------
        dict[str, Any]
            Fixed columns in the original `exposure_rec` dictionary.
        """

        if exposure_rec["airmass"] is not None:
            # No need to do calculations, it's already done.
            return dict()

        if exposure_rec["s_ra"] is None or exposure_rec["s_dec"] is None:
            # Bail out because we don't have enough info.
            return dict()

        if exposure_rec["s_ra"] == 0.0 and exposure_rec["s_dec"] == 0.0:
            # Bail out because ra and dec don't appear to be valid.
            return dict()

        # Convert from RA and Dec
        s_ra, s_dec = map(lambda x: float(exposure_rec[x]), ("s_ra", "s_dec"))
        location = EarthLocation.of_site("LSST")
        obstimes = Time(
            [
                exposure_rec["obs_start_mjd"],
                exposure_rec["exp_midpt_mjd"],
                exposure_rec["obs_end_mjd"],
            ],
            format="mjd",
            scale="tai",
        )
        coord = SkyCoord(s_ra, s_dec, unit="deg")
        altaz = coord.transform_to(AltAz(obstime=obstimes, location=location))

        # Get altaz calculations
        altitude_start, altitude, altitude_end = altaz.alt.deg
        azimuth_start, azimuth, azimuth_end = altaz.az.deg
        zenith_distance_start, zenith_distance, zenith_distance_end = altaz.zen.deg

        # Use K&Y 1989 model to compute airmass from altitude
        airmass = None
        if altitude >= 0 and altitude <= 90:
            a_ky89 = 0.50572
            b_ky89 = 6.07995
            c_ky89 = 1.6364
            airmass = 1 / (sin(radians(altitude)) + a_ky89 * (altitude + b_ky89) ** -c_ky89)

        # Load them into the update dictionary.
        update = {}
        calculations = {
            "altitude_start": altitude_start,
            "altitude": altitude,
            "altitude_end": altitude_end,
            "azimuth_start": azimuth_start,
            "azimuth": azimuth,
            "azimuth_end": azimuth_end,
            "zenith_distance_start": zenith_distance_start,
            "zenith_distance": zenith_distance,
            "zenith_distance_end": zenith_distance_end,
            "airmass": airmass,
        }
        for key, value in calculations.items():
            if exposure_rec[key] is None and value is not None:
                update[key] = value
                self.logger.debug(f"Inferring column: {key}")
        return update

    def fix_band(self, exposure_rec: dict[str, Any]) -> dict[str, Any]:
        """Tries to identify band, if not provided.

        This function relies on the physical_filter column to
        indicate the band. It uses two formats:
         * u_01 => u band, seen in LSSTComCam
         * SDSSr_65mm~empty => r band, seen in LATISS

        It modifies the `exposure_rec` dictionary and returns
        nothing.

        Parameters
        ----------
        exposure_rec : `dict[str, Any]`
            The exposure record dictionary, (almost) ready to
            be copied into consolidated database exposure
            table.

        Returns
        -------
        dict[str, Any]
            Fixed columns in the original `exposure_rec` dictionary.
        """
        if exposure_rec["band"] is not None:
            # Band already set
            return dict()

        if exposure_rec["physical_filter"] is None:
            # Can't infer band from physical_filter
            return dict()

        for band in "ugrizy":
            if f"SDSS{band}" in exposure_rec["physical_filter"]:
                exposure_rec["band"] = band
                self.logger.debug("Inferring column: band")
                return {"band": band}

            if re.fullmatch(f"{band}_[0-9]+", exposure_rec["physical_filter"]):
                self.logger.debug("Inferring column: band")
                exposure_rec["band"] = band
                return {"band": band}

        return dict()

    def fix_dark_time(self, exposure_rec: dict[str, Any]) -> dict[str, Any]:
        """Tries to fill in missing dark_time information from the record.

        The interval from exposure start time to end time seems to be
        a really good proxy for dark_time. If that's not available, we
        fall back on the exposure time as an estimate.

        Parameters
        ----------
        exposure_rec : `dict[str, Any]`
            The exposure record dictionary, (almost) ready to
            be copied into consolidated database exposure
            table.

        Returns
        -------
        dict[str, Any]
            Fixed columns in the original `exposure_rec` dictionary.
        """
        if exposure_rec["dark_time"] is not None:
            return dict()

        if exposure_rec["obs_start_mjd"] is not None and exposure_rec["obs_end_mjd"] is not None:
            self.logger.debug("Inferring column: dark_time")
            seconds_per_day = 86400
            return {
                "dark_time": seconds_per_day * (exposure_rec["obs_end_mjd"] - exposure_rec["obs_start_mjd"])
            }

        if exposure_rec["exp_time"] is None:
            return dict()

        # Fall back to exposure time
        self.logger.debug("Inferring column: dark_time")
        return {"dark_time": exposure_rec["exp_time"]}


def fixup(schema: str, day_obs: int | None = None, seq_num: int | None = None) -> None:
    """Fixes a specified row in the exposure table.

    The row specified by `day_obs` and `seq_num` will be modified
    if any columns can be inferred from the existing data. If
    `day_obs` and `seq_num` are None, then the entire table
    will be recalculated.

    Parameters
    ----------
    day_obs : int | None
        The day of the observation to modify, or None to operate
        on the whole table.

    seq_num : int | None
        The image sequence number to modify, or None to operate
        on the whole table.
    """
    engine = setup_postgres()
    session = Session(bind=engine)

    # Set up a database query
    md = sa.MetaData(schema=f"cdb_{schema}")
    md.reflect(engine)
    exposure_table = md.tables[f"cdb_{schema}.exposure"]
    stmt = sa.select(exposure_table)
    if day_obs is not None and seq_num is not None:
        stmt = stmt.where(
            exposure_table.c.day_obs == day_obs,
            exposure_table.c.seq_num == seq_num,
        )

    # Run and process the query
    rows = session.execute(stmt)
    for row in rows:
        # Try to re-calculate any missing columns
        exposure_rec = {col.name: getattr(row, col.name) for col in exposure_table.columns}
        updates = Fixer(exposure_rec).updates

        if len(updates) > 0:
            # There are values to update, so send them to the DB

            stmt = (
                sa.update(exposure_table)
                .where(
                    exposure_table.c.day_obs == row.day_obs,
                    exposure_table.c.seq_num == row.seq_num,
                )
                .values(updates)
            )
            session.execute(stmt)
            session.commit()


if __name__ == "__main__":
    import sys

    schema = sys.argv[1]
    day_obs = None
    seq_num = None

    if len(sys.argv) > 2:
        day_obs = int(sys.argv[2])
        seq_num = int(sys.argv[3])

    fixup(schema, day_obs, seq_num)
