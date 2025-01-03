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

import astropy
from pydantic import BaseModel, Field, field_validator
from safir.metadata import Metadata
from typing import Any

from .cdb_schema import AllowedFlexType, AllowedFlexTypeEnum, ObservationIdType, ObsTypeEnum
from .dependencies import InstrumentName


class IndexResponseModel(Metadata):
    """Metadata returned by the external root URL."""

    instruments: list[str] = Field(title="Available instruments")
    obs_types: list[str] = Field(title="Available observation types")
    dtypes: list[str] = Field(title="Allowed data types in flexible metadata")


class AddKeyRequestModel(BaseModel):
    key: str = Field(title="The name of the added key")
    dtype: AllowedFlexTypeEnum = Field(title="Data type for the added key")
    doc: str | None = Field("", title="Documentation string for the new key")
    unit: str | None = Field(None, title="Unit for value")
    ucd: str | None = Field(
        None, title="IVOA Unified Content Descriptor (https://www.ivoa.net/documents/UCD1+/)"
    )

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, v: str, values):
        try:
            _ = astropy.units.Unit(v)
        except ValueError:
            raise ValueError(f"'{v}' is a not a valid unit.")
        return v

    @field_validator("ucd")
    @classmethod
    def validate_ucd(cls, v: str, values):
        if not astropy.io.votable.ucd.check_ucd(v):
            raise ValueError(f"'{v}' is not a valid IVOA UCD.")
        return v


class AddKeyResponseModel(BaseModel):
    """Response model for the addkey endpoint."""

    message: str = Field(title="Human-readable response message")
    key: str = Field(title="The name of the added key")
    instrument: InstrumentName = Field(title="The instrument name")
    obs_type: ObsTypeEnum = Field(title="The observation type that owns the new key")


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


class InsertDataModel(BaseModel):
    """This model can be used for either flex or regular data."""

    values: dict[str, AllowedFlexType] = Field(title="Data to insert or update")


class InsertFlexDataResponse(BaseModel):
    message: str = Field(title="Human-readable response message")
    instrument: str = Field(title="Instrument name (e.g., ``LATISS``)")
    obs_type: ObsTypeEnum = Field(title="The observation type (e.g., ``exposure``)")
    obs_id: ObservationIdType | list[ObservationIdType] = Field(title="Observation ID")


class InsertDataResponse(BaseModel):
    message: str = Field(title="Human-readable response message")
    instrument: str = Field(title="Instrument name (e.g., ``LATISS``)")
    obs_id: ObservationIdType | list[ObservationIdType] = Field(title="Observation ID")
    table: str = Field(title="Table name")


class InsertMultipleRequestModel(BaseModel):
    obs_dict: dict[ObservationIdType, dict[str, AllowedFlexType]] = Field(
        title="Observation ID and key/value pairs to insert or update"
    )


class InsertMultipleResponseModel(BaseModel):
    message: str = Field(title="Human-readable response message")
    instrument: str = Field(title="Instrument name (e.g., ``LATISS``)")
    obs_id: ObservationIdType | list[ObservationIdType] = Field(title="Observation ID")
    table: str = Field(title="Table name")


class QueryRequestModel(BaseModel):
    query: str = Field(title="SQL query string")


class QueryResponseModel(BaseModel):
    columns: list[str] = Field(title="Column names")
    data: list[Any] = Field(title="Data rows")
