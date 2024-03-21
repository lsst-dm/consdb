import os
from pandas import DataFrame
import requests
from requests.exceptions import RequestException
from typing import Any, Iterable
from urllib.parse import urljoin

session = requests.Session()
base_url = os.environ["CONSDB_URL"]


def insert(table: str, values: dict[str, Any], **kwargs):
    values.update(kwargs)
    # check values against schema for table
    data = {"table": table, "values": values}
    url = urljoin(base_url, "insert")
    try:
        response = requests.post(url, json=data)
    except RequestException as e:
        raise e
    response.raise_for_status()


def query(
    tables: str | Iterable[str],
    columns: str | Iterable[str],
    *,
    where: str | None = None,
    join: str | None = None
) -> list[Any]:
    if isinstance(tables, str):
        tables = [tables]
    if isinstance(columns, str):
        columns = [columns]
    url = urljoin(base_url, "query")
    data = {"tables": tables, "columns": columns, "where": where, "join": join}
    try:
        response = requests.post(url, json=data)
    except RequestException as e:
        raise e
    try:
        response.raise_for_status()
    except Exception as ex:
        print(response.content.decode())
        raise ex
    arr = response.json()
    return DataFrame(arr[1:], columns=arr[0])


def schema(table: str):
    url = urljoin(base_url, "schema/")
    url = urljoin(url, table)
    try:
        response = requests.get(url)
    except RequestException as e:
        raise e
    response.raise_for_status()
    return response.json()
