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

from enum import StrEnum
from typing import Annotated, Any, Optional

import astropy
import sqlalchemy
import sqlalchemy.dialects.postgresql
from fastapi import Body, FastAPI, Path, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from packaging.version import Version
from pydantic import AfterValidator, BaseModel, Field, field_validator

from .utils import setup_logging, setup_postgres


class ObsTypeEnum(StrEnum):
    EXPOSURE = "exposure"
    VISIT1 = "visit1"
    CCD_EXPOSURE = "ccdexposure"
    CCD_VISIT1 = "ccdvisit1"

    @classmethod
    def _missing_(cls, value):
        """Makes the enum case-insensitive, see
        https://docs.python.org/3/library/enum.html
        """
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None


ObservationIdType = int


# This shenanigan makes flake8 recognize AllowedFlexTypeEnum as a type.
AllowedFlexType = bool | int | float | str
AllowedFlexTypeEnumBase = StrEnum(
    "AllowedFlexTypeEnumBase", {t.__name__.upper(): t.__name__ for t in AllowedFlexType.__args__}
)
AllowedFlexTypeEnum = AllowedFlexTypeEnumBase


def convert_to_flex_type(ty: AllowedFlexTypeEnum, v: str) -> AllowedFlexType:
    """Converts a string containing a flex database value into the
    appropriate type.

    Raises
    ======
    ValueError if the conversion is invalid
    """
    if ty.value == "bool":  # Special case
        return v.lower() in ("true", "t", "1")
    m = [t for t in AllowedFlexType.__args__ if t.__name__ == ty.value]
    assert len(m) == 1
    return m[0](v)


class ObsIdColname(StrEnum):
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


####################
# Global app setup #
####################

