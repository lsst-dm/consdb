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

from typing import Any, Iterable

import sqlalchemy
import sqlalchemy.dialects.postgresql
from flask import Flask, request
from utils import setup_logging, setup_postgres

INSTRUMENT_LIST = ["latiss"]
OBS_TYPE_LIST = ["exposure", "visit", "ccdexposure", "ccdvisit"]
DTYPE_LIST = ["bool", "int", "float", "str"]

OBS_ID_COLNAME_LIST = ["ccdexposure_id", "exposure_id", "obs_id"]

####################
# Global app setup #
####################


app = Flask(__name__)
engine = setup_postgres()
logger = setup_logging(__name__)


########################
# Schema preload class #
########################


class InstrumentTables:
    """The column information for all tables in ConsDB schemas."""

    def __init__(self):
        self.table_names = set()
        self.schemas = dict()
        self.flexible_metadata_schemas = dict()
        self.obs_id_column = dict()
        for instrument in INSTRUMENT_LIST:
            md = sqlalchemy.MetaData(schema=f"cdb_{instrument}")
            md.reflect(engine)
            self.table_names.update([str(table) for table in md.tables])
            self.schemas[instrument] = md
            self.obs_id_column[instrument] = dict()
            self.flexible_metadata_schemas[instrument] = dict()
            for table in md.tables:
                for col_name in OBS_ID_COLNAME_LIST:
                    if col_name in md.tables[table].columns:
                        self.obs_id_column[instrument][table] = col_name
                        break
            for obs_type in OBS_TYPE_LIST:
                table_name = f"cdb_{instrument}.{obs_type}_flexdata"
                schema_table_name = table_name + "_schema"
                if table_name in md.tables and schema_table_name in md.tables:
                    schema_table = md.tables[schema_table_name]
                    stmt = sqlalchemy.select(schema_table.c["key", "dtype", "doc", "unit", "ucd"])
                    schema = dict()
                    with engine.connect() as conn:
                        for row in conn.execute(stmt):
                            schema[row[0]] = row[1:]
                    self.flexible_metadata_schemas[instrument][obs_type] = schema

    def refresh_flexible_metadata_schema(self, instrument: str, obs_type: str):
        schema = dict()
        schema_table = self.get_flexible_metadata_schema(instrument, obs_type)
        stmt = sqlalchemy.select(schema_table.c["key", "dtype", "doc", "unit", "ucd"])
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                schema[row[0]] = row[1:]
        self.flexible_metadata_schemas[instrument][obs_type] = schema

    def compute_flexible_metadata_table_name(self, instrument: str, obs_type: str) -> str:
        """Compute the name of a flexible metadata table.

        Each instrument and observation type made with that instrument can
        have a flexible metadata table.

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

        Raises
        ------
        BadValueException
            Raised if the `instrument` or `obs_type` are not found.
        """
        instrument = instrument.lower()
        obs_type = obs_type.lower()
        if instrument not in self.flexible_metadata_schemas:
            raise BadValueException("instrument", instrument, list(self.flexible_metadata_schemas.keys()))
        if obs_type not in self.flexible_metadata_schemas[instrument]:
            raise BadValueException(
                "observation type",
                obs_type,
                list(self.flexible_metadata_schemas.keys()),
            )
        return f"cdb_{instrument}.{obs_type}_flexdata"

    def compute_flexible_metadata_table_schema_name(self, instrument: str, obs_type: str) -> str:
        """Compute the name of a flexible metadata schema table.

        The schema table contains descriptions of all keys in the flexible
        metadata table for the instrument and observation type.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        schema_table_name: `str`
            Name of the appropriate flexible metadata schema table.
        """
        table_name = self.compute_flexible_metadata_table_name(instrument, obs_type)
        return table_name + "_schema"

    def get_flexible_metadata_table(self, instrument: str, obs_type: str) -> sqlalchemy.schema.Table:
        """Get the table object for a flexible metadata table.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        table_obj: `sqlalchemy.schema.Table`
            ``Table`` object for the flexible metadata table.
        """
        instrument = instrument.lower()
        obs_type = obs_type.lower()
        table_name = self.compute_flexible_metadata_table_name(instrument, obs_type)
        return self.schemas[instrument].tables[table_name]

    def get_flexible_metadata_schema(self, instrument: str, obs_type: str):
        """Get the table object for a flexible metadata schema table.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        schema_table_obj: `sqlalchemy.schema.Table`
            ``Table`` object for the flexible metadata schema table.
        """
        instrument = instrument.lower()
        obs_type = obs_type.lower()
        table_name = self.compute_flexible_metadata_table_schema_name(instrument, obs_type)
        return self.schemas[instrument].tables[table_name]


