# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Defines the configuration models used in the application."""

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, model_validator

TABLES = [
    "exposure_efd",
    "exposure_efd_unpivoted",
    "visit1_efd",
    "visit1_efd_unpivoted",
]
UNPIVOTED_TABLES = ["exposure_efd_unpivoted", "visit1_efd_unpivoted"]


class Field(BaseModel):
    """Represents a field with a name.

    Attributes
    ----------
        name (str): The name of the field.

    """

    name: str


class Topic(BaseModel):
    """Represents a topic with a name and associated fields.

    Attributes
    ----------
        name (str): The name of the topic.
        fields (List[Field]): A list of fields associated with the topic.

    """

    name: str
    fields: List[Field]


class Column(BaseModel):
    """Represents a column with a name and optional tables.

    Attributes
    ----------
        name (str): The name of the column.
        tables (Optional[List[str]]): A list of table names where the column
            exists.
        store_unpivoted (Optional[bool]): Flag indicating whether to store
            column in unpivoted format. Defaults to False.
        function (str): The transformation function to apply to the column.
        function_args (Optional[Dict]): A dictionary of arguments for the
            transformation function.
        datatype (str): The data type of the column. Must match the
            Felis type.
        unit (str): The unit of the column.
        description (str): A description of the column.
        packed_series (bool): Flag indicating whether the column will process
            a packed series.
        subset_field (Optional[str]): The field (InfluxDB column) used to
            filter data during the transformation.
        subset_value (Optional[Union[str, int]]): The value of the field used
            to filter data during the transformation.
        topics (List[Topic]): The EFD topic(s) used in the transformation.

    """

    name: str
    tables: Optional[List[str]] = TABLES
    store_unpivoted: Optional[bool] = False
    function: str
    function_args: Optional[Dict] = None
    datatype: str
    unit: str
    description: str
    packed_series: bool
    subset_field: Optional[str] = None
    subset_value: Optional[Union[str, int]] = None
    topics: List[Topic]

    @model_validator(mode="after")
    @classmethod  # Add this decorator
    def validate_tables_when_unpivoted(cls, model):
        """Validate the tables attribute when unpivoting is required.

        Args:
        ----
            model (Column): The column model to validate.

        Returns:
        -------
            Column: The validated column model.

        """
        # Here 'model' is an instance of 'Column'
        if model.store_unpivoted:
            invalid_tables = [table for table in model.tables if table not in UNPIVOTED_TABLES]
            if invalid_tables:
                raise ValueError(
                    f"When 'store_unpivoted' is True, only {UNPIVOTED_TABLES} "
                    f"are allowed. Invalid tables provided: {invalid_tables}"
                )
        return model


class ConfigModel(BaseModel):
    """Represents the configuration model containing a list of columns.

    Attributes
    ----------
        columns (List[Column]): A list of columns in the configuration.

    """

    columns: List[Column]
