from urllib.parse import urljoin

import astropy.time
import pandas as pd
import requests
from astropy.time import Time
from lsst_efd_client.auth_helper import NotebookAuth


class InfluxDBClient:
    """A simple InfluxDB client.

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
        self.url = url
        self.database_name = database_name
        self.auth = (username, password) if username and password else None

    def query(self, query: str) -> dict:
        """Send a query to the InfluxDB API."""

        params = {"db": self.database_name, "q": query}
        try:
            response = requests.get(f"{self.url}/query", params=params, auth=self.auth)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise Exception(f"An error occurred: {exc}") from exc

    def _to_dataframe(self, response: dict) -> pd.DataFrame:
        """Convert an InfluxDB response to a Pandas dataframe.

        Parameters
        ----------
        response : dict
            The JSON response from the InfluxDB API.
        """
        # One query submitted at a time
        statement = response["results"][0]
        # One topic queried at a time
        series = statement["series"][0]
        result = pd.DataFrame(series.get("values", []), columns=series["columns"])
        if "time" not in result.columns:
            return result
        result = result.set_index(pd.to_datetime(result["time"])).drop("time", axis=1)
        if result.index.tzinfo is None:
            result.index = result.index.tz_localize("UTC")
        if "tags" in series:
            for k, v in series["tags"].items():
                result[k] = v
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
            f'WHERE {timespan}'
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

        query = self.build_time_range_query(topic_name, fields, start, end, index, use_old_csc_indexing)

        response = self.query(query)

        if "series" not in response["results"][0]:
            return pd.DataFrame()

        return self._to_dataframe(response)


class InfluxDbDao(InfluxDBClient):

    def __init__(
        self, efd_name, database_name="efd", creds_service="https://roundtable.lsst.codes/segwarides/"
    ):
        auth = NotebookAuth(service_endpoint=creds_service)
        host, schema_registry_url, port, user, password, path = auth.get_auth(efd_name)

        url = urljoin(f"https://{host}:{port}", f"{path}")

        super(InfluxDbDao, self).__init__(url, database_name=database_name, username=user, password=password)
