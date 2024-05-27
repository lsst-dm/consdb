import astropy.time
import pandas
from lsst.daf.butler import Butler


class ButlerDao:

    def __init__(self, butler: Butler):
        self.butler = butler

    def query_dimension_to_list(self, resultset):
        return [r.toDict() for r in resultset]

    def query_dimension_to_dataframe(self, resultset):
        return pandas.DataFrame([q.toDict() for q in resultset])

    def exposures_by_period(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> list:
        where_clause = f"instrument=instr and exposure.timespan OVERLAPS (T'{start_time}', T'{end_time}')"

        resultset = self.butler.registry.queryDimensionRecords(
            "exposure", where=where_clause, bind=dict(instr=instrument)
        )
        return self.query_dimension_to_list(resultset)

    def visits_by_period(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> list:
        where_clause = f"instrument=instr and visit.timespan OVERLAPS (T'{start_time}', T'{end_time}')"

        resultset = self.butler.registry.queryDimensionRecords(
            "visit", where=where_clause, bind=dict(instr=instrument)
        )

        return self.query_dimension_to_list(resultset)