instrument_tables = InstrumentTables()


##################
# Error handling #
##################


class BadJsonException(Exception):
    """Exception raised for invalid JSON.

    Reports the list of required keys.

    Parameters
    ----------
    method: `str`
        Name of the method being invoked.
    keys: `Iterable` [ `str` ]
        List of keys required in the JSON object.
    """

    status_code = 404

    def __init__(self, method: str, keys: Iterable[str]):
        self.method = method
        self.keys = keys

    def to_dict(self) -> dict[str, Any]:
        """Convert the exception to a dictionary for JSON conversion.

        Returns
        -------
        json_dict: `dict` [ `str`, `Any` ]
            Dictionary with a message and list of required keys.
        """
        data = {
            "message": f"Invalid JSON for {self.method}",
            "required_keys": self.keys,
        }
        return data


def _check_json(json: dict | None, method: str, keys: Iterable[str]) -> dict[str, Any]:
    """Check a JSON object for the presence of required keys.

    Parameters
    ----------
    json: `dict`
        The decoded JSON object.
    method: `str`
        The name of the Web service method being invoked.
    keys: `Iterable` [ `str` ]
        The keys required to be in the JSON object.

    Raises
    ------
    BadJsonException
         Raised if any key is missing.
    """
    if not json or any(x not in json for x in keys):
        raise BadJsonException(method, keys)
    return json


class BadValueException(Exception):
    """Exception raised for an invalid value.

    Reports the bad value and, if available, a list of valid values.

    Parameters
    ----------
    kind: `str`
        Kind of value that failed to validate.
    value: `Any`
        The invalid value.
    valid: `list` [ `Any` ], optional
        List of valid values.
    """

    status_code = 404

    def __init__(self, kind: str, value: Any, valid: list[Any] | None = None):
        self.kind = kind
        self.value = value
        self.valid = valid

    def to_dict(self) -> dict[str, Any]:
        """Convert the exception to a dictionary for JSON conversion.

        Returns
        -------
        json_dict: `dict` [ `str`, `Any` ]
            Dictionary with a message, value, and, if available, list of
            valid values.
        """
        data = {
            "message": f"Unknown {self.kind}",
            "value": self.value,
        }
        if self.valid:
            data["valid"] = self.valid
        return data


@app.errorhandler(BadJsonException)
def handle_bad_json(e: BadJsonException) -> tuple[dict[str, Any], int]:
    """Handle a BadJsonException by returning its content as JSON."""
    return e.to_dict(), e.status_code


@app.errorhandler(BadValueException)
def handle_bad_value(e: BadValueException) -> tuple[dict[str, Any], int]:
    """Handle a BadValueException by returning its content as JSON."""
    return e.to_dict(), e.status_code


@app.errorhandler(sqlalchemy.exc.SQLAlchemyError)
def handle_sql_error(e: sqlalchemy.exc.SQLAlchemyError) -> tuple[dict[str, str], int]:
    """Handle a SQLAlchemyError by returning its content as JSON."""
    return {"message": str(e)}, 500


###################################
# Web service application methods #
###################################


@app.get("/")
def root() -> dict[str, list[str]]:
    """Root URL for liveness checks.

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with a list of instruments, observation types, and
        data types.
    """
    # Don't log liveness checks.
    data = {
        "instruments": INSTRUMENT_LIST,
        "obs_types": OBS_TYPE_LIST,
        "dtypes": DTYPE_LIST,
    }
    return data


@app.get("/consdb")
def root2() -> dict[str, list[str]]:
    """Application root URL.

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with a list of instruments, observation types, and
        data types.
    """
    logger.info(request)
    data = {
        "instruments": INSTRUMENT_LIST,
        "obs_types": OBS_TYPE_LIST,
        "dtypes": DTYPE_LIST,
    }
    return data


