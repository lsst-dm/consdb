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

# test_generate_schema.py

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
from unittest.mock import MagicMock, patch

import lsst.consdb.transformed_efd.generate_schema_from_config as gen_schema
import pytest
import yaml


@pytest.fixture
def mock_config():
    """A minimal, valid config for mocking."""
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
                "tables": ["exposure_efd"],
                "store_unpivoted": True,
                "description": "Unpivoted column",
                "datatype": "float",
                "ivoa": None,
            },
        ],
    }


def test_invalid_instrument():
    """Test that an invalid instrument name raises a ValueError."""
    with pytest.raises(ValueError, match="Invalid instrument"):
        gen_schema.generate_schema("invalid_instrument")


def test_missing_config_columns(mock_config):
    """Test that a config missing the 'columns' section raises a ValueError."""
    invalid_config = {"version": "1.0.0"}
    with (
        patch(f"{gen_schema.__name__}.read_config", return_value=invalid_config),
        pytest.raises(ValueError, match="must contain 'columns' section"),
    ):
        gen_schema.generate_schema("latiss")


def test_default_output_dir(tmp_path, mock_config):
    """Test the default output directory is used when none is specified."""
    # This test mocks the package resource finding mechanism to avoid writing
    # to the actual source tree during tests.
    mock_files_root = tmp_path / "mock_resources"
    mock_schemas_dir = mock_files_root / "schemas" / "yml"

    mock_traversable = MagicMock()
    mock_traversable.joinpath.return_value = mock_schemas_dir

    # We patch `read_config` so we don't need a real config file on disk.
    # The call to `importlib.resources.files` still happens, however.
    with (
        patch("importlib.resources.files", return_value=mock_traversable),
        patch(f"{gen_schema.__name__}.read_config", return_value=mock_config),
    ):
        schema_path = gen_schema.generate_schema("latiss")

        expected_file = mock_schemas_dir / "efd_latiss.yaml"
        assert schema_path == expected_file
        assert expected_file.is_file()
        assert mock_schemas_dir.exists()


def test_schema_content(tmp_path, mock_config):
    """Test tables and columns from the config appear correctly in the YAML."""
    with patch(f"{gen_schema.__name__}.read_config", return_value=mock_config):
        schema_path = gen_schema.generate_schema("latiss", output_dir=tmp_path)
        with open(schema_path) as f:
            schema_data = yaml.safe_load(f)

    assert schema_data["name"] == "efd_latiss"
    assert schema_data["version"]["current"] == "1.0.0"

    exposure_table = next((t for t in schema_data["tables"] if t["name"] == "exposure_efd"), None)
    assert exposure_table is not None

    column_names = [c["name"] for c in exposure_table["columns"]]
    assert "exposure_id" in column_names
    assert "column1" in column_names
    assert "column2" not in column_names

    column1_data = next((c for c in exposure_table["columns"] if c["name"] == "column1"), None)
    assert column1_data is not None
    assert column1_data["description"] == "Test column"
    assert column1_data["datatype"] == "int"
    assert column1_data["ivoa:ucd"] == "meta.id"


def test_argparser_setup(capsys):
    """Test that the argument parser is set up correctly."""
    parser = gen_schema.build_argparser()

    with pytest.raises(SystemExit):
        parser.parse_args([])
    assert "--instrument" in capsys.readouterr().err

    args = parser.parse_args(["--instrument", "latiss"])
    assert args.instrument == "latiss"
    assert args.output_dir is None

    args = parser.parse_args(["--instrument", "latiss", "--output-dir", "custom/path"])
    assert args.instrument == "latiss"
    assert args.output_dir == Path("custom/path")
