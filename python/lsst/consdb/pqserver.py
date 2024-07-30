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

from enum import Enum
from typing import Annotated, Any, Iterable, Optional

from flask import Flask, request
from fastapi import FastAPI, APIRouter, Depends, Path
import sqlalchemy
import sqlalchemy.dialects.postgresql
from pydantic import BaseModel, Field, field_validator
from safir.metadata import Metadata, get_metadata
from .utils import setup_logging, setup_postgres

internal_router = APIRouter()
external_router = APIRouter()


class ObsTypeEnum(str, Enum):
    EXPOSURE = "exposure"
    VISIT1 = "visit1"
    CCD_EXPOSURE = "ccdexposure"
    CCD_VISIT1 = "ccdvisit1"

    @classmethod
    def _missing_(cls, value):
        """Makes the enum case-insensitive, see https://docs.python.org/3/library/enum.html"""
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


ObservationIdType = int

AllowedFlexType = bool | int | float | str
AllowedFlexTypeEnum = Enum(
    "AllowedFlexTypeEnum", {t.__name__.upper(): t.__name__ for t in AllowedFlexType.__args__}
)


def convert_to_flex_type(ty: AllowedFlexTypeEnum, v: str) -> AllowedFlexType:
    """Converts a string containing a flex database value into the appropriate type.

    Raises
    ======
    RuntimeError if ty does not match an allowed flex type

    ValueError if the conversion is invalid
    """
    if ty.value == "bool":  # Special case
        return v.lower() in ("true", "t", "1")
    m = [t for t in AllowedFlexType.__args__ if t.__name__ == ty]
    assert len(m) == 1
    return m[0](v)


class ObsIdColname(str, Enum):
    CCD_VISIT_ID = "ccdvisit_id"
    VISIT_ID = "visit_id"
    CCDEXPOSURE_ID = "ccdexposure_id"
    EXPOSURE_ID = "exposure_id"
    OBS_ID = "obs_id"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


def validate_instrument_name(
    instrument: str = Path(..., description="Must be a valid instrument name (e.g., ``LATISS``)"),
) -> str:
    global instrument_tables
    instrument_lower = instrument.lower()
    if instrument_lower not in [i.lower() for i in instrument_tables.instrument_list]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid instrument name {instrument}, must be one of "
            + ",".join(instrument_tables.instrument_list),
        )
    return instrument_lower


####################
# Global app setup #
####################

app = FastAPI()
engine = setup_postgres()
logger = setup_logging(__name__)


########################
# Schema preload class #
########################


class InstrumentTables:
    """The column information for all tables in ConsDB schemas."""

    def __init__(self):
        inspector = sqlalchemy.inspect(engine)
        self.instrument_list = [name[4:] for name in inspector.get_schema_names() if name.startswith("cdb_")]
        self.table_names = set()
        self.schemas = dict()
        self.flexible_metadata_schemas = dict()
        self.obs_id_column = dict()
        for instrument in self.instrument_list:
            md = sqlalchemy.MetaData(schema=f"cdb_{instrument}")
            md.reflect(engine)
            self.table_names.update([str(table) for table in md.tables])
            self.schemas[instrument] = md
            self.obs_id_column[instrument] = dict()
            self.flexible_metadata_schemas[instrument] = dict()
            for table in md.tables:
                for col_name in ObsIdColname:
                    col_name = col_name.value
                    if col_name in md.tables[table].columns:
                        self.obs_id_column[instrument][table] = col_name
                        break
            for obs_type in ObsTypeEnum:
                obs_type = obs_type.value
                table_name = f"cdb_{instrument}.{obs_type}_flexdata"
                schema_table_name = table_name + "_schema"
                if table_name in md.tables and schema_table_name in md.tables:
                    schema_table = md.tables[schema_table_name]
                    stmt = sqlalchemy.select(schema_table.c["key", "dtype", "doc", "unit", "ucd"])
                    logger.debug(str(stmt))
                    schema = dict()
                    with engine.connect() as conn:
                        for row in conn.execute(stmt):
                            schema[row[0]] = row[1:]
                    self.flexible_metadata_schemas[instrument][obs_type] = schema

    def refresh_flexible_metadata_schema(self, instrument: str, obs_type: str):
        schema = dict()
        schema_table = self.get_flexible_metadata_schema(instrument, obs_type)
        stmt = sqlalchemy.select(schema_table.c["key", "dtype", "doc", "unit", "ucd"])
        logger.debug(str(stmt))
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

    def compute_wide_view_name(self, instrument: str, obs_type: str) -> str:
        """Compute the name of a wide view.

        The wide view joins all tables for a given instrument and observation
        type.

        Parameters
        ----------
        instrument: `str`
            Name of the instrument (e.g. ``LATISS``).
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        view_nae: `str`
            Name of the appropriate wide view.
        """
        instrument = instrument.lower()
        obs_type = obs_type.lower()
        if instrument not in self.schemas:
            raise BadValueException("instrument", instrument, list(self.schemas.keys()))
        view_name = f"cdb_{instrument}.{obs_type}_wide_view"
        if view_name not in self.schemas[instrument].tables:
            obs_type_list = [
                name[len(f"cdb_{instrument}.") : -len("_wide_view")]  # noqa: E203
                for name in self.schemas[instrument].tables
                if name.endswith("_wide_view")
            ]
            raise BadValueException("observation type", obs_type, obs_type_list)
        return view_name


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


