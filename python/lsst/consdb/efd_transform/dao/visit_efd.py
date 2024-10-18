import pandas
from dao.base import DBBase
from sqlalchemy.sql import and_, select


class VisitEfdDao(DBBase):
    """
    Data Access Object for visit1_efd table.

    Args:
        db_uri (str): The URI of the database.

    Attributes:
        tbl: The visit1_efd table object.

    """

    def __init__(self, db_uri: str, schema: str):
        super(VisitEfdDao, self).__init__(db_uri, schema)

        self.tbl = self.get_table("visit1_efd", schema=schema)

    def get_by_visit_id(self, visit_id: int):
        """
        Retrieve rows from the table based on visit_id.

        Args:
            visit_id (int): The visit_id to filter the rows.

        Returns:
            list: A list of rows matching the visit_id.

        """
        stm = select(self.tbl.c).where(and_(self.tbl.c.visit_id == visit_id))

        rows = self.fetch_all_dict(stm)

        return rows

    def get_by_visit_id_instrument(self, visit_id: int, instrument: str):
        """
        Retrieve rows from the table based on visit_id and instrument.

        Args:
            visit_id (int): The visit_id to filter the rows.
            instrument (str): The instrument to filter the rows.

        Returns:
            list: A list of rows matching the visit_id and instrument.

        """
        stm = select(self.tbl.c).where(
            and_(self.tbl.c.visit_id == visit_id, self.tbl.c.instrument == instrument)
        )

        rows = self.fetch_all_dict(stm)

        return rows

    def count(self):
        """
        Get the count of rows in the table.

        Returns:
            int: The count of rows in the table.

        """
        return self.execute_count(self.tbl)

    def upsert(self, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """
        Upsert data into the table.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data to upsert.
            commit_every (int, optional): The number of rows to commit at once.
            Defaults to 100.

        Returns:
            int: The number of rows upserted.

        """
        return self.execute_upsert(tbl=self.tbl, df=df, commit_every=commit_every)
