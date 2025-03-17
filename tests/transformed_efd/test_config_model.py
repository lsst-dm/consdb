import pytest
from lsst.consdb.transformed_efd.config_model import TABLES, Column, ConfigModel, Field, Topic
from pydantic import ValidationError


def test_column_valid_unpivoted_tables():
    column = Column(
        name="valid_column",
        tables=["exposure_efd_unpivoted"],
        store_unpivoted=True,
        function="sum",
        datatype="int",
        unit="units",
        description="Valid test column",
        packed_series=False,
        topics=[Topic(name="TestTopic", fields=[Field(name="TestField")])],
    )
    assert column.store_unpivoted is True
    assert column.tables == ["exposure_efd_unpivoted"]


def test_column_invalid_unpivoted_tables():
    with pytest.raises(ValidationError) as exc_info:
        Column(
            name="invalid_column",
            tables=["exposure_efd"],
            store_unpivoted=True,
            function="avg",
            datatype="float",
            unit="units",
            description="Invalid test column",
            packed_series=False,
            topics=[Topic(name="TestTopic", fields=[Field(name="TestField")])],
        )
    assert "Invalid tables provided" in str(exc_info.value)


def test_column_without_unpivoted():
    column = Column(
        name="non_unpivoted_column",
        tables=["exposure_efd"],
        store_unpivoted=False,
        function="sum",
        datatype="string",
        unit="none",
        description="Non-unpivoted test column",
        packed_series=False,
        topics=[Topic(name="TestTopic", fields=[Field(name="TestField")])],
    )
    assert column.store_unpivoted is False
    assert column.tables == ["exposure_efd"]


def test_column_with_empty_tables():
    column = Column(
        name="empty_tables_column",
        tables=[],
        store_unpivoted=False,
        function="count",
        datatype="string",
        unit="none",
        description="Empty tables test column",
        packed_series=False,
        topics=[Topic(name="TestTopic", fields=[Field(name="TestField")])],
    )
    assert column.tables == []


def test_config_model():
    config = ConfigModel(
        columns=[
            Column(
                name="column1",
                tables=TABLES,
                store_unpivoted=False,
                function="max",
                datatype="integer",
                unit="units",
                description="Column in config",
                packed_series=False,
                topics=[Topic(name="Topic1", fields=[Field(name="Field1")])],
            )
        ]
    )
    assert len(config.columns) == 1
    assert config.columns[0].name == "column1"