@app.post("/consdb/flex/<instrument>/<obs_type>/addkey")
def add_flexible_metadata_key(instrument: str, obs_type: str) -> dict[str, Any] | tuple[dict[str, str], int]:
    """Add a key to a flexible metadata table.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    obs_type: `str`
        Name of the observation type (e.g. ``Exposure``).
    key: `str`
        Key to add (POST JSON data).
    dtype: `str`
        Data type of key's value from ``DTYPE_LIST`` (POST JSON data).
    doc: `str`
        Documentation string (POST JSON data).
    unit: `str`, optional
        Unit for value (POST JSON data).
    ucd: `str`, optional
        IVOA Unified Content Descriptor (https://www.ivoa.net/documents/UCD1+/)
        for value (POST JSON data).

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.

    Raises
    ------
    BadJsonException
        Raised if JSON is absent or missing a required key.

    BadValueException
        Raised if instrument or observation type is invalid.
    """
    logger.info(f"{request} {request.json}")
    info = _check_json(request.json, "flex addkey", ("key", "dtype", "doc"))
    schema_table = instrument_tables.get_flexible_metadata_schema(instrument, obs_type)
    key = info["key"]
    dtype = info["dtype"]
    if dtype not in DTYPE_LIST:
        raise BadValueException("dtype", dtype, DTYPE_LIST)
    doc = info["doc"]
    unit = info.get("unit")
    ucd = info.get("ucd")
    stmt = sqlalchemy.insert(schema_table).values(key=key, dtype=dtype, doc=doc, unit=unit, ucd=ucd)
    logger.debug(str(stmt))
    with engine.connect() as conn:
        _ = conn.execute(stmt)
        conn.commit()
    # Update cached copy without re-querying database.
    instrument_tables.flexible_metadata_schemas[instrument.lower()][obs_type.lower()][key] = [
        dtype,
        doc,
        unit,
        ucd,
    ]
    return {
        "message": "Key added to flexible metadata",
        "key": key,
        "instrument": instrument,
        "obs_type": obs_type,
    }


@app.get("/consdb/flex/<instrument>/<obs_type>/schema")
def get_flexible_metadata_keys(instrument: str, obs_type: str) -> dict[str, list[str | None]]:
    """Retrieve descriptions of keys for a flexible metadata table.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    obs_type: `str`
        Name of the observation type (e.g. ``Exposure``).

    Returns
    -------
    json_dict: `dict` [ `str`, `list` [ `str` | `None` ] ]
        JSON response with 200 HTTP status on success.
        Response is a dictionary of ``dtype``, ``doc``, ``unit``, and ``ucd``
        strings for each key in the table.

    Raises
    ------
    BadValueException
        Raised if instrument or observation type is invalid.
    """
    logger.info(request)
    instrument = instrument.lower()
    obs_type = obs_type.lower()
    _ = instrument_tables.compute_flexible_metadata_table_name(instrument, obs_type)
    instrument_tables.refresh_flexible_metadata_schema(instrument, obs_type)
    return instrument_tables.flexible_metadata_schemas[instrument][obs_type]


@app.get("/consdb/flex/<instrument>/<obs_type>/obs/<int:obs_id>")
def get_flexible_metadata(instrument: str, obs_type: str, obs_id: int) -> dict[str, Any]:
    """Retrieve values for an observation from a flexible metadata table.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    obs_type: `str`
        Name of the observation type (e.g. ``Exposure``).
    obs_id: `int`
        Unique observation identifier.

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.
        Response is a dictionary of ``key``, ``value`` pairs with values
        converted from strings.

    Raises
    ------
    BadValueException
        Raised if instrument or observation type is invalid.
    """
    logger.info(request)
    instrument = instrument.lower()
    obs_type = obs_type.lower()
    table = instrument_tables.get_flexible_metadata_table(instrument, obs_type)
    schema = instrument_tables.flexible_metadata_schemas[instrument][obs_type]
    result = dict()
    stmt = sqlalchemy.select(table.c["key", "value"]).where(table.c.obs_id == obs_id)
    if request.args and "k" in request.args:
        cols = request.args.getlist("k")
        stmt = stmt.where(table.c.key.in_(cols))
    logger.debug(str(stmt))
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            key, value = row
            if key not in schema:
                instrument_tables.refresh_flexible_metadata_schema(instrument, obs_type)
            schema = instrument_tables.flexible_metadata_schemas[instrument][obs_type]
            dtype = schema[key][0]
            if dtype == "bool":
                result[key] = value == "True"
            elif dtype == "int":
                result[key] = int(value)
            elif dtype == "float":
                result[key] = float(value)
            else:
                result[key] = str(value)
    return result


