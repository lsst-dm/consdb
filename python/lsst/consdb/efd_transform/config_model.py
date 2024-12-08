from typing import Dict, List, Optional, Union

from pydantic import BaseModel, model_validator

TABLES = ["exposure_efd", "exposure_efd_unpivoted", "visit1_efd", "visit1_efd_unpivoted"]
UNPIVOTED_TABLES = ["exposure_efd_unpivoted", "visit1_efd_unpivoted"]


class Field(BaseModel):
    name: str


class Topic(BaseModel):
    name: str
    fields: List[Field]


class Column(BaseModel):
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
        # Here 'model' is an instance of 'Column'
        if model.store_unpivoted:
            invalid_tables = [table for table in model.tables if table not in UNPIVOTED_TABLES]
            if invalid_tables:
                raise ValueError(
                    f"When 'store_unpivoted' is True, only {UNPIVOTED_TABLES} are allowed. "
                    f"Invalid tables provided: {invalid_tables}"
                )
        return model


class ConfigModel(BaseModel):
    columns: List[Column]
