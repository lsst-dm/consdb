"""Provides the `ExposureEfdDao` class."""

import pandas
from lsst.consdb.transformed_efd.dao.base import DBBase
from sqlalchemy.sql import and_, select


class ExposureEfdDao(DBBase):
    """A class representing a Data Access Object (DAO) for accessing exposure_efd data.

    Args:
    ----
        db_uri (str): The URI of the database.

    Attributes:
    ----------
        tbl: The table object representing the "exposure_efd" table in the database.

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
            list: A list of dictionaries representing the rows retrieved from the table.

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