path_prefix = "/consdb"
app = FastAPI(
    title="consdb-pqserver",
    description="HTTP API for consdb",
    openapi_url=f"{path_prefix}/openapi.json",
    docs_url=f"{path_prefix}/docs",
    redoc_url=f"{path_prefix}/redoc",
)
engine = None
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
        self.timestamp_columns = dict()
        for instrument in self.instrument_list:
            md = sqlalchemy.MetaData(schema=f"cdb_{instrument}")
            md.reflect(engine)
            self.table_names.update([str(table) for table in md.tables])
            self.schemas[instrument] = md
            self.obs_id_column[instrument] = dict()
            self.flexible_metadata_schemas[instrument] = dict()
            for table in md.tables:
                # Find all timestamp columns in the table
                self.timestamp_columns[table] = set(
                    [
                        column.name
                        for column in md.tables[table].columns
                        if isinstance(column.type, sqlalchemy.DateTime)
                    ]
                )

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

    def get_timestamp_columns(self, table: str) -> set[str]:
        """Returns a set containing all timestamp columns.

        Given the instrument and table name, returns a set
        of strings listing all the columns in the table that
        are a timestamp.

        Parameters
        ----------
        table : `str`
            The name of the table, e.g., "cdb_latiss.exposure".

        Returns
        -------
        `set[str]`
            The names of all timestamp columns in the table.
        """
        columns = self.timestamp_columns[table]
        return columns


    def get_schema_version(self, instrument: str) -> Version:
        if "day_obs" in self.schemas[instrument].tables[f"cdb_{instrument}.ccdexposure"].columns:
            return Version("3.2.0")
        else:
            return Version("3.1.0")

    def get_day_obs_and_seq_num(self, instrument: str, exposure_id: int) -> tuple[int, int]:
        exposure_table_name = f"cdb_{instrument}.exposure"
        exposure_table = self.schemas[instrument].tables[exposure_table_name]
        query = sqlalchemy.select(
            exposure_table.c.day_obs, exposure_table.c.seq_num
        ).where(
            exposure_table.c.exposure_id == exposure_id
        )

        with engine.connect() as conn:
            query_result = conn.execute(query).first()

        if not query_result:
            raise BadValueException(f"Exposure ID: {exposure_id} - no such exposure ID")
        return (query_result.day_obs, query_result.seq_num)

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
        view_name: `str`
            Name of the appropriate wide view.
        """
        instrument = instrument.lower()
        obs_type = obs_type.lower()
        view_name = f"cdb_{instrument}.{obs_type}_wide_view"
        if view_name not in self.schemas[instrument].tables:
            obs_type_list = [
                name[len(f"cdb_{instrument}.") : -len("_wide_view")]  # noqa: E203
                for name in self.schemas[instrument].tables
                if name.endswith("_wide_view")
            ]
            raise BadValueException("observation type", obs_type, obs_type_list)
        return view_name


engine = None
instrument_tables = None
if __name__ == "__main__" or __name__ == "consdb_pq.pqserver":
    engine = setup_postgres()
    instrument_tables = InstrumentTables()


##################
# Error handling #
##################


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


class UnknownInstrumentException(Exception):
    """Exception raised for an unknown instrument.

    Parameters
    ----------
    instrument: `str`
        Name of the unknown instrument.
    """

    status_code = 404

    def __init__(self, instrument: str):
        self.instrument = instrument

    def to_dict(self) -> dict[str, Any]:
        """Convert the exception to a dictionary for JSON conversion.

        Returns
        -------
        json_dict: `dict` [ `str`, `Any` ]
            Dictionary with a message and the unknown instrument name.
        """
        return {
            "message": "Unknown instrument",
            "value": self.instrument,
            "valid": instrument_tables.instrument_list,
        }


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"RequestValidationError {request}: {exc_str}")
    content = {"message": "Validation error", "detail": exc.errors()}
    return JSONResponse(content=content, status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(UnknownInstrumentException)
def unknown_instrument_exception_handler(request: Request, exc: UnknownInstrumentException):
    logger.error(f"UnknownInstrumentException {request}: {exc.instrument}")
    return JSONResponse(content=exc.to_dict(), status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(BadValueException)
def bad_value_exception_handler(request: Request, exc: BadValueException):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"BadValueException {request}: {exc_str}")
    return JSONResponse(content=exc.to_dict(), status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(sqlalchemy.exc.SQLAlchemyError)
def sqlalchemy_exception_handler(request: Request, exc: sqlalchemy.exc.SQLAlchemyError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"SQLAlchemyError {request}: {exc_str}")
    content = {"message": str(exc)}
    return JSONResponse(content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validate_instrument_name(
    instrument: str = Path(description="Must be a valid instrument name (e.g., ``LATISS``)"),
) -> str:
    global instrument_tables
    instrument_lower = instrument.lower()
    if instrument_lower not in [i.lower() for i in instrument_tables.instrument_list]:
        raise UnknownInstrumentException(instrument)
    return instrument


InstrumentName = Annotated[str, AfterValidator(validate_instrument_name)]


###################################
# Web service application methods #
###################################


class IndexResponseModel(BaseModel):
    """Metadata returned by the external root URL."""

    instruments: list[str] = Field(title="Available instruments")
    obs_types: list[str] = Field(title="Available observation types")
    dtypes: list[str] = Field(title="Allowed data types in flexible metadata")


@app.get(
    "/",
    description="Metadata and health check endpoint.",
    include_in_schema=False,
    summary="Application metadata",
)
def internal_root() -> IndexResponseModel:
    """Root URL for liveness checks.

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with a list of instruments, observation types, and
        data types.
    """
    global instrument_tables

    return IndexResponseModel(
        instruments=instrument_tables.instrument_list,
        obs_types=[o.value for o in ObsTypeEnum],
        dtypes=[d.value for d in AllowedFlexTypeEnum],
    )


@app.get(
    "/consdb/",
    description="Application root",
    summary="Application root",
)
def external_root() -> IndexResponseModel:
    """Application root URL /consdb/."""
    global instrument_tables

    return IndexResponseModel(
        instruments=instrument_tables.instrument_list,
        obs_types=[o.value for o in ObsTypeEnum],
        dtypes=[d.value for d in AllowedFlexTypeEnum],
    )


class AddKeyRequestModel(BaseModel):
    key: str = Field(title="The name of the added key")
    dtype: AllowedFlexTypeEnum = Field(title="Data type for the added key")
    doc: Optional[str] = Field("", title="Documentation string for the new key")
    unit: Optional[str] = Field(None, title="Unit for value")
    ucd: Optional[str] = Field(
        None, title="IVOA Unified Content Descriptor (https://www.ivoa.net/documents/UCD1+/)"
    )

    @field_validator("unit")
    def validate_unit(v: str):
        try:
            _ = astropy.units.Unit(v)
        except ValueError:
            raise ValueError(f"'{v}' is a not a valid unit.")
        return v

    @field_validator("ucd")
    def validate_ucd(v: str):
        if not astropy.io.votable.ucd.check_ucd(v):
            raise ValueError(f"'{v}' is not a valid IVOA UCD.")
        return v


class AddKeyResponseModel(BaseModel):
    """Response model for the addkey endpoint."""

    message: str = Field(title="Human-readable response message")
    key: str = Field(title="The name of the added key")
    instrument: InstrumentName = Field(title="The instrument name")
    obs_type: ObsTypeEnum = Field(title="The observation type that owns the new key")


@app.post(
    "/consdb/flex/{instrument}/{obs_type}/addkey",
    summary="Add a flexible metadata key",
    description="Add a flexible metadata key for the specified instrument and obs_type.",
)
def add_flexible_metadata_key(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum,
    data: AddKeyRequestModel,
) -> AddKeyResponseModel:
    """Add a key to a flexible metadata table."""
    global instrument_tables

    instrument_l = instrument.lower()
    schema_table = instrument_tables.get_flexible_metadata_schema(instrument_l, obs_type)
    stmt = sqlalchemy.insert(schema_table).values(
        key=data.key,
        dtype=data.dtype.value,
        doc=data.doc,
        unit=data.unit,
        ucd=data.ucd,
    )
    logger.debug(str(stmt))
    with engine.connect() as conn:
        _ = conn.execute(stmt)
        conn.commit()
    # Update cached copy without re-querying database.
    instrument_tables.flexible_metadata_schemas[instrument_l][obs_type.lower()][data.key] = [
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


class FlexMetadataSchemaResponseModel(BaseModel):
    schema_: dict[str, tuple[AllowedFlexTypeEnum, str, str | None, str | None]] = Field(
        title="""
            Dictionary containing each flex key name
            and its associated data type, documentation, unit, and UCD
        """,
        alias="schema",
    )


class FlexibleMetadataInfo(BaseModel):
    dtype: str = Field(title="Data type for the key")
    doc: str = Field(title="Documentation string for the key")
    unit: str | None = Field(None, title="Unit for value")
    ucd: str | None = Field(None, title="IVOA Unified Content Descriptor")


@app.get(
    "/consdb/flex/{instrument}/{obs_type}/schema",
    summary="Get all flexible metadata keys",
    description="Flex schema for the given instrument and observation type.",
)
def get_flexible_metadata_keys(
    instrument: InstrumentName = Path(title="Instrument name"),
    obs_type: ObsTypeEnum = Path(title="Observation type"),
) -> dict[str, tuple[str, str, str | None, str | None]]:
    """Returns the flex schema for the given instrument and
    observation type.
    """
    global instrument_tables

    instrument = instrument.lower()
    obs_type = obs_type.lower()
    _ = instrument_tables.compute_flexible_metadata_table_name(instrument, obs_type)
    instrument_tables.refresh_flexible_metadata_schema(instrument, obs_type)

    return instrument_tables.flexible_metadata_schemas[instrument][obs_type]


@app.get(
    "/consdb/flex/{instrument}/{obs_type}/obs/{obs_id}",
    description="Flex schema for the given instrument and observation type.",
)
def get_flexible_metadata(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum = Path(title="Observation type"),
    obs_id: ObservationIdType = Path(title="Observation ID"),
    k: list[str] = Query([], title="Columns to retrieve"),
) -> dict[str, AllowedFlexType]:
    """Retrieve values for an observation from a flexible metadata table."""
    global instrument_tables

    instrument_l = instrument.lower()
    table = instrument_tables.get_flexible_metadata_table(instrument_l, obs_type)
    schema = instrument_tables.flexible_metadata_schemas[instrument_l][obs_type]
    result = dict()
    stmt = sqlalchemy.select(table.c["key", "value"]).where(table.c.obs_id == obs_id)
    if len(k) > 0:
        stmt = stmt.where(table.c.key.in_(k))
    logger.debug(str(stmt))
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            key, value = row
            if key not in schema:
                instrument_tables.refresh_flexible_metadata_schema(instrument_l, obs_type)
            schema = instrument_tables.flexible_metadata_schemas[instrument_l][obs_type]
            dtype = schema[key][0]
            result[key] = convert_to_flex_type(AllowedFlexTypeEnum(dtype), value)
    return result


class InsertDataModel(BaseModel):
    """This model can be used for either flex or regular data."""

    values: dict[str, AllowedFlexType] = Field(title="Data to insert or update")


class InsertFlexDataResponse(BaseModel):
    message: str = Field(title="Human-readable response message")
    instrument: str = Field(title="Instrument name (e.g., ``LATISS``)")
    obs_type: ObsTypeEnum = Field(title="The observation type (e.g., ``exposure``)")
    obs_id: ObservationIdType | list[ObservationIdType] = Field(title="Observation ID")


@app.post("/consdb/flex/{instrument}/{obs_type}/obs/{obs_id}")
def insert_flexible_metadata(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum,
    obs_id: ObservationIdType,
    data: InsertDataModel = Body(title="Data to insert or update"),
    u: Optional[int] = Query(0, title="Update if exists"),
) -> InsertFlexDataResponse:
    """Insert or update key/value pairs in a flexible metadata table."""
    global instrument_tables

    instrument_l = instrument.lower()
    table = instrument_tables.get_flexible_metadata_table(instrument_l, obs_type)
    schema = instrument_tables.flexible_metadata_schemas[instrument_l][obs_type]

    value_dict = data.values
    if any(key not in schema for key in value_dict):
        instrument_tables.refresh_flexible_metadata_schema(instrument_l, obs_type)
        schema = instrument_tables.flexible_metadata_schemas[instrument_l][obs_type]
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

            values = {"obs_id": obs_id, "key": key, "value": value_str}
            if instrument_tables.get_schema_version(instrument_l) >= Version("3.2.0"):
                day_obs, seq_num = instrument_tables.get_day_obs_and_seq_num(instrument_l, obs_id)
                values["day_obs"] = day_obs
                values["seq_num"] = seq_num

            stmt: sqlalchemy.sql.dml.Insert
            stmt = sqlalchemy.dialects.postgresql.insert(table).values(**values)
            logger.error(f"{u=}")
            if u != 0:
                stmt = stmt.on_conflict_do_update(index_elements=["obs_id", "key"], set_={"value": value_str})

            logger.debug(str(stmt))
            _ = conn.execute(stmt)

        conn.commit()
    return InsertFlexDataResponse(
        message="Flexible metadata inserted",
        instrument=instrument,
        obs_type=obs_type,
        obs_id=obs_id,
    )


class InsertDataResponse(BaseModel):
    message: str = Field(title="Human-readable response message")
    instrument: str = Field(title="Instrument name (e.g., ``LATISS``)")
    obs_id: ObservationIdType | list[ObservationIdType] = Field(title="Observation ID")
    table: str = Field(title="Table name")


@app.post(
    "/consdb/insert/{instrument}/{table}/obs/{obs_id}",
    summary="Insert data row",
)
def insert(
    instrument: InstrumentName,
    table: str,
    obs_id: ObservationIdType,
    data: InsertDataModel = Body(title="Data to insert or update"),
    u: Optional[int] = Query(0, title="Update if data already exist"),
) -> InsertDataResponse:
    """Insert or update column/value pairs in a ConsDB table."""
    global instrument_tables

    instrument_l = instrument.lower()
    schema = f"cdb_{instrument_l}."
    table_name = table.lower()
    if not table.lower().startswith(schema):
        table_name = schema + table_name
    table_obj = instrument_tables.schemas[instrument_l].tables[table_name]

    valdict = data.values
    obs_id_colname = instrument_tables.obs_id_column[instrument_l][table_name]
    valdict[obs_id_colname] = obs_id

    # If needed, cross-reference day_obs and seq_num from the exposure table.
    if "day_obs" in table_obj.columns and "seq_num" in table_obj.columns:
        if "day_obs" not in valdict or "seq_num" not in valdict:
            day_obs, seq_num = instrument_tables.get_day_obs_and_seq_num(instrument_l, obs_id)
            if "day_obs" not in valdict:
                valdict["day_obs"] = day_obs
            if "seq_num" not in valdict:
                valdict["seq_num"] = seq_num

    stmt: sqlalchemy.sql.dml.Insert
    stmt = sqlalchemy.dialects.postgresql.insert(table_obj).values(valdict)
    if u != 0:
        stmt = stmt.on_conflict_do_update(index_elements=[obs_id_colname], set_=valdict)
    logger.debug(str(stmt))
    with engine.connect() as conn:
        _ = conn.execute(stmt)
        conn.commit()
    return InsertDataResponse(
        message="Data inserted",
        instrument=instrument,
        obs_id=obs_id,
        table=table_name,
    )


class InsertMultipleRequestModel(BaseModel):
    obs_dict: dict[ObservationIdType, dict[str, AllowedFlexType]] = Field(
        title="Observation ID and key/value pairs to insert or update"
    )


class InsertMultipleResponseModel(BaseModel):
    message: str = Field(title="Human-readable response message")
    instrument: str = Field(title="Instrument name (e.g., ``LATISS``)")
    obs_id: ObservationIdType | list[ObservationIdType] = Field(title="Observation ID")
    table: str = Field(title="Table name")


@app.post(
    "/consdb/insert/{instrument}/{table}",
    summary="Insert multiple data rows",
)
def insert_multiple(
    instrument: InstrumentName,
    table: str,
    data: InsertMultipleRequestModel = Body(title="Data to insert or update"),
    u: Optional[int] = Query(0, title="Update if data already exist"),
) -> InsertMultipleResponseModel:
    """Insert or update multiple observations in a ConsDB table.

    Raises
    ------
    BadJsonException
        Raised if JSON is absent or missing a required key.

    BadValueException
        Raised if instrument or observation type is invalid.
    """
    global instrument_tables

    instrument_l = instrument.lower()
    schema = f"cdb_{instrument_l}."
    table_name = table.lower()
    if not table.lower().startswith(schema):
        table_name = schema + table_name
    table_obj = instrument_tables.schemas[instrument_l].tables[table_name]
    table_name = f"cdb_{instrument_l}." + table.lower()
    obs_id_colname = instrument_tables.obs_id_column[instrument_l][table_name]

    timestamp_columns = instrument_tables.get_timestamp_columns(table_name)

    with engine.connect() as conn:
        for obs_id, valdict in data.obs_dict.items():
            valdict[obs_id_colname] = obs_id

            # If needed, cross-reference day_obs and seq_num from the
            # exposure table.
            if "day_obs" in table_obj.columns and "seq_num" in table_obj.columns:
                if "day_obs" not in valdict or "seq_num" not in valdict:
                    day_obs, seq_num = instrument_tables.get_day_obs_and_seq_num(instrument_l, obs_id)
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

            stmt: sqlalchemy.sql.dml.Insert
            stmt = sqlalchemy.dialects.postgresql.insert(table_obj).values(valdict)
            if u != 0:
                stmt = stmt.on_conflict_do_update(index_elements=[obs_id_colname], set_=valdict)
            logger.debug(str(stmt))
            # TODO: optimize as executemany
            _ = conn.execute(stmt)
        conn.commit()

    return InsertMultipleResponseModel(
        message="Data inserted",
        table=table,
        instrument=instrument,
        obs_id=data.obs_dict.keys(),
    )


@app.get(
    "/consdb/query/{instrument}/{obs_type}/obs/{obs_id}",
    summary="Get all metadata",
    description="Get all metadata for a given observation.",
)
def get_all_metadata(
    instrument: InstrumentName,
    obs_type: ObsTypeEnum,
    obs_id: ObservationIdType,
    flex: Optional[int] = Query(0, title="Include flexible metadata"),
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
    if flex != 0:
        flex_result = get_flexible_metadata(instrument, obs_type, obs_id)
        result.update(flex_result)
    return result


class QueryRequestModel(BaseModel):
    query: str = Field(title="SQL query string")


class QueryResponseModel(BaseModel):
    columns: list[str] = Field(title="Column names")
    data: list[Any] = Field(title="Data rows")


@app.post("/consdb/query")
def query(
    data: QueryRequestModel = Body(title="SQL query string"),
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
    with engine.connect() as conn:
        cursor = conn.exec_driver_sql(data.query)
        first = True
        for row in cursor:
            logger.debug(row)
            if first:
                columns.extend(row._fields)
                first = False
            rows.append(list(row))

    return QueryResponseModel(
        columns=columns,
        data=rows,
    )


@app.get("/consdb/schema")
def list_instruments() -> list[str]:
    """Retrieve the list of instruments available in ConsDB."""
    global instrument_tables

    return instrument_tables.instrument_list


@app.get("/consdb/schema/{instrument}")
def list_table(
    instrument: InstrumentName,
) -> list[str]:
    """Retrieve the list of tables for an instrument."""
    global instrument_tables

    schema = instrument_tables.schemas[instrument.lower()]
    return list(schema.tables.keys())


@app.get("/consdb/schema/{instrument}/{table}")
def schema(
    instrument: InstrumentName = Path(description="Instrument name"),
    table: str = Path(description="Table name to retrieve schema"),
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
    global instrument_tables

    instrument_l = instrument.lower()
    schema = instrument_tables.schemas[instrument_l]
    if not table.startswith(f"cdb_{instrument_l}."):
        table = f"cdb_{instrument_l}.{table}"
    table = table.lower()
    if table not in schema.tables:
        raise BadValueException("table", table, list(schema.tables.keys()))
    return {c.name: [str(c.type), c.doc] for c in schema.tables[table].columns}
