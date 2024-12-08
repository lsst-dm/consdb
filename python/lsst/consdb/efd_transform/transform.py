import logging
from typing import Any, Dict, List, Union

import astropy.time
import numpy
import pandas
from dao.butler import ButlerDao
from dao.exposure_efd import ExposureEfdDao
from dao.exposure_efd_unpivoted import ExposureEfdUnpivotedDao
from dao.influxdb import InfluxDbDao
from dao.visit_efd import VisitEfdDao
from dao.visit_efd_unpivoted import VisitEfdUnpivotedDao
from lsst.daf.butler import Butler
from summary import Summary


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
        efd: InfluxDbDao,
        config: Dict[str, Any],
        logger: logging.Logger,
        commit_every: int = 100,
    ):
        """
        Initializes a new instance of the Transform class.

        Args:
            butler (Butler): The Butler object for accessing data.
            db_uri (str): The database connection string.
            efd (dao.InfluxDbDao): The EFD client for accessing
                EFD data.
            config (dict[str, Any]): The configuration for the
                transformation process.
            logger (logging.Logger): The logger object for logging
                messages.
            commit_every (int, optional): The number of records to commit
                to the database at once. Defaults to 100.
        """
        self.log = logger
        self.butler_dao = ButlerDao(butler)
        self.db_uri = db_uri
        self.efd = efd
        self.config = config
        self.commit_every = commit_every

        self.log.info("----------- Transform -----------")

    def get_schema_by_instrument(self, instrument: str) -> str:
        """
        Get the schema name for the given instrument.

        Args:
            instrument (str): The instrument name.

        Returns:
            str: The schema name.
        """
        schemas = {
            "LATISS": "cdb_latiss",
            "LSSTComCam": "cdb_lsstcomcam",
            "LSSTComCamSim": "cdb_lsstcomcamsim",
        }
        return schemas[instrument]

    def process_interval(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> Dict[str, int]:
        """
        Process the given time interval for a specific instrument.

        Args:
            instrument (str): The instrument name.
            start_time (astropy.time.Time): The start time of the interval.
            end_time (astropy.time.Time): The end time of the interval.
        """
        count = {"exposures": 0, "visits1": 0, "exposures_unpivoted": 0, "visits1_unpivoted": 0}

        self.log.info(f"Proccessing interval {start_time} - {end_time}")

        # Retrieves all exposures for the period
        exposures = self.butler_dao.exposures_by_period(instrument, start_time, end_time)

        self.log.info(f"Exposures: {len(exposures)}")

        # Retrieves all visits for the period
        visits = self.butler_dao.visits_by_period(instrument, start_time, end_time)

        self.log.info(f"Visits: {len(visits)}")

        if len(exposures) == 0 and len(visits) == 0:
            self.log.info("No exposures or visits found for the period.")
            return count

        # Identifies the period that will be used to consult the topics
        topic_interval = self.get_topic_interval(start_time, end_time, exposures, visits)
        self.log.info(f"Topic interval: {topic_interval[0]} - {topic_interval[1]}")

        result_exp = {}
        for exposure in exposures:
            result_exp[exposure["id"]] = {
                "exposure_id": exposure["id"],
                "instrument": instrument,
            }

        result_exp_unpivoted = []

        result_vis = {}
        for visit in visits:
            result_vis[visit["id"]] = {
                "visit_id": visit["id"],
                "instrument": instrument,
            }

        result_vis_unpivoted = []

        # map all topics and fields to perform a single query per topic
        # map all topics and fields to perform a single query per topic
        topics_columns_map = {}
        for column in self.config["columns"]:
            for values in column["topics"]:
                topic = values["name"]
                if topic not in topics_columns_map.keys():
                    topics_columns_map[topic] = {
                        "name": topic,
                        "fields": [],
                        "packed_series": [],
                        "columns": [],
                    }
                for field in values["fields"]:
                    topics_columns_map[topic]["fields"].append(field["name"])

                # remove duplicate fields per topic
                topics_columns_map[topic]["fields"] = list(set(topics_columns_map[topic]["fields"]))

                # Append packed_series to the list
                topics_columns_map[topic]["packed_series"].append(column["packed_series"])
                topics_columns_map[topic]["columns"].append(column)

            # Add a new key to store if any series is packed
            topics_columns_map[topic]["is_packed"] = any(topics_columns_map[topic]["packed_series"])

        # Iterates over topic to perform the transformation
        for key, topic in topics_columns_map.items():
            # query the topic
            self.log.info(f"Querying the Topic: {topic['name']}")
            topic_series = self.get_efd_values(topic, topic_interval, topic["is_packed"])

            # process the columns in that topic:
            for column in topic["columns"]:
                # self.log.debug(column)
                self.log.info(f"Proccessing Column: {column['name']}")
                # get fields
                if not topic_series.empty:
                    fields = [f["name"] for f in column["topics"][0]["fields"]]
                    if column["subset_field"]:
                        subset_field = str(column["subset_field"])
                        subset_value = str(column["subset_value"])

                        if subset_field in topic_series and not topic_series[subset_field].empty:
                            # Ensure both the column and subset_value are of the same type
                            topic_series[subset_field] = topic_series[subset_field].fillna("").astype(str)
                            subset_value = str(subset_value)

                            # Filter the DataFrame
                            filtered_df = topic_series.loc[topic_series[subset_field] == subset_value]

                            # Verify which fields exist in the filtered DataFrame
                            fields.remove(subset_field)
                            valid_fields = [field for field in fields if field in filtered_df.columns]

                            if valid_fields:
                                data = [
                                    {"topic": topic["name"], "series": filtered_df[valid_fields].dropna()}
                                ]
                            else:
                                self.log.warning(
                                    f"No valid fields found in filtered DataFrame for topic: {topic['name']}"
                                )
                                data = [{"topic": topic["name"], "series": pandas.DataFrame()}]
                        else:
                            data = [{"topic": topic["name"], "series": pandas.DataFrame()}]
                    else:
                        data = [{"topic": topic["name"], "series": topic_series[fields].dropna()}]

                    if "exposure_efd" in column["tables"]:
                        for exposure in exposures:
                            function_kwargs = column["function_args"] or {}
                            column_value = self.proccess_column_value(
                                start_time=exposure["timespan"].begin.utc,
                                end_time=exposure["timespan"].end.utc,
                                topics=data,
                                transform_function=column["function"],
                                **function_kwargs,
                            )

                            result_exp[exposure["id"]][column["name"]] = column_value

                    if "exposure_efd_unpivoted" in column["tables"]:
                        for exposure in exposures:
                            function_kwargs = column["function_args"] or {}
                            series_df = data[0]["series"]

                            for col in series_df.columns:
                                new_topic = topic.copy()
                                new_topic["fields"] = [col]
                                new_topic["columns"][0]["topics"][0]["fields"] = [{"name": col}]
                                new_data = [{"topic": new_topic, "series": series_df[[col]]}]

                                # Safeguard processing
                                column_value = self.proccess_column_value(
                                    start_time=getattr(exposure["timespan"].begin, "utc", None),
                                    end_time=getattr(exposure["timespan"].end, "utc", None),
                                    topics=new_data,
                                    transform_function=column.get("function"),
                                    **function_kwargs,
                                )

                                # if col == 'annularZernikeCoeff0':
                                #     print('*'.center(80, '*'))
                                #     print(column_value)
                                #     print(series_df[[col]])
                                #     print('*'.center(80, '*'))
                                # print(new_data)

                                # Append the processed result to the result_exp_unpivoted list
                                if column_value:
                                    result_exp_unpivoted.append(
                                        {
                                            "exposure_id": exposure["id"],
                                            "topic": column["name"],
                                            "column": col,
                                            "value": column_value,
                                        }
                                    )

                    if "visit1_efd" in column["tables"]:
                        for visit in visits:
                            function_kwargs = column["function_args"] or {}
                            column_value = self.proccess_column_value(
                                start_time=visit["timespan"].begin.utc,
                                end_time=visit["timespan"].end.utc,
                                topics=data,
                                transform_function=column["function"],
                                **function_kwargs,
                            )

                            result_vis[visit["id"]][column["name"]] = column_value

                    if "visit1_efd_unpivoted" in column["tables"]:
                        for visit in visits:
                            function_kwargs = column["function_args"] or {}
                            series_df = data[0]["series"]

                            for col in series_df.columns:
                                new_topic = topic.copy()
                                new_topic["fields"] = [col]
                                new_topic["columns"][0]["topics"][0]["fields"] = [{"name": col}]
                                new_data = [{"topic": new_topic, "series": series_df[[col]]}]

                                column_value = self.proccess_column_value(
                                    start_time=getattr(visit["timespan"].begin, "utc", None),
                                    end_time=getattr(visit["timespan"].end, "utc", None),
                                    topics=new_data,
                                    transform_function=column.get("function"),
                                    **function_kwargs,
                                )
                                if column_value:
                                    result_vis_unpivoted.append(
                                        {
                                            "visit_id": visit["id"],
                                            "topic": topic,
                                            "column": col,
                                            "value": column_value,
                                        }
                                    )
        # ingesting exposure
        results = []
        for result_row in result_exp:
            results.append(result_exp[result_row])

        df_exposures = pandas.DataFrame(results)

        if not df_exposures.empty:
            self.log.info(f"Exposure results to be inserted into the database: {len(df_exposures)}")
            exp_dao = ExposureEfdDao(db_uri=self.db_uri, schema=self.get_schema_by_instrument(instrument))
            affected_rows = exp_dao.upsert(df=df_exposures, commit_every=self.commit_every)
            count["exposures"] = affected_rows
            self.log.info(f"Database rows affected: {affected_rows}")
        del results

        # ingesting exposure_unpivoted
        df_exposures_unpivoted = pandas.DataFrame(result_exp_unpivoted)
        # print(df_exposures_unpivoted)
        self.log.info(
            f"Exposure unpivoted results to be inserted into the database: {len(df_exposures_unpivoted)}"
        )
        if not df_exposures_unpivoted.empty:
            exp_unpivoted_dao = ExposureEfdUnpivotedDao(
                db_uri=self.db_uri, schema=self.get_schema_by_instrument(instrument)
            )
            affected_rows = exp_unpivoted_dao.upsert(
                df=df_exposures_unpivoted, commit_every=self.commit_every
            )
            count["exposures_unpivoted"] = affected_rows
            self.log.info(f"Database rows affected: {affected_rows}")
        # del result_exp_unpivoted

        # ingesting visit
        results = []
        for result_row in result_vis:
            results.append(result_vis[result_row])

        df_visits = pandas.DataFrame(results)
        if not df_visits.empty:
            self.log.info(f"Visit results to be inserted into the database: {len(df_visits)}")
            vis_dao = VisitEfdDao(db_uri=self.db_uri, schema=self.get_schema_by_instrument(instrument))
            affected_rows = vis_dao.upsert(df=df_visits, commit_every=self.commit_every)
            self.log.info(f"Database rows affected: {affected_rows}")
            count["visits1"] = affected_rows
        del results

        # ingesting visit_unpivoted
        df_visits_unpivoted = pandas.DataFrame(result_vis_unpivoted)
        self.log.info(f"Visit unpivoted results to be inserted into the database: {len(df_visits_unpivoted)}")
        if not df_visits_unpivoted.empty:
            vis_unpivoted_dao = VisitEfdUnpivotedDao(
                db_uri=self.db_uri, schema=self.get_schema_by_instrument(instrument)
            )
            affected_rows = vis_unpivoted_dao.upsert(df=df_visits_unpivoted, commit_every=self.commit_every)
            self.log.info(f"Database rows affected: {affected_rows}")
            count["visits1_unpivoted"] = affected_rows
        # del result_vis_unpivoted

        return count

    def proccess_column_value(
        self,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
        topics,
        transform_function,
        **function_kwargs,
    ) -> Any:
        """
        Process the column value for a given time range and topics using an
        aggregation function.

        Args:
            start_time (astropy.time.Time): The start time of the time range.
            end_time (astropy.time.Time): The end time of the time range.
            topics: The topics to retrieve values from.
            transform_function: The function to apply to the values.
            **function_kwargs: Additional keyword arguments to pass to the
              transform function.

        Returns:
            The processed column value.
        """

        values = self.topic_values_by_exposure(start_time, end_time, topics)

        if not values.empty:
            column_value = Summary(values).apply(transform_function, **function_kwargs)
            return column_value

        return None

    def topic_values_by_exposure(
        self, start_time: astropy.time.Time, end_time: astropy.time.Time, topics
    ) -> pandas.DataFrame:
        """
        Retrieve topic values for a given time range.

        Args:
            start_time (astropy.time.Time): The start time of the range.
            end_time (astropy.time.Time): The end time of the range.
            topics (list): A list of topics.

        Returns:
            pandas.DataFrame: A DataFrame containing the topic values for the
                              given time range, or an empty DataFrame if no
                              values match.
        """

        start_time = pandas.Timestamp(start_time.to_datetime(), tz="UTC")
        end_time = pandas.Timestamp(end_time.to_datetime(), tz="UTC")

        topics_values = []

        for topic in topics:
            topic_table = topic["series"]
            if not topic_table.empty:
                values = topic_table.loc[(topic_table.index > start_time) & (topic_table.index < end_time)]
                if not values.empty:
                    topics_values.append(values)

        # Concatenate the list of DataFrames or return an empty DataFrame if
        # the list is empty
        if topics_values:
            result = pandas.concat(topics_values)
        else:
            result = pandas.DataFrame()  # Return an empty DataFrame

        return result

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

    def topics_by_column(self, column, topic_interval, packed_series) -> List[dict]:
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
            topic_series = self.get_efd_values(topic, topic_interval, packed_series)
            data.append({"topic": topic["name"], "series": topic_series})
            self.log.debug(f"EFD Topic {topic['name']} return {len(topic_series)} rows")

        return data

    def get_efd_values(
        self, topic: Dict[str, Any], topic_interval: List[astropy.time.Time], packed_series: bool = False
    ) -> pandas.DataFrame:

        start = topic_interval[0].utc  # Start time of the interval in UTC
        end = topic_interval[1].utc  # End time of the interval in UTC
        window = astropy.time.TimeDelta(
            topic.get("window", 0.0), format="sec"
        )  # Time window around the interval

        fields = [f for f in topic["fields"]]  # List of field names to query

        # Define the chunk size for querying to manage large numbers of fields
        chunk_size = 100  # Adjust as necessary based on system capabilities
        chunks = [fields[i : i + chunk_size] for i in range(0, len(fields), chunk_size)]
        # Split the fields into smaller lists (chunks) to avoid querying too
        # many fields at once

        all_series = []  # List to collect DataFrames from each chunk

        for chunk in chunks:
            try:
                if packed_series:
                    # Query packed time series for the current chunk of fields
                    series = self.efd.select_packed_time_series(
                        topic["name"], chunk, start - window, end + window, ref_timestamp_scale="utc"
                    )
                else:
                    # Query regular time series for the current chunk of fields
                    series = self.efd.select_time_series(
                        topic["name"],
                        chunk,
                        start - window,
                        end + window,
                    )
                if not series.empty:
                    all_series.append(series)  # Append the result to the list
                    # only if not empty
            except Exception as e:
                # Log any errors encountered during querying
                self.log.warning(f"An unexpected error occurred: {e}")
                # Optional: you might want to include a placeholder DataFrame
                # with the same columns here if needed

        if all_series:
            # Concatenate all collected DataFrames into a single DataFrame if
            # any results were collected
            combined_series = pandas.concat(all_series, axis=1)
        else:
            # Return an empty DataFrame if no data was collected
            combined_series = pandas.DataFrame()

        return combined_series

    def get_topic_interval(
        self,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
        exposures: List[dict],
        visits: List[dict],
    ) -> List[astropy.time.Time]:
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
