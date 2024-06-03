from typing import Dict, List, Optional

from pydantic import BaseModel


class Field(BaseModel):
    """
    Represents a field in the Topic model.

    Attributes:
      name (str): The name of the field.
      is_array (bool, optional): Indicates if the field is an array. Defaults to False.
    """

    name: str
    is_array: Optional[bool] = False


class Topic(BaseModel):
    """
    Represents a topic in the Column model.

    Attributes:
      name (str): The name of the topic.
      fields (List[Field]): A list of fields associated with the topic.
    """

    name: str
    fields: List[Field]


class Column(BaseModel):
    """
    Represents a column in a database table.

    Attributes:
      name (str): The name of the column.
      function (str): The function to be applied to the column.
      function_args (Optional[Dict]): Optional arguments for the function.
      type (str): The data type of the column.
      unit (str): The unit of measurement for the column.
      description (str): A description of the column.
      tables (Optional[List[str]]): Optional list of tables where the column is
      present.
      topics (List[Topic]): List of topics associated with the column.
    """

    name: str
    function: str
    function_args: Optional[Dict] = None
    type: str
    unit: str
    description: str
    tables: Optional[List[str]] = ["ExposureEFD", "VisitEFD"]
    topics: List[Topic]


class ConfigModel(BaseModel):
    """
    Represents a configuration model.

    Attributes:
      columns (List[Column]): A list of columns.
    """

    columns: List[Column]
