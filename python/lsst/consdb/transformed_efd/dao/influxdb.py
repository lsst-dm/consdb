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

"""Provides the `InfluxDBClient` and `InfluxDbDao` classes.

These classes support operations such as querying time-series data, retrieving
field keys, and unpacking packed dataframes.
"""

import itertools
import logging
import math
import os
from functools import partial
from urllib.parse import urljoin

import astropy.time
import numpy as np
import pandas as pd
import requests
from astropy.time import Time

# from lsst_efd_client.auth_helper import NotebookAuth


class InfluxDBClient:
    """A InfluxDB client.

    Parameters
    ----------
    url : str
        The URL of the InfluxDB API.
    database_name : str
        The name of the database to query.
    username : str, optional
        The username to authenticate with.
    password : str, optional
        The password to authenticate with.

    """

    def __init__(
        self,
        url: str,
        database_name: str,
        username: str | None = None,
        password: str | None = None,
        logger: logging.Logger = None,
        max_fields_per_query: int = 100,
    ) -> None:
        """Initialize the InfluxDBClient class.
        Parameters
        ----------
        url : str
            The URL of the InfluxDB API.
        database_name : str
            The name of the database to query.
        username : str, optional
            The username to authenticate with.
        password : str, optional
            The password to authenticate with.
        logger : logging.Logger, optional
            A logger instance for logging messages.
        max_fields_per_query : int, optional
            The maximum number of fields to include in a single InfluxDB query
            to avoid complexity errors. Defaults to 100.
        """
        self.url = url
        self.database_name = database_name
        self.auth = (username, password) if username and password else None
        # Ensure self.log is always a valid logger to prevent crashes.
        self.log = logger or logging.getLogger(__name__)
        self.max_fields_per_query = max_fields_per_query

    def query(self, query: str) -> dict:
        """Send a query to the InfluxDB API and retrieve the result.

        Parameters
        ----------
        query : `str`
            The query string to be executed on the InfluxDB database.

        Returns
        -------
        response : `dict`
            A dictionary containing the JSON response from the InfluxDB API.

        Raises
        ------
        Exception
            If an error occurs during the request to the InfluxDB API.

        """
        params = {"db": self.database_name, "q": query}
        try:
            response = requests.get(f"{self.url}/query", params=params, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            self.log.error(f"Request failed: url={self.url}/query params={params} error={exc}", exc_info=True)
            raise Exception(f"An error occurred: error={exc}") from exc

    def get_fields(self, topic_name):
        """Retrieves field keys for a topic from the InfluxDB database.

        Parameters
        ----------
        topic_name : str
            The name of the topic to query for field keys.

        Returns
        -------
        list or None
            A list of field keys if successful, or None if an error occurs.

        """
        try:
            # data = self.query(f'SHOW FIELD KEYS FROM "{topic_name}"')
            data = self.query(f'SHOW FIELD KEYS FROM "{self.database_name}"."autogen"."{topic_name}" ')
            field_keys = []
            if "results" in data:
                for result in data["results"]:
                    if "series" in result:
                        for series in result["series"]:
                            if "values" in series:
                                for value in series["values"]:
                                    field_keys.append(value[0])
            return field_keys
        except Exception as e:
            self.log.error(f"Error fetching topic fields: topic={topic_name} error={e}")
            return None

    def _make_fields(self, fields, base_fields):
        """Construct dictionary of fields grouped by their base field names.

        This function was adapted from the original implementation found at
        [https://github.com/lsst-sqre/lsst-efd-client.git]. The core logic
        remains consistent with the original, but modifications might have been
        made to better align with our specific use case and requirements.
        Original source:
        [https://github.com/lsst-sqre/lsst-efd-client/blob/main/src/lsst_efd_client/efd_helper.py#L274]

        Parameters
        ----------
        fields : list
            A list of all field names to process.
        base_fields : list
            A list of base field names to use for grouping.

        Returns
        -------
        tuple
            A tuple containing the dictionary of grouped fields and the number
            of grouped fields.

        """
        ret = {}
        n = None
        for bfield in base_fields:
            for f in fields:
                if f.startswith(bfield) and f[len(bfield) :].isdigit():  # Check prefix is complete
                    ret.setdefault(bfield, []).append(f)
            if n is None:
                n = len(ret[bfield])
            if n != len(ret[bfield]):
                raise ValueError(f"Field lengths do not agree for " f"{bfield}: {n} vs. {len(ret[bfield])}")

            def sorter(prefix, val):
                return int(val[len(prefix) :])

            part = partial(sorter, bfield)
            ret[bfield].sort(key=part)
        return ret, n

    def make_fields(self, fields: str, base_fields: [str, bytes]):
        """Construct a list of fields based on provided base field names.

        This function was adapted from the original implementation found at
        [https://github.com/lsst-sqre/lsst-efd-client.git]. The core logic
        remains consistent with the original, but modifications might have been
        made to better align with our specific use case and requirements.
        Original source:
        [https://github.com/lsst-sqre/lsst-efd-client/blob/main/src/lsst_efd_client/efd_helper.py#L301]

        Parameters
        ----------
        fields : str
            A string representing all fields.
        base_fields : str or bytes
            The base field name(s) to expand.

        Returns
        -------
        list
            A list of expanded field names.

        """
        if isinstance(base_fields, str):
            base_fields = [
                base_fields,
            ]
        elif isinstance(base_fields, bytes):
            base_fields = base_fields.decode()
            base_fields = [
                base_fields,
            ]
        qfields, els = self._make_fields(fields, base_fields)
        field_list = []
        for k in qfields:
            field_list += qfields[k]
        return field_list

    def _merge_packed_time_series(
        self,
        packed_dataframe,
        base_field,
        stride=1,
        ref_timestamp_col="cRIO_timestamp",
        fmt="unix_tai",
        scale="tai",
    ):
        """Select and unpack fields that are time samples into a dataframe.

        This function was adapted from the original implementation found at
        [https://github.com/lsst-sqre/lsst-efd-client.git]. The core logic
        remains consistent with the original, but modifications might have been
        made to better align with our specific use case and requirements.
        Original source:
        [https://github.com/lsst-sqre/lsst-efd-client/blob/main/src/lsst_efd_client/efd_utils.py#L22]

        Parameters
        ----------
        packed_dataframe : `pandas.DataFrame`
            packed data frame containing the desired data
        base_field :  `str`
            Base field name that will be expanded to query all
            vector entries.
        stride : `int`, optional
            Only use every stride value when unpacking. Must be a factor
            of the number of packed values. (1 by default)
        ref_timestamp_col : `str`, optional
            Name of the field name to use to assign timestamps to unpacked
            vector fields (default is 'cRIO_timestamp').
        fmt : `str`, optional
            Format to give to the `astropy.time.Time` constructor. Defaults to
            'unix_tai' since most internal timestamp columns are in TAI.
        scale : `str`, optional
            Time scale to give to the `astropy.time.Time` constructor.
            Defaults to 'tai'.

        Returns
        -------
        result : `pandas.DataFrame`
            A `pandas.DataFrame` containing the results of the query.

        """
        packed_fields = [
            k for k in packed_dataframe.keys() if k.startswith(base_field) and k[len(base_field) :].isdigit()
        ]
        packed_fields = sorted(packed_fields, key=lambda k: int(k[len(base_field) :]))  # sort by pack ID
        npack = len(packed_fields)
        if npack % stride != 0:
            raise RuntimeError(
                "Stride must be a factor of the number of packed fields: " f"{stride} v. {npack}"
            )
        packed_len = len(packed_dataframe)
        n_used = npack // stride  # number of raw fields being used
        output = np.empty(n_used * packed_len)
        times = np.empty_like(output, dtype=packed_dataframe[ref_timestamp_col].iloc[0])

        if packed_len == 1:
            dt = 0
        else:
            dt = (
                packed_dataframe[ref_timestamp_col].iloc[1] - packed_dataframe[ref_timestamp_col].iloc[0]
            ) / npack
        for i in range(0, npack, stride):
            i0 = i // stride
            output[i0::n_used] = packed_dataframe[f"{base_field}{i}"]
            times[i0::n_used] = packed_dataframe[ref_timestamp_col] + i * dt

        # Convert times to astropy Time and then to pandas timestamps in UTC
        timestamps = Time(times, format=fmt, scale=scale)
        result = pd.DataFrame({base_field: output, "time": times})
        result["time"] = pd.to_datetime(timestamps.utc.iso, errors="coerce", utc=True)

        # Set time as index and ensure index is timezone-aware
        result = result.set_index(result["time"]).drop("time", axis=1)
        if result.index.tzinfo is None:
            result.index = result.index.tz_localize("UTC")

        return result

    def merge_packed_time_series(
        self,
        result,
        base_fields,
        ref_timestamp_col="cRIO_timestamp",
        ref_timestamp_fmt="unix_tai",
        ref_timestamp_scale="tai",
    ):
        """Merge packed time series data into a single DataFrame.

        This function was adapted from the original implementation found at
        [https://github.com/lsst-sqre/lsst-efd-client.git]. The core logic
        remains consistent with the original, but modifications might have been
        made to better align with our specific use case and requirements.
        Original source:
        [https://github.com/lsst-sqre/lsst-efd-client/blob/main/src/lsst_efd_client/efd_helper.py#L319]

        Parameters
        ----------
        result : `pandas.DataFrame`
            The DataFrame containing the packed data.
        base_fields : `list`
            Base field name(s) that will be expanded to query all
            vector entries.
        ref_timestamp_col : `str`, optional
            Name of the field name to use to assign timestamps to unpacked
            vector fields (default is 'cRIO_timestamp').
        ref_timestamp_fmt : `str`, optional
            Format to use for translating `ref_timestamp_col` values.
            Defaults to 'unix_tai'.
        ref_timestamp_scale : `str`, optional
            Time scale to use in translating `ref_timestamp_col` values.
            Defaults to 'tai'.

        Returns
        -------
        result : `pandas.DataFrame`
            A `pandas.DataFrame` containing the merged time series data.

        """
        if result.empty:
            return result

        vals = {}
        try:
            for f in base_fields[0:3]:
                # Ensure the helper function merge_packed_time_series is
                # correctly defined and imported
                df = self._merge_packed_time_series(
                    result,
                    f,
                    ref_timestamp_col=ref_timestamp_col,
                    fmt=ref_timestamp_fmt,
                    scale=ref_timestamp_scale,
                )
                vals[f] = df[f]
            # vals.update({"times": df["times"]})
            return pd.DataFrame(vals, index=df.index)
        except Exception as e:
            self.log.error(f"Error merging field: field={f} error={e}")
            raise

    def _convert_index_format(self, x):
        if pd.notna(x):
            return x.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            return x

    def _to_dataframe(self, response: dict) -> pd.DataFrame:
        """Convert an InfluxDB query response to a Pandas DataFrame.

        Parameters
        ----------
        response : `dict`
            The JSON response from the InfluxDB API, containing the results
            of the query.

        Returns
        -------
        result : `pandas.DataFrame`
            A DataFrame containing the queried data. The DataFrame's index
            is set to the timestamp of each record if available, and
            localized to UTC if not already time-zone aware. Additional
            tags or metadata from the response are added as columns to the
            DataFrame.

        Raises
        ------
        KeyError
            If the response does not contain the expected structure.

        """
        # One query submitted at a time
        statement = response["results"][0]
        # One topic queried at a time
        series = statement["series"][0]
        result = pd.DataFrame(series.get("values", []), columns=series["columns"])

        if "time" not in result.columns:
            return result

        # Convert the "time" column to datetime objects and fix inconsistencies
        # in datetime iso format
        result["time"] = pd.to_datetime(result["time"], errors="coerce", utc=True).apply(
            self._convert_index_format
        )
        result = result.set_index(result["time"]).drop("time", axis=1)
        # Convert the index to a DatetimeIndex
        result.index = pd.to_datetime(result.index, errors="coerce", utc=True)
        # Ensure the index is timezone-aware
        if result.index.tzinfo is None:
            result.index = result.index.tz_localize("UTC")
        # Add tags if present
        if "tags" in series:
            for k, v in series["tags"].items():
                result[k] = v
        # Set the name if present
        if "name" in series:
            result.name = series["name"]

        return result

    def build_time_range_query(
        self,
        topic_name,
        fields,
        start,
        end,
        index=None,
        use_old_csc_indexing=False,
        aggregate_interval: str | None = None,
        aggregate_func: str | None = None,
    ):
        """Build a query based on a time range, with optional aggregation.

        Parameters
        ----------
        topic_name : `str`
            Name of topic for which to build a query.
        fields :  `str` or `list`
            Name of field(s) to query.
        start : `astropy.time.Time`
            Start time of the time range.
        end : `astropy.time.Time`
            End time of the range either as an absolute time.
        index : `int`, optional
            When index is used, add an 'AND salIndex = index' to the query.
            (default is `None`).
        use_old_csc_indexing: `bool`, optional
            When index is used, add an 'AND {CSCName}ID = index' to the query
            which is the old CSC indexing name.
            (default is `False`).
        aggregate_interval : `str`, optional
            If set, groups the results into time buckets of this duration
            (e.g.,"1s", "5m", "1h"). Requires `aggregate_func` to be set.
            (default is `None`).
        aggregate_func : `str`, optional
            If set, applies an aggregation function to the fields within each
            time bucket. Supported values are 'mean', 'max', and 'min'.
            (default is `None`).

        Returns
        -------
        query : `str`
            A string containing the constructed query statement.

        Raises
        ------
        ValueError
            If inputs are invalid, such as providing `aggregate_interval`
            without `aggregate_func` or an unsupported function name.
        TypeError
            If time arguments are not `astropy.time.Time` objects.
        """
        if not isinstance(start, Time):
            raise TypeError("The first time argument must be a time stamp")
        if not start.scale == "utc":
            raise ValueError("Timestamps must be in UTC.")
        elif isinstance(end, Time):
            if not end.scale == "utc":
                raise ValueError("Timestamps must be in UTC.")
            start_str = start.isot
            end_str = end.isot
        else:
            raise TypeError("The second time argument must be the time stamp for the end " "or a time delta.")

        index_str = ""
        if index:
            if use_old_csc_indexing:
                parts = topic_name.split(".")
                index_name = f"{parts[-2]}ID"  # The CSC name is always the penultimate
            else:
                index_name = "salIndex"
            index_str = f" AND {index_name} = {index}"

        # Ensure fields is a list for consistent processing
        if isinstance(fields, str):
            fields = [fields]
        elif isinstance(fields, bytes):
            fields = [fields.decode()]

        select_clause = ""
        # Build SELECT clause based on aggregation parameters
        if aggregate_interval and aggregate_func:
            # Standard aggregations: mean, max, min
            valid_funcs = ["mean", "max", "min"]
            if aggregate_func.lower() not in valid_funcs:
                raise ValueError(f"aggregate_func must be one of {valid_funcs}")
            # Use AS to keep original column names in the result
            select_fields = [f'{aggregate_func.upper()}("{f}") AS "{f}"' for f in fields]
            select_clause = f'SELECT {", ".join(select_fields)}'
        elif aggregate_interval and not aggregate_func:
            raise ValueError("aggregate_func must be provided if aggregate_interval is set.")
        else:
            # Original behavior: select raw, un-aggregated fields
            select_clause = f'SELECT {", ".join(f'"{f}"' for f in fields)}'

        # Build GROUP BY clause if aggregation is enabled
        group_by_clause = ""
        if aggregate_interval:
            group_by_clause = f" GROUP BY time({aggregate_interval})"

        # influxdb demands last Z
        timespan = f"time >= '{start_str}Z' AND time <= '{end_str}Z'{index_str}"

        # Build the final query
        return (
            f"{select_clause} "
            f'FROM "{self.database_name}"."autogen"."{topic_name}" '
            f"WHERE {timespan}"
            f"{group_by_clause}"
        )

    def _execute_single_timeseries_query(
        self,
        topic_name: str,
        fields: list,
        start: astropy.time.Time,
        end: astropy.time.Time,
        index: int | None = None,
        use_old_csc_indexing: bool = False,
        aggregate_interval: str | None = None,
        aggregate_func: str | None = None,
    ) -> pd.DataFrame:
        """
        Executes a single time series query and returns a DataFrame.

        This is the core execution logic used by the public
        `select_time_series` method. It builds the query, executes
        it, and converts the response to a pandas DataFrame.

        Parameters
        ----------
        All parameters are identical to the public `select_time_series`
        method.

        Returns
        -------
        result : `pandas.DataFrame`
            A `~pandas.DataFrame` containing the results of the single query.
        """
        query = self.build_time_range_query(
            topic_name,
            fields,
            start,
            end,
            index,
            use_old_csc_indexing,
            aggregate_interval=aggregate_interval,
            aggregate_func=aggregate_func,
        )
        response = self.query(query)
        if "series" not in response["results"][0]:
            return pd.DataFrame()

        return self._to_dataframe(response)

    def select_time_series(
        self,
        topic_name: str,
        fields,
        start: astropy.time.Time,
        end: astropy.time.Time,
        index: int | None = None,
        use_old_csc_indexing: bool = False,
        aggregate_interval: str | None = None,
        aggregate_func: str | None = None,
    ):
        """Select time series data from InfluxDB based on a time range.
        This function queries specific fields from the InfluxDB database
        within a defined time range. It can optionally perform server-side
        aggregation.

        If the number of fields exceeds `self.max_fields_per_query`, the
        request is automatically split into smaller chunks and the results
        are concatenated.
        Parameters
        ----------
        topic_name : `str`
            Name of the topic to query.
        fields : `str` or `list`
            Name of the field(s) to query.
        start : `astropy.time.Time`
            Start time of the time range.
        end : `astropy.time.Time`
            End time of the range either as an absolute time.
        index : `int`, optional
            When index is used, add an 'AND salIndex = index' to the query.
            (default is `None`).
        use_old_csc_indexing: `bool`, optional
            When index is used, add an 'AND {CSCName}ID = index' to the query
            which is the old CSC indexing name.
            (default is `False`).
        aggregate_interval : `str`, optional
            If set, groups the results into time buckets of this duration
            (e.g., "1s", "5m", "1h"). Requires `aggregate_func` to be set.
            (default is `None`).
        aggregate_func : `str`, optional
            If set, applies an aggregation function to the fields within each
            time bucket. Supported values are 'mean', 'max', and 'min'.
            (default is `None`)

        Returns
        -------
        result : `pandas.DataFrame`
            A `~pandas.DataFrame` containing the results of the query.
        """
        if not isinstance(fields, list):
            fields = list(fields)

        # If the number of fields is within the limit, make a single call.
        if len(fields) <= self.max_fields_per_query:
            return self._execute_single_timeseries_query(
                topic_name,
                fields,
                start,
                end,
                index,
                use_old_csc_indexing,
                aggregate_interval=aggregate_interval,
                aggregate_func=aggregate_func,
            )

        # Otherwise, split the query into chunks and call the helper for each.
        self.log.info(
            f"Querying {len(fields)} fields for topic '{topic_name}', which exceeds the limit of "
            f"{self.max_fields_per_query}. Splitting into chunks."
        )

        all_series_dfs = []

        total_chunks = math.ceil(len(fields) / self.max_fields_per_query)
        field_chunks = itertools.batched(fields, self.max_fields_per_query)

        for i, chunk in enumerate(field_chunks):
            self.log.debug(f"Querying field chunk {i+1}/{total_chunks} ({len(chunk)} fields)...")
            try:
                df_chunk = self._execute_single_timeseries_query(
                    topic_name,
                    chunk,
                    start,
                    end,
                    index,
                    use_old_csc_indexing,
                    aggregate_interval=aggregate_interval,
                    aggregate_func=aggregate_func,
                )
                if not df_chunk.empty:
                    all_series_dfs.append(df_chunk)
            except Exception as e:
                self.log.error(f"Failed to query chunk {i+1} for topic {topic_name}: {e}", exc_info=True)

        if not all_series_dfs:
            self.log.warning(f"All query chunks for topic {topic_name} returned empty or failed.")
            return pd.DataFrame()

        # Concatenate all resulting dataframes horizontally and clean up.
        final_df = pd.concat(all_series_dfs, axis=1)
        final_df = final_df.loc[:, ~final_df.columns.duplicated()]
        return final_df

    def select_packed_time_series(
        self,
        topic_name,
        base_fields,
        start,
        end,
        index=None,
        ref_timestamp_col="cRIO_timestamp",
        ref_timestamp_fmt="unix_tai",
        ref_timestamp_scale="tai",
        use_old_csc_indexing=False,
    ):
        """Select and unpack fields that are time samples into a dataframe.

        This function was adapted from the original implementation found at
        [https://github.com/lsst-sqre/lsst-efd-client.git]. The core logic
        remains consistent with the original, but modifications might have been
        made to better align with our specific use case and requirements.
        Original source:
        [https://github.com/lsst-sqre/lsst-efd-client/blob/main/src/lsst_efd_client/efd_helper.py#L1081]

        Parameters
        ----------
        topic_name : `str`
            Name of topic to query.
        base_fields :  `str` or `list`
            Base field name(s) that will be expanded to query all
            vector entries.
        start : `astropy.time.Time`
            Start time of the time range, if ``is_window`` is specified,
            this will be the midpoint of the range.
        end : `astropy.time.Time` or `astropy.time.TimeDelta`
            End time of the range either as an absolute time or
            a time offset from the start time.
        is_window : `bool`, optional
            If set and the end time is specified as a
            `~astropy.time.TimeDelta`, compute a range centered on the start
            time (default is `False`).
        index : `int`, optional
            When index is used, add an 'AND salIndex = index' to the query.
            (default is `None`).
        ref_timestamp_col : `str`, optional
            Name of the field name to use to assign timestamps to unpacked
            vector fields (default is 'cRIO_timestamp').
        ref_timestamp_fmt : `str`, optional
            Format to use to translating ``ref_timestamp_col`` values
            (default is 'unix_tai').
        ref_timestamp_scale : `str`, optional
            Time scale to use in translating ``ref_timestamp_col`` values
            (default is 'tai').
        convert_influx_index : `bool`, optional
            Convert influxDB time index from TAI to UTC? This is for legacy
            instances that may still have timestamps stored internally as TAI.
            Modern instances all store index timestamps as UTC natively.
            Default is `False`, don't translate from TAI to UTC.
        use_old_csc_indexing: `bool`, optional
            When index is used, add an 'AND {CSCName}ID = index' to the query
            which is the old CSC indexing name.
            (default is `False`).

        Returns
        -------
        result : `pandas.DataFrame`
            A `~pandas.DataFrame` containing the results of the query.

        """
        fields = self.get_fields(topic_name)
        field_list = self.make_fields(fields, base_fields)
        result = self.select_time_series(
            topic_name,
            field_list
            + [
                ref_timestamp_col,
            ],
            start,
            end,
            index=index,
            use_old_csc_indexing=use_old_csc_indexing,
        )
        return self.merge_packed_time_series(
            result,
            base_fields,
            ref_timestamp_col,
            ref_timestamp_fmt,
            ref_timestamp_scale,
        )


class InfluxDbDao(InfluxDBClient):
    """A specialized extension of `InfluxDBClient`.

    This class provides streamlined access to EFD data, leveraging environment
    variables or a credentials service for authentication. It facilitates
    querying and managing time-series data with minimal configuration.

    Attributes
    ----------
    efd_name : str
        The name of the EFD instance to connect to.
    database_name : str
        The name of the InfluxDB database to query.
    creds_service : str
        The URL of the credentials service used for authentication.

    """

    def __init__(
        self,
        efd_name: str,
        database_name="efd",
        creds_service="https://roundtable.lsst.codes/segwarides/",
        max_fields_per_query: int = 100,
    ):
        """Initializes InfluxDbDao, extending the InfluxDBClient class.
        Parameters
        ----------
        efd_name : str
            The name of the EFD (Engineering and Facility Database) instance to
            connect to.
        database_name : str, optional
            The name of the InfluxDB database to use. Default is "efd".
        creds_service : str, optional
            The URL of the credentials service to use for authentication.
            Default is "https://roundtable.lsst.codes/segwarides/".
        max_fields_per_query : int, optional
            The maximum number of fields per query. Passed to the parent
            client. Default is 100.
        """
        # auth = NotebookAuth(service_endpoint=creds_service)
        # host, schema_registry_url, port, user,
        # password, path = auth.get_auth(efd_name)
        user = os.getenv("EFD_USERNAME", "efdreader")
        password = os.getenv("EFD_PASSWORD")
        host = os.getenv("EFD_HOST", "usdf-rsp.slac.stanford.edu")
        port = os.getenv("EFD_PORT", 443)
        path = os.getenv("EFD_PATH", "/influxdb-enterprise-data/")
        url = urljoin(f"https://{host}:{port}", f"{path}")

        # Call the parent constructor with all relevant parameters
        super().__init__(
            url,
            database_name=database_name,
            username=user,
            password=password,
            max_fields_per_query=max_fields_per_query,
        )
