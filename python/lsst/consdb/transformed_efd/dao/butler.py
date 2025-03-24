# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Provides the `ButlerDao` class for interacting with data via Butler object.

It includes methods to query dimensions and retrieve exposures or visits within
specified time periods.
"""

import astropy.time
import pandas
from lsst.daf.butler import Butler


class ButlerDao:
    """A class that provides data access methods for querying Butler.

    Args:
    ----
        butler (Butler): The Butler object used for data access.

    """

    def __init__(self, butler: Butler):
        """Initialize the `ButlerDao` class.

        Args:
        ----
            butler (Butler): The Butler object used for data access.

        """
        self.butler = butler

    def query_dimension_to_list(self, resultset) -> list:
        """Convert given resultset to a list of dictionaries.

        Args:
        ----
            resultset: The resultset to be converted.

        Returns:
        -------
            A list of dictionaries representing the resultset.

        """
        list_of_dicts = [r.toDict() for r in resultset]
        return list_of_dicts

    def query_dimension_to_dataframe(self, resultset) -> pandas.DataFrame:
        """Convert resultset of query dimensions to a pandas DataFrame.

        Args:
        ----
            resultset: The resultset of query dimensions.

        Returns:
        -------
            A pandas DataFrame containing the query dimensions.

        """
        return pandas.DataFrame(self.query_dimension_to_list(resultset))

    def exposures_by_period(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> list:
        """Retrieves exposures for a time period for the specified instrument.


        Args:
        ----
            instrument (str): The instrument name.
            start_time (astropy.time.Time): The start time of the period.
            end_time (astropy.time.Time): The end time of the period.

        Returns:
        -------
            list: A list of exposures within the specified time period.

        """
        where_clause = (
            f"instrument=instr and exposure.timespan OVERLAPS " f"(T'{start_time}/utc', T'{end_time}/utc')"
        )

        resultset = self.butler.registry.queryDimensionRecords(
            "exposure", where=where_clause, bind=dict(instr=instrument)
        ).order_by("timespan.begin")
        return self.query_dimension_to_list(resultset)

    def visits_by_period(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> list:
        """Retrieves visits for a time period for the specified instrument.

        Args:
        ----
            instrument (str): The instrument name.
            start_time (astropy.time.Time): The start time of the period.
            end_time (astropy.time.Time): The end time of the period.

        Returns:
        -------
            list: A list of visits within the specified time period.

        """
        where_clause = (
            f"instrument=instr and visit.timespan OVERLAPS " f"(T'{start_time}/utc', T'{end_time}/utc')"
        )

        resultset = self.butler.registry.queryDimensionRecords(
            "visit", where=where_clause, bind=dict(instr=instrument)
        ).order_by("timespan.begin")

        return self.query_dimension_to_list(resultset)
