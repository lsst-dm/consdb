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
from typing import Any

import astropy
import sqlalchemy
import sqlalchemy.dialects.postgresql
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from packaging.version import Version
from sqlalchemy.orm import Session

from ..cdb_schema import (
    AllowedFlexType,
    AllowedFlexTypeEnum,
    InstrumentTable,
    ObservationIdType,
    ObsTypeEnum,
    convert_to_flex_type,
)
from ..config import config
from ..dependencies import InstrumentName, get_db, get_instrument_list, get_instrument_table, get_logger
from ..exceptions import BadValueException
from ..models import (
    AddKeyRequestModel,
    AddKeyResponseModel,
    IndexResponseModel,
    InsertDataModel,
    InsertDataResponse,
    InsertFlexDataResponse,
    InsertMultipleRequestModel,
    InsertMultipleResponseModel,
    QueryRequestModel,
    QueryResponseModel,
)

external_router = APIRouter()
"""FastAPI router for all external handlers."""


@external_router.get(
    "/",
    description="Application root",
    summary="Application root",
)
def external_root(
    instrument_list: list[str] = Depends(get_instrument_list),
) -> IndexResponseModel:
    """Application root URL /consdb/."""

    return IndexResponseModel(
        name=config.name,
        version=config.version,
        description=config.description,
        repository_url=config.repository_url,
        documentation_url=config.documentation_url,
        instruments=instrument_list,
        obs_types=[o.value for o in ObsTypeEnum],
        dtypes=[d.value for d in AllowedFlexTypeEnum],
    )


