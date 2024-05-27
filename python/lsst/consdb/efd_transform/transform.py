import logging
from typing import Any, List, Union

import astropy.time
import lsst_efd_client
import numpy
import pandas
from dao.butler import ButlerDao
from dao.exposure_efd import ExposureEfdDao
from dao.visit_efd import VisitEfdDao
from efd_transform.summary import Summary
from lsst.daf.butler import Butler

# from sqlalchemy import Engine


class Transform:
    """
    A class that represents a data transformation process.

    Args:
        butler (Butler): The Butler object for accessing data.
        db_uri (str): The database connection string.
        efd (lsst_efd_client.EfdClient): The EFD client for accessing EFD data.
        config (dict[str, Any]): The configuration for the transformation
                                 process.
        logger (logging.Logger): The logger object for logging messages.

    Attributes:
        log (logging.Logger): The logger object for logging messages.
        butler_dao (ButlerDao): The DAO object for accessing data using the
                                Butler.
        db (Engine): The database engine for storing transformed data.
        efd (lsst_efd_client.EfdClient): The EFD client for accessing EFD data.
        config (dict[str, Any]): The configuration for the transformation
                                 process.
    """

    def __init__(
        self,
        butler: Butler,
        db_uri: str,
        efd: lsst_efd_client.EfdClient,
        config: dict[str, Any],
        logger: logging.Logger,
    ):
        """
        Initializes a new instance of the Transform class.

        Args:
            butler (Butler): The Butler object for accessing data.
            db_uri (str): The database connection string.
            efd (lsst_efd_client.EfdClient): The EFD client for accessing EFD data.
            config (dict[str, Any]): The configuration for the transformation process.
            logger (logging.Logger): The logger object for logging messages.
        """
        self.log = logger
        self.butler_dao = ButlerDao(butler)
        self.db_uri = db_uri
        self.efd = efd
        self.config = config

        self.log.info("----------- MAIN -----------")
        self.log.debug(f"DB URI: {self.db_uri}")
        self.log.debug(f"EFD: {self.efd}")
        self.log.debug(f"Configs Columns: {len(self.config['columns'])}")

    async def process_interval(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ):

        self.log.info(f"Proccessing interval {start_time} - {end_time}")

        # Retrieves all exposures for the period
        exposures = self.butler_dao.exposures_by_period(instrument, start_time, end_time)

        self.log.info(f"Exposures: {len(exposures)}")

        # Retrieves all visits for the period
        visits = self.butler_dao.visits_by_period(instrument, start_time, end_time)

        self.log.info(f"Visits: {len(visits)}")

        # Identifies the period that will be used to consult the topics
        topic_interval = self.get_topic_interval(start_time, end_time, exposures, visits)
        self.log.info(f"Topic interval: {topic_interval[0]} - {topic_interval[1]}")

        result_exp = {}
        for exposure in exposures:
            result_exp[exposure["id"]] = {
                "exposure_id": exposure["id"],
                "instrument": instrument,
            }

        result_vis = {}
        for visit in visits:
            result_vis[visit["id"]] = {
                "visit_id": visit["id"],
                "instrument": instrument,
            }

        # self.log.info(result_exp)

        # Iterates over the columns defined in the config.
        # for each column retrieves EFD topic information
        for column in self.config["columns"]:
            # self.log.debug(column)
            self.log.info(f"Proccessing Column: {column['name']}")

            # Array with all topics needed for this column
            # topics = [{'name': topic name, series: pandas.DataFrame}]
            topics = await self.topics_by_column(column, topic_interval)

            for exposure in exposures:
                column_value = self.proccess_column_value(
                    start_time=exposure["timespan"].begin,
                    end_time=exposure["timespan"].end,
                    topics=topics,
                    transform_function=column["function"],
                )

                result_exp[exposure["id"]][column["name"]] = column_value

            for visit in visits:

                column_value = self.proccess_column_value(
                    start_time=visit["timespan"].begin,
                    end_time=visit["timespan"].end,
                    topics=topics,
                    transform_function=column["function"],
                )

                result_vis[visit["id"]][column["name"]] = column_value

        results = []
        for result_row in result_exp:
            results.append(result_exp[result_row])

        df_exposures = pandas.DataFrame(results)
        # df_exposures = pandas.DataFrame(results[35:45])
        self.log.info(f"Exposure results to be inserted into the database: {len(df_exposures)}")

        exp_dao = ExposureEfdDao(db_uri=self.db_uri)
        affected_rows = exp_dao.upsert(df=df_exposures)
        self.log.info(f"Database rows affected: {affected_rows}")
        del results

        results = []
        for result_row in result_vis:
            results.append(result_vis[result_row])

        df_visits = pandas.DataFrame(results)
        self.log.info(f"Visit results to be inserted into the database: {len(df_visits)}")

        vis_dao = VisitEfdDao(db_uri=self.db_uri)
        affected_rows = vis_dao.upsert(df=df_visits)
        self.log.info(f"Database rows affected: {affected_rows}")
        del results

    def proccess_column_value(
        self, start_time: astropy.time.Time, end_time: astropy.time.Time, topics, transform_function
    ) -> Any:
        """
        Process the column value for a given time range and topics using an
        aggregation function.

        Args:
            start_time (astropy.time.Time): The start time of the time range.
            end_time (astropy.time.Time): The end time of the time range.
            topics: The topics to retrieve values from.
            transform_function: The function to apply to the values.

        Returns:
            The processed column value.

        """

        values = self.topic_values_by_exposure(start_time, end_time, topics)
        if len(values) > 1:
            values = self.concatenate_arrays(values)

        column_value = Summary(values).apply(transform_function)

        return column_value

    def topic_values_by_exposure(
        self, start_time: astropy.time.Time, end_time: astropy.time.Time, topics
    ) -> List:
        """
        Retrieve topic values for a given time range.

        Args:
            start_time (astropy.time.Time): The start time of the range.
            end_time (astropy.time.Time): The end time of the range.
            topics (list): A list of topics.

        Returns:
            list: A list of topic values for the given time range.
        """

        topics_values = []

        for topic in topics:

            topic_table = topic["series"]
            if not topic_table.empty:
                values = topic_table.loc[
                    (topic_table.index > str(start_time)) & (topic_table.index < str(end_time))
                ]
                topics_values.append(values)

        return topics_values

    def concatenate_arrays(
        self, input_data: Union[List[float], List[List[float]], numpy.ndarray, List[numpy.ndarray]]
    ) -> numpy.ndarray:
        """
        Concatenates values from a list or list of lists or a numpy array
        or list of numpy arrays, returning a single flat numpy array.

        Args:
            input_data (Union[List[float], List[List[float]],
                        numpy.ndarray, List[numpy.ndarray]]):
                Input data, can be a list of floats or list of lists of
                floats or a numpy array or list of numpy arrays.

        Returns:
            numpy.ndarray: Concatenated flat numpy array.

        Raises:
            TypeError: If the input data is not a list or list of lists or
                       a numpy array or list of numpy arrays.
        """
        if isinstance(input_data, numpy.ndarray):
            return numpy.concatenate(input_data.flat)
        elif isinstance(input_data, list):
            flat_arrays = [
                numpy.array(arr).flat if isinstance(arr, numpy.ndarray) else numpy.array(arr).flatten()
                for arr in input_data
            ]
            return numpy.concatenate(flat_arrays)
        else:
            raise TypeError(
                "Input data must be a list or list of lists or a numpy array or list of numpy arrays."
            )

    async def topics_by_column(self, column, topic_interval) -> list[dict]:
        """
        Retrieves the EFD topics and their corresponding series for a
        given column.

        Args:
            column (dict): The column containing the topics.
            topic_interval: The interval for retrieving the topic series.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary
                        contains the topic name and its series.
        """

        data = []
        for topic in column["topics"]:
            topic_series = await self.get_efd_values(topic, topic_interval)
            data.append({"topic": topic["name"], "series": topic_series})
            self.log.debug(f"EFD Topic {topic['name']} return {len(topic_series)} rows")

        return data

    async def get_efd_values(
        self,
        topic: dict[str, Any],
        topic_interval: list[astropy.time.Time],
    ) -> pandas.DataFrame:

        start = topic_interval[0].utc
        end = topic_interval[1].utc
        window = astropy.time.TimeDelta(topic.get("window", 0.0), format="sec")

        fields = [f["name"] for f in topic["fields"]]

        series = await self.efd.select_time_series(
            topic["name"],
            fields,
            start - window,
            end + window,
            topic.get("index", None),
        )

        # TODO: Currently doing a temporary resample and interpolate.
        # Only to simulate that there is more than one message
        # per exposure period and allow summarization to be done.
        # if len(series) > 0:
        #     series = series.resample("10s", origin=series.index[0]).mean()
        #     series = series.interpolate(method="time")

        # print(series)
        # print(series.info(verbose=True))

        return series

    def get_topic_interval(
        self,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
        exposures: list[dict],
        visits: list[dict],
    ) -> list[astropy.time.Time]:
        """
        Get the topic interval based on the given start and end times,
        exposures, and visits.

        Args:
            start_time (astropy.time.Time): The start time of the interval.
            end_time (astropy.time.Time): The end time of the interval.
            exposures (list[dict]): A list of exposure dictionaries.
            visits (list[dict]): A list of visit dictionaries.

        Returns:
            list[astropy.time.Time]: A list containing the minimum and maximum
                                     topic times.
        """

        min_topic_time = start_time
        max_topic_time = end_time

        for exposure in exposures:
            if exposure["timespan"].end < end_time:
                min_topic_time = min(exposure["timespan"].begin, min_topic_time)
                max_topic_time = max(exposure["timespan"].begin, max_topic_time)

        for visit in visits:
            if visit["timespan"].end < end_time:
                min_topic_time = min(visit["timespan"].begin, min_topic_time)
                max_topic_time = max(visit["timespan"].begin, max_topic_time)

        return [min_topic_time, max_topic_time]
