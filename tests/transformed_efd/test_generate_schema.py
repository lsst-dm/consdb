from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
from lsst.consdb.transformed_efd.generate_schema_from_config import (
    build_argparser,
    generate_schema,
    schema_dict,
)


# Fixtures
@pytest.fixture
def mock_config():
    return {
        "columns": [
            {
                "name": "column1",
                "datatype": "int",
                "description": "Test column",
                "tables": ["exposure_efd"],
            },
            {
                "name": "column2",
                "datatype": "float",
                "description": "Unpivoted column",
                "tables": ["visit1_efd"],
                "store_unpivoted": True,
            },
        ]
    }


@pytest.fixture
def empty_config():
    return {"columns": []}


# 1. Input Validation Tests
def test_invalid_instrument(tmp_path):
    """Test invalid instrument raises ValueError"""
    config_path = tmp_path / "config.yml"
    with pytest.raises(ValueError, match="Invalid instrument"):
        generate_schema(config_path, "invalid_instrument")


# 2. Config File Tests
def test_missing_config_columns(tmp_path):
    """Test missing 'columns' section raises ValueError"""
    config_path = tmp_path / "config.yml"
    with patch("lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value={}):
        with pytest.raises(ValueError, match="must contain 'columns' section"):
            generate_schema(config_path, "latiss")


# 3. File Generation Tests
def test_schema_file_creation(tmp_path, mock_config):
    """Test schema file is created with correct name"""
    config_path = tmp_path / "config.yml"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema(config_path, "latiss")
        assert schema_path.name == "efd_latiss.yaml"
        assert schema_path.exists()


# 4. Directory Handling Tests
def test_output_dir_creation(tmp_path, mock_config):
    """Test output directory is created if missing"""
    config_path = tmp_path / "config.yml"
    output_dir = tmp_path / "new_dir"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        _ = generate_schema(config_path, "latiss", output_dir)
        assert output_dir.exists()


# 5. Table Content Tests
def test_exposure_table_content(tmp_path, mock_config):
    """Test exposure table contains expected columns"""
    config_path = tmp_path / "config.yml"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema(config_path, "latiss")
        content = schema_path.read_text()
        assert "exposure_efd" in content
        assert "exposure_id" in content
        assert "column1" in content


# 6. Unpivoted Table Tests
def test_unpivoted_table_generation(tmp_path, mock_config):
    """Test unpivoted tables are generated"""
    config_path = tmp_path / "config.yml"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema(config_path, "latiss")
        content = schema_path.read_text()
        assert "exposure_efd_unpivoted" in content
        assert "visit1_efd_unpivoted" in content


# 7. Column Writing Tests
def test_column_writing(tmp_path, mock_config):
    """Test columns are written with correct formatting"""
    config_path = tmp_path / "config.yml"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema(config_path, "latiss")
        content = schema_path.read_text()
        assert '- name: "column1"' in content
        assert "datatype: int" in content
        assert "description: Test column" in content


# 8. CLI Argument Parser Test
def test_argparser_output_dir():
    """Test argparser handles output_dir correctly"""
    parser = build_argparser()
    args = parser.parse_args(["--config", "test.yml", "--instrument", "latiss", "--output-dir", "custom"])
    assert args.output_dir == Path("custom")


# 9. Instrument Coverage Test
@pytest.mark.parametrize("instrument", schema_dict.keys())
def test_all_instruments(tmp_path, mock_config, instrument):
    """Test all instruments in schema_dict work"""
    config_path = tmp_path / "config.yml"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema(config_path, instrument)
        assert instrument.lower() in schema_path.name.lower()


# 10. Default Output Directory Test
def test_default_output_dir(tmp_path, mock_config):
    """Test default output directory is used when none specified"""
    config_path = tmp_path / "config.yml"
    expected_dir = config_path.parent.parent / "schemas/yml"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        generate_schema(config_path, "latiss")
        assert expected_dir.exists()


# 11. Empty Config Test
def test_empty_config(tmp_path, empty_config):
    """Test handling of empty columns list"""
    config_path = tmp_path / "config.yml"
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=empty_config
    ):
        schema_path = generate_schema(config_path, "latiss")
        content = schema_path.read_text()
        assert "exposure_efd" in content  # Should still create tables
        assert "column1" not in content  # But no custom columns


# 12. File Writing Test with Mock
def test_file_writing_with_mock(mock_config):
    """Test file writing operations using mock"""
    with (
        patch("builtins.open", mock_open()) as mocked_file,
        patch(
            "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
        ),
        patch("pathlib.Path.mkdir"),
    ):

        generate_schema(Path("dummy.yml"), "latiss")

        # Verify file was opened for writing
        mocked_file.assert_called_once()
        handle = mocked_file()

        # Verify basic structure was written
        assert any("name: efd_latiss" in call[0][0] for call in handle.write.call_args_list)
        assert any("exposure_efd" in call[0][0] for call in handle.write.call_args_list)
