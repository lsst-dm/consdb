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
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import yaml

# Import the functions and variables to be tested
from lsst.consdb.transformed_efd.generate_schema_from_config import (
    build_argparser,
    generate_schema,
    schema_dict,
)


# A minimal, valid config for mocking
@pytest.fixture
def mock_config():
    return {
        "version": "1.0.0",
        "columns": [
            {
                "name": "column1",
                "tables": ["exposure_efd"],
                "store_unpivoted": False,
                "description": "Test column",
                "datatype": "int",
                "ivoa": {"ucd": "meta.id"},
            },
            {
                "name": "column2",
                "tables": ["exposure_efd_unpivoted"],
                "store_unpivoted": True,
                "description": "Unpivoted column",
                "datatype": "float",
                "ivoa": None,
            },
        ],
    }


@pytest.fixture
def empty_config():
    return {"version": "1.0.0", "columns": []}


def test_invalid_instrument():
    """Test that an invalid instrument name raises a ValueError."""
    with pytest.raises(ValueError, match="Invalid instrument"):
        generate_schema("invalid_instrument")


def test_missing_config_columns():
    """Test that a config missing the 'columns' section raises a ValueError."""
    # Mock read_config to return a config without the 'columns' key
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config",
        return_value={"version": "1.0.0"},
    ):
        with pytest.raises(ValueError, match="must contain 'columns' section"):
            generate_schema("latiss")


def test_schema_file_creation(tmp_path, mock_config):
    """Test that the schema file is created with the correct name."""
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        # The instrument 'latiss' should produce 'efd_latiss.yaml'
        schema_path = generate_schema("latiss", output_dir=tmp_path)
        expected_file = tmp_path / "efd_latiss.yaml"
        assert schema_path == expected_file
        assert expected_file.is_file()


def test_output_dir_creation(tmp_path, mock_config):
    """Test that the output directory is created if it does not exist."""
    output_dir = tmp_path / "new_dir"
    assert not output_dir.exists()
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        generate_schema("latiss", output_dir=output_dir)
    assert output_dir.exists()
    assert (output_dir / "efd_latiss.yaml").is_file()


def test_default_output_dir(mock_config):
    """The default output directory is used when none is specified."""

    with (
        patch("pathlib.Path.mkdir"),
        patch("builtins.open", mock_open()),
        patch(
            "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
        ),
    ):

        # The function returns the path to the generated schema file.
        schema_path = generate_schema("latiss")

        # The default path is relative to the source code,
        # but we know what it should end with.
        # The schema name for 'latiss' is 'efd_latiss'.
        expected_suffix = Path("schemas") / "yml" / "efd_latiss.yaml"
        assert str(schema_path).endswith(str(expected_suffix))


def test_exposure_table_content(tmp_path, mock_config):
    """Test that the exposure table contains columns from the config."""
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema("latiss", output_dir=tmp_path)
        with open(schema_path) as f:
            schema_data = yaml.safe_load(f)

        exposure_table = next(t for t in schema_data["tables"] if t["name"] == "exposure_efd")
        column_names = [c["name"] for c in exposure_table["columns"]]

        assert "exposure_id" in column_names
        assert "column1" in column_names  # From mock_config
        assert "column2" not in column_names  # Unpivoted columns should not be here


def test_unpivoted_table_generation(tmp_path, mock_config):
    """Test that unpivoted tables are generated correctly."""
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema("lsstcam", output_dir=tmp_path)
        with open(schema_path) as f:
            schema_data = yaml.safe_load(f)

        # Check that the unpivoted table exists
        unpivoted_table = next(
            (t for t in schema_data["tables"] if t["name"] == "exposure_efd_unpivoted"), None
        )
        assert unpivoted_table is not None

        # The unpivoted table should NOT contain the
        # explicitly defined 'column2'
        column_names = [c["name"] for c in unpivoted_table["columns"]]
        assert "column2" not in column_names


def test_column_writing(tmp_path, mock_config):
    """Test that columns are written with correct format and IVOA metadata."""
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema("latiss", output_dir=tmp_path)
        with open(schema_path, "r") as f:
            content = f.read()

        # Check for correct YAML structure for column1
        assert "name: column1" in content
        assert "description: Test column" in content
        assert "datatype: int" in content
        assert "ivoa:ucd: meta.id" in content


@pytest.mark.parametrize("instrument", schema_dict.keys())
def test_all_instruments(tmp_path, mock_config, instrument):
    """Test that schema generation works for all supported instruments."""
    with patch(
        "lsst.consdb.transformed_efd.generate_schema_from_config.read_config", return_value=mock_config
    ):
        schema_path = generate_schema(instrument, output_dir=tmp_path)
        expected_schema_name = schema_dict[instrument]
        assert schema_path.name == f"{expected_schema_name}.yaml"
        assert schema_path.is_file()


def test_argparser_setup():
    """Test that the argument parser is set up correctly."""
    parser = build_argparser()

    # Test required instrument argument
    with pytest.raises(SystemExit):
        parser.parse_args([])  # No arguments should fail

    # Test with required instrument argument
    args = parser.parse_args(["--instrument", "latiss"])
    assert args.instrument == "latiss"
    assert args.output_dir is None

    # Test with output_dir argument
    args = parser.parse_args(["--instrument", "latiss", "--output-dir", "custom/path"])
    assert args.instrument == "latiss"
    assert args.output_dir == Path("custom/path")
