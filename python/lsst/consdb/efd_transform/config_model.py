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
            invalid_tables = [
                table for table in model.tables if table not in UNPIVOTED_TABLES
            ]
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
