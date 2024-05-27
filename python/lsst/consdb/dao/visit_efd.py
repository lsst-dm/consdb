import pandas
from dao.base import DBBase
from sqlalchemy.sql import and_, select


class VisitEfdDao(DBBase):
    def __init__(self, db_uri: str):
        super(VisitEfdDao, self).__init__(db_uri)

        self.tbl = self.get_table("VisitEFD")

    def get_by_visit_id(self, visit_id: int):

        stm = select(self.tbl.c).where(and_(self.tbl.c.visit_id == visit_id))

        rows = self.fetch_all_dict(stm)

        return rows

    def get_by_visit_id_instrument(self, visit_id: int, instrument: str):

        stm = select(self.tbl.c).where(
            and_(self.tbl.c.visit_id == visit_id, self.tbl.c.instrument == instrument)
        )

        rows = self.fetch_all_dict(stm)

        return rows

    def count(self):
        return self.execute_count(self.tbl)

    def upsert(self, df: pandas.DataFrame) -> int:
        return self.execute_upsert(tbl=self.tbl, df=df)