'''
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
'''


###################################
# Web service application methods #
###################################


@internal_router.get(
    "/",
    description="Metadata and health check endpoint.",
    include_in_schema=False,
    response_model=Metadata,
    response_model_exclude_none=True,
    summary="Application metadata",
)
async def internal_root() -> Metadata:
    """Root URL for liveness checks.

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with a list of instruments, observation types, and
        data types.
    """
    return get_metadata(
        package_name="consdb-pqserver",
        application_name=config.name,
    )


class Index(BaseModel):
    """Metadata returned by the external root URL."""

    instruments: list[str] = Field(..., title="Available instruments")
    obs_types: list[str] = Field(..., title="Available observation types")
    dtypes: list[str] = Field(..., title="Allowed data types in flexible metadata")


@external_router.get(
    "/",
    description="Application root",
    response_model=Index,
    response_model_exclude_none=True,
    summary="Application root",
)
async def external_root() -> Index:
    """Application root URL /consdb/."""
    global instrument_tables

    logger.info(request)
    return Index(
        instruments=instrument_tables.instrument_list,
        obs_types=[o.value for o in ObsTypeEnum],
        dtypes=[d.value for d in AllowedTypesEnum],
    )


class AddKeyRequestModel(BaseModel):
    key: str = Field(..., title="The name of the added key")
    dtype: AllowedFlexTypeEnum = Field(..., title="Data type for the added key")
    doc: str = Field(..., title="Documentation string for the new key")
    unit: Optional[str] = Field(..., title="Unit for value")
    ucd: Optional[str] = Field(
        ..., title="IVOA Unified Content Descriptor (https://www.ivoa.net/documents/UCD1+/)"
    )

    @field_validator("unit")
    def validate_unit(v):
        try:
            unit = astropy.units.Unit(v)
        except ValueError:
            raise ValueError(f"'{v}' is a not a valid unit.")
        return v

    @field_validator("ucd")
    def validate_ucd(v):
        if not astropy.io.votable.ucd.check_ucd(v):
            raise ValueError(f"'{v}' is not a valid IVOA UCD.")
        return v


class AddKeyResponseModel(BaseModel):
    """Response model for the addkey endpoint."""

    message: str = Field(..., title="Human-readable response message")
    key: str = Field(..., title="The name of the added key")
    instrument: str = (Depends(validate_instrument_name),)
    obs_type: ObsTypeEnum = Field(..., title="The observation type that owns the new key")


@external_router.post(
    "/flex/{instrument}/{obs_type}/addkey",
    summary="Add a flexible metadata key for the specified instrument and obs_type.",
    response_model=AddKeyResponseModel,
)
async def add_flexible_metadata_key(
    instrument: Annotated[str, Depends(validate_instrument_name)],
    obs_type: ObsTypeEnum,
    data: AddKeyRequestModel,
) -> AddKeyResponseModel:
    """Add a key to a flexible metadata table."""
    global instrument_tables

    logger.info(f"{request} {request.json}")
    info = _check_json(request.json, "flex addkey", ("key", "dtype", "doc"))
    schema_table = instrument_tables.get_flexible_metadata_schema(instrument, obs_type)
    stmt = sqlalchemy.insert(schema_table).values(
        key=data.key,
        dtype=data.dtype,
        doc=data.doc,
        unit=data.unit,
        ucd=data.ucd,
    )
    logger.debug(str(stmt))
    with engine.connect() as conn:
        _ = conn.execute(stmt)
        conn.commit()
    # Update cached copy without re-querying database.
    instrument_tables.flexible_metadata_schemas[instrument.lower()][obs_type.lower()][key] = [
        data.dtype,
        data.doc,
        data.unit,
        data.ucd,
    ]
    return AddKeyResponse(
        message="Key added to flexible metadata",
        key=data.key,
        instrument=instrument,
        obs_type=data.obs_type,
    )


@external_router.get(
    "/flex/{instrument}/{obs_type}/schema",
    description="Flex schema for the given instrument and observation type.",
)
async def get_flexible_metadata_keys(
    instrument: Annotated[str, Depends(validate_instrument_name)],
    obs_type: ObsTypeEnum,
) -> dict[str, list[str | None]]:
    """Returns the flex schema for the given instrument and observation type."""
    global instrument_tables

    logger.info(request)
    instrument = instrument.lower()
    obs_type = obs_type.lower()
    _ = instrument_tables.compute_flexible_metadata_table_name(instrument, obs_type)
    instrument_tables.refresh_flexible_metadata_schema(instrument, obs_type)
    return instrument_tables.flexible_metadata_schemas[instrument][obs_type]


