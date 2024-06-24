import pandas
from dao.base import DBBase
from sqlalchemy.sql import and_, select


class ExposureEfdDao(DBBase):
    """
    A class representing a Data Access Object (DAO) for accessing
    ExposureEFD data.

    Args:
        db_uri (str): The URI of the database.

    Attributes:
        tbl: The table object representing the "ExposureEFD" table in the
        database.

    """

    def __init__(self, db_uri: str):
        super(ExposureEfdDao, self).__init__(db_uri)

        self.tbl = self.get_table("ExposureEFD")

    def get_by_exposure_id(self, exposure_id: int):
        """
        Retrieves rows from the "ExposureEFD" table based on exposure ID.

        Args:
            exposure_id (int): The exposure ID.

        Returns:
            list: A list of dictionaries representing the rows retrieved from
                the table.

        """
        stm = select(self.tbl.c).where(and_(self.tbl.c.exposure_id == exposure_id))

        rows = self.fetch_all_dict(stm)

        return rows

    def get_by_exposure_id_instrument(self, exposure_id: int, instrument: str):
        """
        Retrieves rows from the "ExposureEFD" table based on exposure ID and
        instrument.

        Args:
            exposure_id (int): The exposure ID.
            instrument (str): The instrument name.

        Returns:
            list: A list of dictionaries representing the rows retrieved from
                the table.

        """
        stm = select(self.tbl.c).where(
            and_(self.tbl.c.exposure_id == exposure_id, self.tbl.c.instrument == instrument)
        )

        rows = self.fetch_all_dict(stm)

        return rows

    def count(self):
        """
        Returns the count of rows in the "ExposureEFD" table.

        Returns:
            int: The count of rows in the table.

        """
        return self.execute_count(self.tbl)

    def upsert(self, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """
        Upserts a DataFrame into the "ExposureEFD" table.

        Args:
            df (pandas.DataFrame): The DataFrame to be upserted.
            commit_every (int, optional): The number of rows to commit
            at a time. Defaults to 100.

        Returns:
            int: The number of rows upserted.

        """
        return self.execute_upsert(tbl=self.tbl, df=df, commit_every=commit_every)
