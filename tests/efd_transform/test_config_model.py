import pytest
from pydantic import ValidationError

from python.lsst.consdb.efd_transform.config_model import UNPIVOTED_TABLES, Column, ConfigModel, Field, Topic


def test_column_creation_valid():
    topic = Topic(name="topic1", fields=[Field(name="field1")])
    column = Column(
        name="valid_column",
        tables=UNPIVOTED_TABLES,
        store_unpivoted=True,
        function="mean",
        datatype="float",
        unit="kg",
        description="A valid column",
        packed_series=False,
        topics=[topic],
    )
    assert column.name == "valid_column"
    assert column.tables == UNPIVOTED_TABLES


def test_column_with_invalid_tables():
    topic = Topic(name="topic2", fields=[Field(name="field2")])
    with pytest.raises(ValidationError) as excinfo:
        Column(
            name="invalid_column",
            tables=["invalid_table"],
            store_unpivoted=True,
            function="sum",
            datatype="float",
            unit="m",
            description="An invalid column",
            packed_series=False,
            topics=[topic],
        )
    assert "Invalid tables provided" in str(excinfo.value)


def test_config_model_creation():
    topic = Topic(name="topic3", fields=[Field(name="field3")])
    column = Column(
        name="column_in_model",
        tables=UNPIVOTED_TABLES,
        store_unpivoted=True,
        function="max",
        datatype="int",
        unit="s",
        description="A column within a model",
        packed_series=True,
        topics=[topic],
    )
    config_model = ConfigModel(columns=[column])
    assert len(config_model.columns) == 1
    assert config_model.columns[0].name == "column_in_model"