@external_router.post(
    "/flex/{instrument}/{obs_type}/addkey",
    summary="Add a flexible metadata key",
    description="Add a flexible metadata key for the specified instrument and obs_type.",
)
def add_flexible_metadata_key(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum,
    data: AddKeyRequestModel,
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(get_logger),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> AddKeyResponseModel:
    """Add a key to a flexible metadata table."""

    schema_table = instrument_table.get_flexible_metadata_schema(obs_type)
    insert_stmt = schema_table.insert().values(
        key=data.key,
        dtype=data.dtype.value,
        doc=data.doc,
        unit=data.unit,
        ucd=data.ucd,
    )
    db.execute(insert_stmt)
    db.commit()
    # Update cached copy without re-querying database.
    instrument_table.flexible_metadata_schemas[obs_type.lower()][data.key] = [
        data.dtype.value,
        data.doc,
        data.unit,
        data.ucd,
    ]
    return AddKeyResponseModel(
        message="Key added to flexible metadata",
        key=data.key,
        instrument=instrument,
        obs_type=obs_type,
    )


@external_router.get(
    "/flex/{instrument}/{obs_type}/schema",
    summary="Get all flexible metadata keys",
    description="Flex schema for the given instrument and observation type.",
)
def get_flexible_metadata_keys(
    instrument: InstrumentName = Path(title="Instrument name"),
    obs_type: ObsTypeEnum = Path(title="Observation type"),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> dict[str, tuple[str, str, str | None, str | None]]:
    """Returns the flex schema for the given instrument and
    observation type.
    """

    obs_type = obs_type.lower()
    _ = instrument_table.compute_flexible_metadata_table_name(obs_type)
    instrument_table.refresh_flexible_metadata_schema(obs_type)

    return instrument_table.flexible_metadata_schemas[obs_type]


@external_router.get(
    "/flex/{instrument}/{obs_type}/obs/{obs_id}",
    description="Flex schema for the given instrument and observation type.",
)
def get_flexible_metadata(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum = Path(title="Observation type"),
    obs_id: ObservationIdType = Path(title="Observation ID"),
    k: list[str] = Query([], title="Columns to retrieve"),
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(get_logger),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> dict[str, AllowedFlexType]:
    """Retrieve values for an observation from a flexible metadata table."""

    table = instrument_table.get_flexible_metadata_table(obs_type)
    schema = instrument_table.flexible_metadata_schemas[obs_type]
    result = dict()

    query = db.query(table.c.key, table.c.value).filter(table.c.obs_id == obs_id)
    if len(k) > 0:
        query = query.filter(table.c.key.in_(k))
    rows = query.all()
    for key, value in rows:
        if key not in schema:
            instrument_table.refresh_flexible_metadata_schema(obs_type)
        schema = instrument_table.flexible_metadata_schemas[obs_type]
        dtype = schema[key][0]
        result[key] = convert_to_flex_type(AllowedFlexTypeEnum(dtype), value)
    return result


@external_router.post("/flex/{instrument}/{obs_type}/obs/{obs_id}")
def insert_flexible_metadata(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum,
    obs_id: ObservationIdType,
    data: InsertDataModel = Body(title="Data to insert or update"),
    u: int | None = Query(0, title="Update if exists"),
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(get_logger),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> InsertFlexDataResponse:
    """Insert or update key/value pairs in a flexible metadata table."""
    table = instrument_table.get_flexible_metadata_table(obs_type)
    schema = instrument_table.flexible_metadata_schemas[obs_type]

    value_dict = data.values
    if any(key not in schema for key in value_dict):
        instrument_table.refresh_flexible_metadata_schema(obs_type)
        schema = instrument_table.flexible_metadata_schemas[obs_type]
    for key, value in value_dict.items():
        if key not in schema:
            raise BadValueException("key", key, list(schema.keys()))

        # check value against dtype
        dtype = schema[key][0]
        if dtype != type(value).__name__:
            raise BadValueException(f"{dtype} value", value, [type(value).__name__])

    has_multi_column_primary_keys = (
        instrument_table.get_schema_version() >= Version("3.2.0") and obs_type == "exposure"
    )

    if has_multi_column_primary_keys:
        day_obs, seq_num = instrument_table.get_day_obs_and_seq_num(obs_id)

    for key, value in value_dict.items():
        value_str = str(value)

        values = {"obs_id": obs_id, "key": key, "value": value_str}
        if has_multi_column_primary_keys:
            values["day_obs"] = day_obs
            values["seq_num"] = seq_num

        stmt: sqlalchemy.sql.dml.Insert
        stmt = sqlalchemy.dialects.postgresql.insert(table).values(**values)
        logger.error(f"{u=}")
        if u != 0:
            if has_multi_column_primary_keys:
                stmt = stmt.on_conflict_do_update(
                    index_elements=["day_obs", "seq_num", "key"], set_={"value": value_str}
                )
            else:
                stmt = stmt.on_conflict_do_update(index_elements=["obs_id", "key"], set_={"value": value_str})

        logger.debug(str(stmt))
        _ = db.execute(stmt)

        db.commit()
    return InsertFlexDataResponse(
        message="Flexible metadata inserted",
        instrument=instrument,
        obs_type=obs_type,
        obs_id=obs_id,
    )


@external_router.post(
    "/insert/{instrument}/{table}/obs/{obs_id}",
    summary="Insert data row",
)
def insert(
    instrument: InstrumentName,
    table: str,
    obs_id: ObservationIdType,
    data: InsertDataModel = Body(title="Data to insert or update"),
    u: int | None = Query(0, title="Update if data already exist"),
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(get_logger),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> InsertDataResponse:
    """Insert or update column/value pairs in a ConsDB table."""

    schema = f"cdb_{instrument}."
    table_name = table.lower()
    if not table.lower().startswith(schema):
        table_name = schema + table_name

    if table_name not in instrument_table.schemas.tables:
        raise BadValueException("table", table_name, list(instrument_table.schemas.tables.keys()))

    table_obj = instrument_table.schemas.tables[table_name]

    valdict = data.values
    obs_id_colname = instrument_table.obs_id_column[table_name]
    valdict[obs_id_colname] = obs_id

    # If needed, cross-reference day_obs and seq_num from the exposure table.
    if "day_obs" in table_obj.columns and "seq_num" in table_obj.columns:
        if "day_obs" not in valdict or "seq_num" not in valdict:

            primary_key = obs_id
            for primary_key_name in ("obs_id", "exposure_id", "visit_id"):
                if primary_key_name in valdict:
                    primary_key = valdict[primary_key_name]

            day_obs, seq_num = instrument_table.get_day_obs_and_seq_num(primary_key)
            if "day_obs" not in valdict:
                valdict["day_obs"] = day_obs
            if "seq_num" not in valdict:
                valdict["seq_num"] = seq_num

    stmt: sqlalchemy.sql.dml.Insert
    stmt = sqlalchemy.dialects.postgresql.insert(table_obj).values(valdict)
    if u != 0:
        stmt = stmt.on_conflict_do_update(index_elements=[obs_id_colname], set_=valdict)
    logger.debug(str(stmt))
    _ = db.execute(stmt)
    db.commit()
    return InsertDataResponse(
        message="Data inserted",
        instrument=instrument,
        obs_id=obs_id,
        table=table_name,
    )


@external_router.post(
    "/insert/{instrument}/{table}",
    summary="Insert multiple data rows",
)
def insert_multiple(
    instrument: InstrumentName,
    table: str,
    data: InsertMultipleRequestModel = Body(title="Data to insert or update"),
    u: int | None = Query(0, title="Update if data already exist"),
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(get_logger),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> InsertMultipleResponseModel:
    """Insert or update multiple observations in a ConsDB table.

    Raises
    ------
    BadJsonException
        Raised if JSON is absent or missing a required key.

    BadValueException
        Raised if instrument or observation type is invalid.
    """

    schema = f"cdb_{instrument}."
    table_name = table.lower()
    if not table.lower().startswith(schema):
        table_name = schema + table_name
    table_obj = instrument_table.schemas.tables[table_name]
    table_name = f"cdb_{instrument}." + table.lower()
    obs_id_colname = instrument_table.obs_id_column[table_name]

    timestamp_columns = instrument_table.get_timestamp_columns(table_name)

    bulk_data = []
    for obs_id, valdict in data.obs_dict.items():
        valdict[obs_id_colname] = obs_id

        # If needed, cross-reference day_obs and seq_num from the
        # exposure table.
        if "day_obs" in table_obj.columns and "seq_num" in table_obj.columns:
            if "day_obs" not in valdict or "seq_num" not in valdict:
                primary_key = obs_id
                for primary_key_name in ("obs_id", "exposure_id", "visit_id"):
                    if primary_key_name in valdict:
                        primary_key = valdict[primary_key_name]

                day_obs, seq_num = instrument_table.get_day_obs_and_seq_num(primary_key)
                if "day_obs" not in valdict:
                    valdict["day_obs"] = day_obs
                if "seq_num" not in valdict:
                    valdict["seq_num"] = seq_num

        # Convert timestamps in the input from string to datetime
        for column in timestamp_columns:
            if column in valdict and valdict[column] is not None:
                timestamp = valdict[column]
                timestamp = astropy.time.Time(timestamp, format="isot", scale="tai")
                valdict[column] = timestamp.to_datetime()

    bulk_data.append(valdict)

    try:
        if bulk_data:
            stmt = sqlalchemy.dialects.postgresql.insert(table_obj).values(bulk_data)
            if u != 0:
                # Specify update behavior for conflicts
                update_dict = {col: stmt.excluded[col] for col in table_obj.columns.keys()}
                stmt = stmt.on_conflict_do_update(index_elements=[obs_id_colname], set_=update_dict)

            db.execute(stmt)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Failed to insert or update data")
        raise

    return InsertMultipleResponseModel(
        message="Data inserted",
        table=table,
        instrument=instrument,
        obs_id=data.obs_dict.keys(),
    )


@external_router.get(
    "/query/{instrument}/{obs_type}/obs/{obs_id}",
    summary="Get all metadata",
    description="Get all metadata for a given observation.",
)
def get_all_metadata(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum,
    obs_id: ObservationIdType,
    flex: bool = Query(False, title="Include flexible metadata"),
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(get_logger),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> dict[str, Any]:
    """Get all information about an observation.

    Parameters
    ----------
    instrument: `str`
        Name of the instrument (e.g. ``LATISS``).
    obs_type: `str`
        Name of the observation type (e.g. ``Exposure``).
    obs_id: `int`
        Unique observation identifier.
    flex: bool
        Include flexible metadata if set to "1" (URL query parameter).

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.
        Response is a dict with columns as keys.

    Raises
    ------
    """

    obs_type = obs_type.lower()
    view_name = instrument_table.compute_wide_view_name(obs_type)
    view = instrument_table.schemas[view_name]
    obs_id_column = instrument_table.obs_id_column[view_name]
    result = dict()

    row = db.query(view).filter(view.c[obs_id_column] == obs_id).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Observation {obs_id} not found.")

    result = dict(row)

    if flex:
        flex_result = get_flexible_metadata(instrument, obs_type, obs_id)
        result.update(flex_result)
    return result


@external_router.post("/query")
def query(
    data: QueryRequestModel = Body(title="SQL query string"),
    db: Session = Depends(get_db),
    logger: logging.Logger = Depends(get_logger),
) -> QueryResponseModel:
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
    """

    columns = []
    rows = []

    with db.connection() as connection:
        result = connection.exec_driver_sql(data.query)
        columns = result.keys()
        rows = [list(row) for row in result]

    return QueryResponseModel(
        columns=columns,
        data=rows,
    )


@external_router.get("/schema")
def list_instruments(
    instrument_list: list[str] = Depends(get_instrument_list),
) -> list[str]:
    """Retrieve the list of instruments available in ConsDB."""

    return instrument_list


@external_router.get("/schema/{instrument}")
def list_table(
    instrument: InstrumentName,
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> list[str]:
    """Retrieve the list of tables for an instrument."""

    schema = instrument_table.schemas
    return list(schema.tables.keys())


@external_router.get("/schema/{instrument}/{table}")
def schema(
    instrument: InstrumentName = Path(description="Instrument name"),
    table: str = Path(description="Table name to retrieve schema"),
    instrument_table: InstrumentTable = Depends(get_instrument_table),
) -> dict[str, list[str | None]]:
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

    schema = instrument_table.schemas
    if not table.startswith(f"cdb_{instrument}."):
        table = f"cdb_{instrument}.{table}"
    table = table.lower()
    if table not in schema.tables:
        raise BadValueException("table", table, list(schema.tables.keys()))
    return {c.name: [str(c.type), c.doc] for c in schema.tables[table].columns}
