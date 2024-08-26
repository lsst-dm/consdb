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
    ) -> None:
        """
        Initialize the InfluxDBClient class.

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
        self.url = url
        self.database_name = database_name
        self.auth = (username, password) if username and password else None

    def query(self, query: str) -> dict:
        """
        Send a query to the InfluxDB API and retrieve the result.

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
            raise Exception(f"An error occurred: {exc}") from exc

    def get_fields(self, topic_name):
        """
        Retrieve the field keys for a given topic from the InfluxDB database.

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
            print(f"Error occurred while fetching fields for topic {topic_name}: {e}")
            return None

    def _make_fields(self, fields, base_fields):
        """
        Helper method to construct a dictionary of fields grouped by their base
        field names.

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
                raise ValueError(f"Field lengths do not agree for {bfield}: {n} vs. {len(ret[bfield])}")

            def sorter(prefix, val):
                return int(val[len(prefix) :])

            part = partial(sorter, bfield)
            ret[bfield].sort(key=part)
        return ret, n

    def make_fields(self, fields: str, base_fields: [str, bytes]):
        """
        Construct a list of fields based on provided base field names.

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
        """Select fields that are time samples and unpack them into a
        dataframe.

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

        timestamps = Time(times, format=fmt, scale=scale)
        return pd.DataFrame({base_field: output, "times": times}, index=timestamps.utc.datetime64)

    def merge_packed_time_series(
        self,
        result,
        base_fields,
        ref_timestamp_col="cRIO_timestamp",
        ref_timestamp_fmt="unix_tai",
        ref_timestamp_scale="tai",
    ):
        """
        Merge packed time series data into a single DataFrame.

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
            vals.update({"times": df["times"]})
            return pd.DataFrame(vals, index=df.index)
        except Exception as e:
            print(f"Error occurred while merging field {f}: {e}")
            raise

    def _to_dataframe(self, response: dict) -> pd.DataFrame:
        """
        Convert an InfluxDB query response to a Pandas DataFrame.

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

        # Convert the "time" column to datetime objects
        result["time"] = pd.to_datetime(result["time"], errors="coerce", utc=True)

        # Define a lambda function to convert datetime to the desired format
        convert_index_format = lambda x: x.strftime("%Y-%m-%dT%H:%M:%S.%f%z") if pd.notna(x) else x

        # Apply the lambda function to format the index
        result_index = result["time"].map(lambda x: convert_index_format(x))

        # Set the formatted index
        result = result.set_index(result_index).drop("time", axis=1)

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

    def build_time_range_query(self, topic_name, fields, start, end, index=None, use_old_csc_indexing=False):
        """Build a query based on a time range.

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

        Returns
        -------
        query : `str`
            A string containing the constructed query statement.
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
        timespan = f"time >= '{start_str}Z' AND time <= '{end_str}Z'{index_str}"  # influxdb demands last Z

        if isinstance(fields, str):
            fields = [
                fields,
            ]
        elif isinstance(fields, bytes):
            fields = fields.decode()
            fields = [
                fields,
            ]

        # Build query here
        return (
            f'SELECT {", ".join(fields)} FROM "{self.database_name}"."autogen"."{topic_name}" '
            f"WHERE {timespan}"
        )

    def select_time_series(
        self,
        topic_name,
        fields,
        start: astropy.time.Time,
        end: astropy.time.Time,
        index=None,
        use_old_csc_indexing=False,
    ):
        """
        Select time series data from InfluxDB based on a time range.

        This function queries specific fields from the InfluxDB database
        within a defined time range.

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

        Returns
        -------
        result : `pandas.DataFrame`
            A `~pandas.DataFrame` containing the results of the query.
        """
        query = self.build_time_range_query(topic_name, fields, start, end, index, use_old_csc_indexing)
        response = self.query(query)

        if "series" not in response["results"][0]:
            return pd.DataFrame()

        return self._to_dataframe(response)

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
        """Select fields that are time samples and unpack them into a
        dataframe.

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

    def __init__(
        self, efd_name: str, database_name="efd", creds_service="https://roundtable.lsst.codes/segwarides/"
    ):
        """
        Initialize the InfluxDbDao class, which extends the InfluxDBClient
        class.

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
        """
        # auth = NotebookAuth(service_endpoint=creds_service)
        # host, schema_registry_url, port, user,
        # password, path = auth.get_auth(efd_name)

        user = os.getenv("EFD_USERNAME", "efdreader")
        password = os.getenv("EFD_PASSWORD")
        # database_name=os.getenv("EFD_DATABASE", "efd")
        host = os.getenv("EFD_HOST", "usdf-rsp.slac.stanford.edu")
        port = os.getenv("EFD_PORT", 443)
        path = os.getenv("EFD_PATH", "/influxdb-enterprise-data/")

        url = urljoin(f"https://{host}:{port}", f"{path}")

        super(InfluxDbDao, self).__init__(url, database_name=database_name, username=user, password=password)
