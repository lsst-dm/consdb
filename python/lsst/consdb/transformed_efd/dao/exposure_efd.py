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

"""Provides the `ExposureEfdDao` class."""

import pandas
from lsst.consdb.transformed_efd.dao.base import DBBase
from sqlalchemy.sql import and_, select


class ExposureEfdDao(DBBase):
    """Represents a DAO for accessing exposure_efd data.

    Args:
    ----
        db_uri (str): The URI of the database.

    Attributes:
    ----------
        tbl: The table object for the 'exposure_efd' table.

    """

    def __init__(self, db_uri: str, schema: str):
        """Initialize the `ExposureEfdDao` class.

        Args:
        ----
            db_uri (str): The URI of the database.
            schema (str): The schema name in the database.

        """
        super(ExposureEfdDao, self).__init__(db_uri, schema)

        self.tbl = self.get_table("exposure_efd", schema=schema)

    def get_by_exposure_id(self, exposure_id: int):
        """Retrieve row from the "exposure_efd" table based on exposure ID.

        Args:
        ----
            exposure_id (int): The exposure ID.

        Returns:
        -------
            list: List of dictionaries for rows retrieved from the table.

        """
        stm = select(self.tbl.c).where(and_(self.tbl.c.exposure_id == exposure_id))

        rows = self.fetch_all_dict(stm)

        return rows

    def count(self):
        """Return count of rows in the "exposure_efd" table.

        Returns
        -------
            int: The count of rows in the table.

        """
        return self.execute_count(self.tbl)

    def upsert(self, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """Upsert DataFrame into the "exposure_efd" table.

        Args:
        ----
            df (pandas.DataFrame): The DataFrame to be upserted.
            commit_every (int, optional): The number of rows to commit
            at a time. Defaults to 100.

        Returns:
        -------
            int: The number of rows upserted.

        """
        return self.execute_upsert(tbl=self.tbl, df=df, commit_every=commit_every)


class ExposureEfdUnpivotedDao(DBBase):
    """A class representing a DAO for accessing exposure_efd_unpivoted data.

    Args:
    ----
        db_uri (str): The URI of the database.

    Attributes:
    ----------
        tbl: The table object representing the "exposure_efd_unpivoted" table
        in the database.

    """

    def __init__(self, db_uri: str, schema: str):
        """Initialize the `ExposureEfdUnpivotedDao` class.

        Args:
        ----
            db_uri (str): The URI of the database.
            schema (str): The schema name in the database.

        """
        super(ExposureEfdUnpivotedDao, self).__init__(db_uri, schema)

        self.tbl = self.get_table("exposure_efd_unpivoted", schema=schema)

    def get_by_exposure_id(self, exposure_id: int):
        """Retrieves a row from 'exposure_efd_unpivoted' by exposure ID.

        Args:
        ----
            exposure_id (int): The exposure ID.

        Returns:
        -------
            list: A list of dictionaries representing the rows retrieved from
                the table.

        """
        stm = select(self.tbl.c).where(self.tbl.c.exposure_id == exposure_id)

        rows = self.fetch_all_dict(stm)

        return rows

    def count(self):
        """Return count of rows in the "exposure_efd_unpivoted" table.

        Returns
        -------
            int: The count of rows in the table.

        """
        return self.execute_count(self.tbl)

    def upsert(self, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """Upsert DataFrame into the "exposure_efd_unpivoted" table.

        Args:
        ----
            df (pandas.DataFrame): The DataFrame to be upserted.
            commit_every (int, optional): The number of rows to commit
            at a time. Defaults to 100.

        Returns:
        -------
            int: The number of rows upserted.

        """
        return self.execute_upsert(tbl=self.tbl, df=df, commit_every=commit_every)
