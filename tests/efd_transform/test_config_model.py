import pytest
from pydantic import ValidationError

from python.lsst.consdb.efd_transform.config_model import Column, ConfigModel, Field, Topic


def get_columns():
    columns = [
        Column(
            name="column1",
            function="function1",
            type="type1",
            unit="unit1",
            description="description1",
            topics=[
                Topic(
                    name="topic1",
                    fields=[
                        Field(name="field1", is_array=False),
                        Field(name="field2", is_array=True),
                    ],
                ),
                Topic(
                    name="topic2",
                    fields=[
                        Field(name="field3", is_array=False),
                        Field(name="field4", is_array=True),
                    ],
                ),
            ],
        ),
        Column(
            name="column2",
            function="function2",
            type="type2",
            unit="unit2",
            description="description2",
            topics=[
                Topic(
                    name="topic3",
                    fields=[
                        Field(name="field5", is_array=False),
                        Field(name="field6", is_array=True),
                    ],
                ),
            ],
        ),
    ]

    return columns


def test_config_model_valid():
    columns = get_columns()

    config_model = ConfigModel(columns=columns)

    assert config_model.columns == columns


def test_config_model_invalid():

    # Missing required attribute 'columns'
    with pytest.raises(ValidationError):
        ConfigModel()

    # Invalid type for 'columns'
    with pytest.raises(ValidationError):
        ConfigModel(columns="invalid")

    # Invalid type for 'name' in Column
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].name = 123
        ConfigModel.model_validate(columns)

    # Invalid type for 'function' in Column
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].function = 123
        ConfigModel.model_validate(columns)

    # Invalid type for 'type' in Column
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].type = 123
        ConfigModel.model_validate(columns)

    # Invalid type for 'unit' in Column
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].unit = 123
        ConfigModel.model_validate(columns)

    # Invalid type for 'description' in Column
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].description = 123
        ConfigModel.model_validate(columns)

    # Invalid type for 'tables' in Column
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].tables = "invalid"
        ConfigModel.model_validate(columns)

    # Invalid type for 'topics' in Column
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].topics = "invalid"
        ConfigModel.model_validate(columns)

    # Invalid type for 'name' in Topic
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].topics[0].name = 123
        ConfigModel.model_validate(columns)

    # Invalid type for 'fields' in Topic
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].topics[0].fields = "invalid"
        ConfigModel.model_validate(columns)

    # Invalid type for 'name' in Field
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].topics[0].fields[0].name = 123
        ConfigModel.model_validate(columns)

    # Invalid type for 'is_array' in Field
    with pytest.raises(ValidationError):
        columns = get_columns()
        columns[0].topics[0].fields[0].is_array = "invalid"
        ConfigModel.model_validate(columns)
