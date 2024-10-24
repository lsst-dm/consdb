import astropy.time
import pandas
from lsst.daf.butler import Butler


class ButlerDao:
    """
    A class that provides data access methods for querying dimensions using
    a Butler object.

    Args:
        butler (Butler): The Butler object used for data access.

    """

    def __init__(self, butler: Butler):
        self.butler = butler

    def query_dimension_to_list(self, resultset) -> list:
        """
        Converts the given resultset to a list of dictionaries.

        Args:
            resultset: The resultset to be converted.

        Returns:
            A list of dictionaries representing the resultset.
        """
        list_of_dicts = [r.toDict() for r in resultset]
        return list_of_dicts

    def query_dimension_to_dataframe(self, resultset) -> pandas.DataFrame:
        """
        Converts a resultset of query dimensions to a pandas DataFrame.

        Args:
            resultset: The resultset of query dimensions.

        Returns:
            A pandas DataFrame containing the query dimensions.
        """
        return pandas.DataFrame(self.query_dimension_to_list(resultset))

    def exposures_by_period(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> list:
        """
        Retrieve a list of exposures within a specified time period for a
        given instrument.

        Args:
            instrument (str): The instrument name.
            start_time (astropy.time.Time): The start time of the period.
            end_time (astropy.time.Time): The end time of the period.

        Returns:
            list: A list of exposures within the specified time period.

        """
        where_clause = (
            f"instrument=instr and exposure.timespan OVERLAPS (T'{start_time}/utc', T'{end_time}/utc')"
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
        """
        Retrieve a list of visits within a specified time period for a given
        instrument.

        Args:
            instrument (str): The instrument name.
            start_time (astropy.time.Time): The start time of the period.
            end_time (astropy.time.Time): The end time of the period.

        Returns:
            list: A list of visits within the specified time period.

        """
        where_clause = (
            f"instrument=instr and visit.timespan OVERLAPS (T'{start_time}/utc', T'{end_time}/utc')"
        )

        resultset = self.butler.registry.queryDimensionRecords(
            "visit", where=where_clause, bind=dict(instr=instrument)
        ).order_by("timespan.begin")

        return self.query_dimension_to_list(resultset)