@app.post("/consdb/flex/<instrument>/<obs_type>/obs/<int:obs_id>")
def insert_flexible_metadata(
    instrument: str, obs_type: str, obs_id: int
) -> dict[str, Any] | tuple[dict[str, str], int]:
    """Insert or update key/value pairs in a flexible metadata table.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    obs_type: `str`
        Name of the observation type (e.g. ``Exposure``).
    obs_id: `int`
        Unique observation identifier.
    u: `str`
        Allow update if set to "1" (URL query parameter).
    values: `dict` [ `str`, `Any` ]
        Dictionary of key/value pairs to insert or update (JSON POST data).

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.

    Raises
    ------
    BadJsonException
        Raised if JSON is absent or missing a required key.

    BadValueException
        Raised if instrument or observation type is invalid.
    """
    logger.info(f"{request} {request.json}")
    info = _check_json(request.json, "flex obs", ("values",))
    instrument = instrument.lower()
    obs_type = obs_type.lower()
    table = instrument_tables.get_flexible_metadata_table(instrument, obs_type)
    schema = instrument_tables.flexible_metadata_schemas[instrument][obs_type]

    value_dict = info["values"]
    if any(key not in schema for key in value_dict):
        instrument_tables.refresh_flexible_metadata_schema(instrument, obs_type)
        schema = instrument_tables.flexible_metadata_schemas[instrument][obs_type]
    for key, value in value_dict.items():
        if key not in schema:
            raise BadValueException("key", key, list(schema.keys()))

        # check value against dtype
        dtype = schema[key][0]
        if dtype == "bool" and not isinstance(value, bool):
            raise BadValueException("bool value", value)
        elif dtype == "int" and not isinstance(value, int):
            raise BadValueException("int value", value)
        elif dtype == "float" and not isinstance(value, float):
            raise BadValueException("float value", value)
        elif dtype == "str" and not isinstance(value, str):
            raise BadValueException("str value", value)

    with engine.connect() as conn:
        for key, value in value_dict.items():
            value_str = str(value)
            stmt: sqlalchemy.sql.dml.Insert
            if request.args and request.args.get("u") == "1":
                stmt = (
                    sqlalchemy.dialects.postgresql.insert(table)
                    .values(obs_id=obs_id, key=key, value=value_str)
                    .on_conflict_do_update(index_elements=["obs_id", "key"], set_={"value": value_str})
                )
            else:
                stmt = sqlalchemy.insert(table).values(obs_id=obs_id, key=key, value=value_str)
            logger.debug(str(stmt))
            _ = conn.execute(stmt)

        conn.commit()
    return {
        "message": "Flexible metadata inserted",
        "obs_id": obs_id,
        "instrument": instrument,
        "obs_type": obs_type,
    }


@app.post("/consdb/insert/<instrument>/<table>/obs/<int:obs_id>")
def insert(instrument: str, table: str, obs_id: int) -> dict[str, Any] | tuple[dict[str, str], int]:
    """Insert or update column/value pairs in a ConsDB table.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    table: `str`
        Name of table to insert into.
    obs_id: `int`
        Unique observation identifier.
    u: `str`
        Allow update if set to "1" (URL query parameter).
    values: `dict` [ `str`, `Any` ]
        Dictionary of key/value pairs to insert or update (JSON POST data).

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.

    Raises
    ------
    BadJsonException
        Raised if JSON is absent or missing a required key.

    BadValueException
        Raised if instrument or observation type is invalid.
    """
    logger.info(f"{request} {request.json}")
    instrument = instrument.lower()
    if instrument not in instrument_tables.schemas:
        raise BadValueException("instrument", instrument, list(instrument_tables.schemas.keys()))
    info = _check_json(request.json, "insert", ("values",))
    schema = f"cdb_{instrument}."
    table_name = table.lower()
    if not table.lower().startswith(schema):
        table_name = schema + table_name
    table_obj = instrument_tables.schemas[instrument].tables[table_name]
    valdict = info["values"]
    obs_id_colname = instrument_tables.obs_id_column[instrument][table_name]
    valdict[obs_id_colname] = obs_id

    stmt: sqlalchemy.sql.dml.Insert
    if request.args and request.args.get("u") == "1":
        stmt = (
            sqlalchemy.dialects.postgresql.insert(table_obj)
            .values(valdict)
            .on_conflict_do_update(index_elements=[obs_id_colname], set_=valdict)
        )
    else:
        stmt = sqlalchemy.insert(table_obj).values(valdict)
    logger.debug(str(stmt))
    with engine.connect() as conn:
        _ = conn.execute(stmt)
        conn.commit()
    return {
        "message": "Data inserted",
        "instrument": instrument,
        "table": table_name,
        "obs_id": obs_id,
    }


