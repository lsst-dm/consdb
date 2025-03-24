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

"""Defines the `VisitEfdUnpivotedDao` class."""

import pandas
from lsst.consdb.transformed_efd.dao.base import DBBase
from sqlalchemy.sql import select


class VisitEfdUnpivotedDao(DBBase):
    """Data Access Object for visit1_efd_unpivoted table.

    Args:
    ----
        db_uri (str): The URI of the database.

    Attributes:
    ----------
        tbl: The visit1_efd_unpivoted table object.

    """

    def __init__(self, db_uri: str, schema: str):
        """Initialize the `VisitEfdUnpivotedDao` class.

        Args:
        ----
            db_uri (str): The URI of the database.
            schema (str): The schema name in the database.

        """
        super(VisitEfdUnpivotedDao, self).__init__(db_uri, schema)

        self.tbl = self.get_table("visit1_efd_unpivoted", schema=schema)

    def get_by_visit_id(self, visit_id: int):
        """Retrieve rows from the table based on visit_id.

        Args:
        ----
            visit_id (int): The visit_id to filter the rows.

        Returns:
        -------
            list: A list of rows matching the visit_id.

        """
        stm = select(self.tbl.c).where(self.tbl.c.visit_id == visit_id)

        rows = self.fetch_all_dict(stm)

        return rows

    def count(self):
        """Get the count of rows in the table.

        Returns
        -------
            int: The count of rows in the table.

        """
        return self.execute_count(self.tbl)

    def upsert(self, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """Upsert data into the table.

        Args:
        ----
            df (pandas.DataFrame): The DataFrame containing the data to upsert.
            commit_every (int, optional): The number of rows to commit at once.
            Defaults to 100.

        Returns:
        -------
            int: The number of rows upserted.

        """
        return self.execute_upsert(tbl=self.tbl, df=df, commit_every=commit_every)
