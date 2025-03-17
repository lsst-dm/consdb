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
from enum import StrEnum
from typing import Generator

import sqlalchemy
import sqlalchemy.dialects.postgresql
from packaging.version import Version
from sqlalchemy.orm import Session

from .exceptions import BadValueException


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

    if len(m) != 1:
        raise ValueError(f"Invalid type {ty.value} for conversion")

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


########################
# Schema preload class #
########################


class InstrumentTable:
    """The column information for a single table in ConsDB schemas."""

    def __init__(
        self,
        *,
        engine: sqlalchemy.Engine,
        get_db: Generator[Session, None, None],
        instrument: str,
        logger: logging.Logger,
    ):
        self.instrument = instrument.lower()
        self.logger = logger
        self.get_db = get_db

        self.table_names = set()
        self.schemas = dict()
        self.flexible_metadata_schemas = dict()
        self.obs_id_column = dict()
        self.timestamp_columns = dict()

        md = sqlalchemy.MetaData(schema=f"cdb_{self.instrument}")
        md.reflect(engine, views=True)
        self.table_names.update([str(table) for table in md.tables])
        self.schemas = md
        for table in md.tables:
            # Find all timestamp columns in the table
            self.timestamp_columns[table] = set(
                [
                    column.name
                    for column in md.tables[table].columns
                    if isinstance(column.type, sqlalchemy.DateTime)
                ]
            )

            # Compile the list of obs id column names for
            # each table.
            for col_name in ObsIdColname:
                # If there are multiple observation ID columns in a table,
                # this breaks ties by selecting the first one found based
                # on the ordering defined in the ObsIdColname enum.
                col_name = col_name.value
                if col_name in md.tables[table].columns:
                    self.obs_id_column[table] = col_name
                    break

        for obs_type in ObsTypeEnum:
            obs_type = obs_type.value.lower()
            table_name = f"cdb_{self.instrument}.{obs_type}_flexdata"
            schema_table_name = table_name + "_schema"
            if table_name in md.tables and schema_table_name in md.tables:
                self.flexible_metadata_schemas[obs_type] = None
                self.refresh_flexible_metadata_schema(obs_type)

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

    def get_schema_version(self) -> Version:
        if "day_obs" in self.schemas.tables[f"cdb_{self.instrument}.ccdexposure"].columns:
            return Version("3.2.0")
        else:
            return Version("3.1.0")

    def get_day_obs_and_seq_num(self, exposure_id: int) -> tuple[int, int]:
        exposure_table_name = f"cdb_{self.instrument}.exposure"
        exposure_table = self.schemas.tables[exposure_table_name]
        query = sqlalchemy.select(exposure_table.c.day_obs, exposure_table.c.seq_num).where(
            exposure_table.c.exposure_id == exposure_id
        )

        db = next(self.get_db())
        query_result = db.execute(query).first()

        if not query_result:
            raise BadValueException(f"Exposure ID: {exposure_id} - no such exposure ID")
        return (query_result.day_obs, query_result.seq_num)

    def refresh_flexible_metadata_schema(self, obs_type: str):
        schema = dict()
        schema_table = self.get_flexible_metadata_schema(obs_type)
        stmt = sqlalchemy.select(schema_table.c["key", "dtype", "doc", "unit", "ucd"])
        self.logger.debug(str(stmt))
        db = next(self.get_db())
        for row in db.execute(stmt):
            schema[row[0]] = row[1:]
        self.flexible_metadata_schemas[obs_type] = schema

    def compute_flexible_metadata_table_name(self, obs_type: str) -> str:
        """Compute the name of a flexible metadata table.

        Each instrument and observation type made with that instrument can
        have a flexible metadata table.

        Parameters
        ----------
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
        obs_type = obs_type.lower()
        if obs_type not in self.flexible_metadata_schemas:
            raise BadValueException(
                "observation type",
                obs_type,
                list(self.flexible_metadata_schemas.keys()),
            )
        return f"cdb_{self.instrument}.{obs_type}_flexdata"

    def compute_flexible_metadata_table_schema_name(self, obs_type: str) -> str:
        """Compute the name of a flexible metadata schema table.

        The schema table contains descriptions of all keys in the flexible
        metadata table for the instrument and observation type.

        Parameters
        ----------
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        schema_table_name: `str`
            Name of the appropriate flexible metadata schema table.
        """
        table_name = self.compute_flexible_metadata_table_name(obs_type)
        return table_name + "_schema"

    def get_flexible_metadata_table(self, obs_type: str) -> sqlalchemy.schema.Table:
        """Get the table object for a flexible metadata table.

        Parameters
        ----------
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        table_obj: `sqlalchemy.schema.Table`
            ``Table`` object for the flexible metadata table.
        """
        obs_type = obs_type.lower()
        table_name = self.compute_flexible_metadata_table_name(obs_type)
        return self.schemas.tables[table_name]

    def get_flexible_metadata_schema(self, obs_type: str):
        """Get the table object for a flexible metadata schema table.

        Parameters
        ----------
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        schema_table_obj: `sqlalchemy.schema.Table`
            ``Table`` object for the flexible metadata schema table.
        """
        obs_type = obs_type.lower()
        table_name = self.compute_flexible_metadata_table_schema_name(obs_type)
        return self.schemas.tables[table_name]

    def compute_wide_view_name(self, obs_type: str) -> str:
        """Compute the name of a wide view.

        The wide view joins all tables for a given instrument and observation
        type.

        Parameters
        ----------
        obs_type: `str`
            Name of the observation type (e.g. ``Exposure``).

        Returns
        -------
        view_name: `str`
            Name of the appropriate wide view.
        """
        obs_type = obs_type.lower()
        view_name = f"cdb_{self.instrument}.{obs_type}_wide_view"
        if view_name not in self.schemas.tables:
            obs_type_list = [
                name[len(f"cdb_{self.instrument}.") : -len("_wide_view")]  # noqa: E203
                for name in self.schemas.tables
                if name.endswith("_wide_view")
            ]
            raise BadValueException("observation type", obs_type, obs_type_list)
        return view_name
