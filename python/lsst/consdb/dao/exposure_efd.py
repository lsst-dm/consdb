import pandas
from dao.base import DBBase
from sqlalchemy.sql import and_, select


class ExposureEfdDao(DBBase):
    def __init__(self, db_uri: str):
        super(ExposureEfdDao, self).__init__(db_uri)

        self.tbl = self.get_table("ExposureEFD")

    def get_by_exposure_id(self, exposure_id: int):

        stm = select(self.tbl.c).where(and_(self.tbl.c.exposure_id == exposure_id))

        rows = self.fetch_all_dict(stm)

        return rows

    def get_by_exposure_id_instrument(self, exposure_id: int, instrument: str):

        stm = select(self.tbl.c).where(
            and_(self.tbl.c.exposure_id == exposure_id, self.tbl.c.instrument == instrument)
        )

        rows = self.fetch_all_dict(stm)

        return rows

    def count(self):
        return self.execute_count(self.tbl)

    def upsert(self, df: pandas.DataFrame) -> int:
        return self.execute_upsert(tbl=self.tbl, df=df)