@app.post("/consdb/insert/<instrument>/<table>")
def insert_multiple(instrument: str, table: str) -> dict[str, Any] | tuple[dict[str, str], int]:
    """Insert or update multiple observations in a ConsDB table.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    table: `str`
        Name of table to insert into.
    u: `str`
        Allow update if set to "1" (URL query parameter).
    obs_dict: `dict` [ `int`, `dict` [ `str`, `Any` ] ]
        Dictionary of unique observation ids and key/value pairs to insert or
        update (JSON POST data).

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.

    Raises
    ------
    BadJsonException
        Raised if JSON is absent or missing a required key.

    BadValueException
        Raised if instrument or observation type is invalid.
    """
    logger.info(f"{request} {request.json}")
    instrument = instrument.lower()
    if instrument not in instrument_tables.schemas:
        raise BadValueException("instrument", instrument, list(instrument_tables.schemas.keys()))
    info = _check_json(request.json, "insert", ("obs_dict"))
    schema = f"cdb_{instrument}."
    table_name = table.lower()
    if not table.lower().startswith(schema):
        table_name = schema + table_name
    table_obj = instrument_tables.schemas[instrument].tables[table_name]
    table_name = f"cdb_{instrument}." + info["table"].lower()
    table = instrument_tables.schemas[instrument].tables[table_name]
    obs_id_colname = instrument_tables.obs_id_column[instrument][table_name]

    with engine.connect() as conn:
        for obs_id, valdict in info["obs_dict"]:
            if not isinstance(obs_id, int):
                raise BadValueException("obs_id value", obs_id)
            valdict[obs_id_colname] = obs_id

            stmt: sqlalchemy.sql.dml.Insert
            if request.args and request.args.get("u") == "1":
                stmt = (
                    sqlalchemy.dialects.postgresql.insert(table_obj)
                    .values(valdict)
                    .on_conflict_do_update(index_elements=[obs_id_colname], set_=valdict)
                )
            else:
                stmt = sqlalchemy.insert(table_obj).values(valdict)
            logger.debug(str(stmt))
            # TODO: optimize as executemany
            _ = conn.execute(stmt)
        conn.commit()

    return {
        "message": "Data inserted",
        "table": table_name,
        "instrument": instrument,
        "obs_ids": info["obs_dict"].keys(),
    }


@app.post("/consdb/query")
def query() -> dict[str, Any] | tuple[dict[str, str], int]:
    """Query the ConsDB database.

    Parameters
    ----------
    query: `str`
        SQL query string (JSON POST data).

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.
        Response is a dict with a ``columns`` key with value being a list
        of string column names and a ``data`` key with value being a list
        of rows.

    Raises
    ------
    BadJsonException
        Raised if JSON is absent or missing a required key.
    """
    logger.info(f"{request} {request.json}")
    info = _check_json(request.json, "query", ("query",))
    with engine.connect() as conn:
        cursor = conn.exec_driver_sql(info["query"])
        first = True
        result = {}
        rows = []
        for row in cursor:
            if first:
                result["columns"] = list(row._fields)
                first = False
            rows.append(list(row))
        result["data"] = rows
    return result


@app.get("/consdb/schema")
def list_instruments() -> list[str]:
    """Retrieve the list of instruments available in ConsDB."

    Returns
    -------
    json_list: `list` [ `str` ]
        JSON response with 200 HTTP status on success.
        Response is a list of instrument names.

    Raises
    ------
    BadValueException
        Raised if instrument is invalid.
    """
    logger.info(request)
    return list(instrument_tables.schemas.keys())


@app.get("/consdb/schema/<instrument>")
def list_table(instrument: str) -> list[str]:
    """Retrieve the list of tables for an instrument.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).

    Returns
    -------
    json_list: `list` [ `str` ]
        JSON response with 200 HTTP status on success.
        Response is a list of table names.

    Raises
    ------
    BadValueException
        Raised if instrument is invalid.
    """
    logger.info(request)
    instrument = instrument.lower()
    if instrument not in instrument_tables.schemas:
        raise BadValueException("instrument", instrument, list(instrument_tables.schemas.keys()))
    schema = instrument_tables.schemas[instrument]
    return list(schema.tables.keys())


@app.get("/consdb/schema/<instrument>/<table>")
def schema(instrument: str, table: str) -> dict[str, list[str]]:
    """Retrieve the descriptions of columns in a ConsDB table.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    table: `str`
        Name of table.

    Returns
    -------
    json_dict: `dict` [ `str`, `list` [ `str` ] ]
        JSON response with 200 HTTP status on success.
        Response is a dict with column names as keys and lists of data type
        and documentation strings as values.

    Raises
    ------
    BadValueException
        Raised if instrument is invalid.
    """
    logger.info(request)
    instrument = instrument.lower()
    if instrument not in instrument_tables.schemas:
        raise BadValueException("instrument", instrument, list(instrument_tables.schemas.keys()))
    schema = instrument_tables.schemas[instrument]
    if not table.startswith(f"cdb_{instrument}"):
        table = f"cdb_{instrument}.{table}"
    table = table.lower()
    if table not in schema.tables:
        raise BadValueException("table", table, list(schema.tables.keys()))
    return {c.name: [str(c.type), c.doc] for c in schema.tables[table].columns}
