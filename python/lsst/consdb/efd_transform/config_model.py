from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class Field(BaseModel):
    """
    Represents a field in the config model.

    Attributes
    ----------
    name : str
      The name of the field.
    """

    name: str


class Topic(BaseModel):
    """
    Represents a topic.

    Parameters
    ----------
    name : str
      The name of the topic.
    fields : List[Field]
      The list of fields associated with the topic.

    Attributes
    ----------
    name : str
      The name of the topic.
    fields : List[Field]
      The list of fields associated with the topic.
    """

    name: str
    fields: List[Field]


class Column(BaseModel):
    """
    Represents a column in the configuration model.

    Parameters
    ----------
    name : str
      The name of the column.
    tables : Optional[List[str]], optional
      The list of tables that the column belongs to, by default
      ["ExposureEFD", "VisitEFD"].
    function : str
      The function applied to the column.
    function_args : Optional[Dict], optional
      The arguments passed to the function, by default {}.
    datatype : str
      The datatype of the column.
    unit : str
      The unit of the column.
    description : str
      The description of the column.
    packed_series : bool
      Indicates if the column is part of a packed series.
    subset_field : Optional[str], optional
      The field used for subsetting, by default None.
    subset_value : Optional[Union[str,int]], optional
      The value used for subsetting, by default None.
    topics : List[Topic]
      The list of topics associated with the column.
    """

    name: str
    tables: Optional[List[str]] = ["ExposureEFD", "VisitEFD"]
    function: str
    function_args: Optional[Dict] = None
    datatype: str
    unit: str
    description: str
    packed_series: bool
    subset_field: Optional[str] = None
    subset_value: Optional[Union[str, int]] = None
    topics: List[Topic]


class ConfigModel(BaseModel):
    """
    Model representing the configuration of a database table.

    Attributes
    ----------
      columns (List[Column]): List of columns in the table.

    """

    columns: List[Column]