@external_router.get(
    "/flex/{instrument}/{obs_type}/obs/{obs_id}",
    description="Flex schema for the given instrument and observation type.",
)
async def get_flexible_metadata(
    instrument: Annotated[str, Depends(validate_instrument_name)],
    obs_type: ObsTypeEnum,
    obs_id: ObservationIdType,
) -> dict[str, AllowedFlexType]:
    """Retrieve values for an observation from a flexible metadata table."""
    global instrument_tables

    logger.info(request)
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
            result[key] = convert_to_flex_type(AllowedFlexTypeEnum(key), value)
    return result


class GenericResponse(BaseModel):
    message: str = Field(..., title="Human-readable response message")
    instrument: str = Field(..., title="Instrument name (e.g., ``LATISS``)")
    obs_type: ObsTypeEnum = Field(..., title="The observation type (e.g., ``exposure``)")
    obs_id: ObservationIdType | list[ObservationIdType] = Field(..., title="Observation ID")
    table: Optional[str] = Field(..., title="Table name")


@external_router.post("/flex/{instrument}/{obs_type}/obs/{obs_id}")
def insert_flexible_metadata(
    instrument: Annotated[str, Depends(validate_instrument_name)],
    obs_type: ObsTypeEnum,
    obs_id: ObservationIdType,
) -> GenericResponse:
    """Insert or update key/value pairs in a flexible metadata table."""
    global instrument_tables

    logger.info(f"{request} {request.json}")
    info = _check_json(request.json, "flex obs", ("values",))
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
        if dtype != type(value).__name__:
            raise BadValueException(f"{dtype} value", value)

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
    return GenericResponse(
        message="Flexible metadata inserted",
        obs_id=obs_id,
        instrument=instrument,
        obs_type=obs_type,
    )


@external_router.post("/insert/{instrument}/{table}/obs/{obs_id}")
def insert(
    instrument: Annotated[str, Depends(validate_instrument_name)],
    table: str,
    obs_id: ObservationIdType,
) -> GenericResponse:
    """Insert or update column/value pairs in a ConsDB table."""
    global instrument_tables

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
    return GenericResponse(
        message="Data inserted",
        instrument=instrument,
        table=table_name,
        obs_id=obs_id,
    )


@external_router.post("/insert/{instrument}/{table}")
def insert_multiple(
    instrument: Annotated[str, Depends(validate_instrument_name)],
    table: str,
) -> dict[str, Any] | tuple[dict[str, str], int]:
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
    global instrument_tables

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
            if not isinstance(obs_id, ObservationIdType):
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

    return GenericResponse(
        message="Data inserted",
        table=table_name,
        instrument=instrument,
        obs_id=info["obs_dict"].keys(),
    )


@external_router.get("/query/{instrument}/{obs_type}/obs/{obs_id}")
def get_all_metadata(
    instrument: Annotated[str, Depends(validate_instrument_name)],
    obs_type: ObsTypeEnum,
    obs_id: ObservationIdType,
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
    flex: `str`
        Include flexible metadata if set to "1" (URL query parameter).

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with 200 HTTP status on success.
        Response is a dict with columns as keys.

    Raises
    ------
    """
    global instrument_tables

    logger.info(request)
    instrument = instrument.lower()
    obs_type = obs_type.lower()
    view_name = instrument_tables.compute_wide_view_name(instrument, obs_type)
    view = instrument_tables.schemas[view_name]
    obs_id_column = instrument_tables.obs_id_column[instrument][view_name]
    stmt = sqlalchemy.select(view).where(view.c[obs_id_column] == obs_id)
    logger.debug(str(stmt))
    result = dict()
    with engine.connect() as conn:
        rows = conn.execute(stmt).all()
        assert len(rows) == 1
        result = dict(rows[0]._mapping)
    if request.args and "flex" in request.args and request.args["flex"] == "1":
        flex_result = get_flexible_metadata(instrument, obs_type, obs_id)
        result.update(flex_result)
    return result


@external_router.post("/query")
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
        result: dict[str, Any] = {}
        rows = []
        for row in cursor:
            if first:
                result["columns"] = list(row._fields)
                first = False
            rows.append(list(row))
        result["data"] = rows
    return result


@external_router.get("/schema")
def list_instruments() -> list[str]:
    """Retrieve the list of instruments available in ConsDB."""
    global instrument_tables

    logger.info(request)
    return instrument_tables.instrument_list


@external_router.get("/consdb/schema/{instrument}")
def list_table(
    instrument: Annotated[str, Depends(validate_instrument_name)],
) -> list[str]:
    """Retrieve the list of tables for an instrument."""
    global instrument_tables

    logger.info(request)
    schema = instrument_tables.schemas[instrument]
    return list(schema.tables.keys())


@external_router.get("/schema/{instrument}/<table>")
def schema(instrument: Annotated[str, Depends(validate_instrument_name)], table: str) -> dict[str, list[str]]:
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
    global instrument_tables

    logger.info(request)
    schema = instrument_tables.schemas[instrument]
    if not table.startswith(f"cdb_{instrument}."):
        table = f"cdb_{instrument}.{table}"
    table = table.lower()
    if table not in schema.tables:
        raise BadValueException("table", table, list(schema.tables.keys()))
    return {c.name: [str(c.type), c.doc] for c in schema.tables[table].columns}
