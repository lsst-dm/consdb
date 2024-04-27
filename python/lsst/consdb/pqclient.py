# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
from typing import Any
from urllib.parse import quote

import requests
from astropy.table import Table  # type: ignore

__all__ = ["ConsDbClient"]


logger = logging.getLogger(__name__)


def _urljoin(*args: str) -> str:
    """Join parts of a URL with slashes.

    Does not do any quoting.  Mostly to remove a level of list-making.

    Parameters
    ----------
    *args: `str`
        Each parameter is a URL part.

    Returns
    -------
    url: `str`
        The joined URL.
    """
    return "/".join(args)


class ConsDbClient:
    """A client library for accessing the Consolidated Database.

    This library provides a basic interface for using flexible metadata
    (key/value pairs associated with observation ids from an observation
    type table), determining the schema of ConsDB tables, querying the
    ConsDB using a general SQL SELECT statement, and inserting into
    ConsDB tables.

    Parameters
    ----------
    url: `str`, optional
        Base URL of the Web service, defaults to the value of environment
        variable ``LSST_CONSDB_PQ_URL`` (the location of the publish/query
        service).

    Notes
    -----
    This client is a thin layer over the publish/query Web service, which
    avoids having a dependency on database drivers.

    It enforces the return of query results as Astropy Tables.

    """

    def __init__(self, url: str | None = None):
        self.session = requests.Session()
        if url is None:
            self.url = os.environ["LSST_CONSDB_PQ_URL"]
        else:
            self.url = url
        self.url = self.url.rstrip("/")

    def _handle_get(
        self, url: str, query: dict[str, str | list[str]] | None = None
    ) -> Any:
        """Submit GET requests to the server.

        Parameters
        ----------
        url: `str`
            URL to GET.
        query: `dict` [`str`, `str` | `list` [`str`]], optional
            Query parameters to attach to the URL.

        Raises
        ------
        requests.exceptions.RequestException
            Raised if any kind of connection error occurs.
        requests.exceptions.HTTPError
            Raised if a non-successful status is returned.
        requests.exceptions.JSONDecodeError
            Raised if the result does not decode as JSON.

        Returns
        -------
        result: `Any`
            Result of decoding the Web service result content as JSON.
        """
        logger.debug(f"GET {url}")
        try:
            response = self.session.get(url, params=query)
        except requests.exceptions.RequestException as e:
            raise e
        response.raise_for_status()
        return response.json()

    def _handle_post(self, url: str, data: dict[str, Any]) -> requests.Response:
        """Submit POST requests to the server.

        Parameters
        ----------
        url: `str`
            URL to POST.
        data: `dict` [`str`, `Any`]
            Key/value pairs of data to POST.

        Raises
        ------
        requests.exceptions.RequestException
            Raised if any kind of connection error occurs.
        requests.exceptions.HTTPError
            Raised if a non-successful status is returned.

        Returns
        -------
        result: `requests.Response`
            The raw Web service result object.
        """
        logger.debug(f"POST {url}: {data}")
        try:
            response = self.session.post(url, json=data)
        except requests.exceptions.RequestException as e:
            raise e
        response.raise_for_status()
        return response

    @staticmethod
    def compute_flexible_metadata_table_name(instrument: str, obs_type: str) -> str:
        """Compute the name of a flexible metadata table.

        Each instrument and observation type made with that instrument can
        have a flexible metadata table.  This function is useful when
        issuing SQL queries, and it avoids a round-trip to the server.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        table_name: `str`
            Name of the appropriate flexible metadata table.

        """
        return f"cdb_{instrument}.{obs_type}_flexdata"

    def add_flexible_metadata_key(
        self, instrument: str, obs_type: str, key: str, dtype: str, doc: str
    ) -> requests.Response:
        """Add a key to a flexible metadata table.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).
        key: `str`
            Name of the key to be added (must not already exist).
        dtype: `str`
            One of ``bool``, ``int``, ``float``, or ``str``.
        doc: `str`
            Documentation string for the key. Ideally contains units and a UCD.

        Returns
        -------
        response: `requests.Response`
            HTTP response from the server, with 200 status for success.
        """
        data = {"key": key, "dtype": dtype, "doc": doc}
        url = _urljoin(self.url, "flex", quote(instrument), quote(obs_type), "addkey")
        return self._handle_post(url, data)

    def get_flexible_metadata_keys(
        self, instrument: str, obs_type: str
    ) -> list[tuple[str, str, str]]:
        """Retrieve the valid keys for a flexible metadata table.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        key_info: `list` [ `tuple` [ `str`, `str`, `str` ] ]
            List of tuples, one for each key. Each tuple contains the name of
            the key, a data type string, and a documentation string.
        """
        url = _urljoin(self.url, "flex", quote(instrument), quote(obs_type), "schema")
        return self._handle_get(url)

    def get_flexible_metadata(
        self, instrument: str, obs_type: str, obs_id: int, keys: list[str] | None = None
    ) -> dict[str, Any]:
        """Get the flexible metadata for an observation.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).
        obs_id: `int`
            Unique observation id.
        keys: `list` [ `str` ], optional
            List of keys to be retrieved; all if not specified.

        Returns
        -------
        result_dict: `dict` [ `str`, `Any` ]
            Dictionary of key/value pairs for the observation.
        """
        url = _urljoin(
            self.url,
            "flex",
            quote(instrument),
            quote(obs_type),
            "obs",
            quote(str(obs_id)),
        )
        return self._handle_get(url, {"k": keys} if keys else None)

    def insert_flexible_metadata(
        self,
        instrument: str,
        obs_type: str,
        obs_id: int,
        values: dict[str, Any] | None = None,
        *,
        allow_update: bool = False,
        **kwargs,
    ) -> requests.Response:
        """Set flexible metadata values for an observation.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).
        obs_id: `int`
            Unique observation id.
        values: `dict` [ `str`, `Any` ], optional
            Dictionary of key/value pairs to add for the observation.
        allow_update: `bool`, optional
            If ``True``, allow replacement of values of existing keys.
        **kwargs: `dict`
            Additional key/value pairs, overriding ``values``.

        Returns
        -------
        response: `requests.Response`
            HTTP response from the server, with 200 status for success.
        """
        if values:
            values.update(kwargs)
        else:
            values = kwargs
        data = {"values": values}
        url = _urljoin(
            self.url,
            "flex",
            quote(instrument),
            quote(obs_type),
            "obs",
            quote(str(obs_id)),
        )
        if allow_update:
            url += "?u=1"
        return self._handle_post(url, data)

    def insert(
        self,
        instrument: str,
        table: str,
        obs_id: int,
        values: dict[str, Any],
        *,
        allow_update=False,
        **kwargs,
    ) -> requests.Response:
        """Insert values into a single ConsDB fixed metadata table.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        table: `str`
            Name of the table to insert into.
        obs_id: `int`
            Unique observation id.
        values: `dict` [ `str`, `Any` ], optional
            Dictionary of column/value pairs to add for the observation.
        allow_update: `bool`, optional
            If ``True``, allow replacement of values of existing columns.
        **kwargs: `dict`
            Additional column/value pairs, overriding ``values``.

        Returns
        -------
        response: `requests.Response`
            HTTP response from the server, with 200 status for success.
        """
        if values:
            values.update(kwargs)
        else:
            values = kwargs
        data = {"table": table, "obs_id": obs_id, "values": values}
        url = _urljoin(
            self.url,
            "insert",
            quote(instrument),
            quote(table),
            "obs",
            quote(str(obs_id)),
        )
        if allow_update:
            url += "?u=1"
        return self._handle_post(url, data)

    def query(self, query: str) -> Table:
        """Query the ConsDB database.

        Parameters
        ----------
        query: `str`
            A SQL query (currently) to the database.

        Returns
        -------
        result: `Table`
            An ``astropy.Table`` containing the query results.

        Notes
        -----
        This is a very general query interface because it is expected that
        a wide variety of types of queries will be needed. If some types prove
        to be common, syntactic sugar could be added to make the simpler.
        """
        url = _urljoin(self.url, "query")
        data = {"query": query}
        result = self._handle_post(url, data).json()
        return Table(rows=result["data"], names=result["columns"])

    def schema(self, instrument: str, table: str) -> list[tuple[str, str, str]]:
        """Retrieve the schema of a fixed metadata table in ConsDB.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        table: `str`
            Name of the table to insert into.

        Returns
        -------
        column_info: `list` [ `tuple` [ `str`, `str`, `str` ] ]
            List of tuples, one for each column in the table. Each tuple
            contains the name of the key, a data type string, and a
            documentation string.

        Notes
        -----
        Fixed metadata data types may use the full database vocabulary,
        unlike flexible metadata data types.
        """
        url = _urljoin(self.url, "schema", quote(instrument), quote(table))
        return self._handle_get(url)
