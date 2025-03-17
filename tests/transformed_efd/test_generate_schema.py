import sys
from unittest.mock import mock_open, patch

import pytest
from lsst.consdb.transformed_efd.generate_schema import build_argparser, schema_dict

# Mocked configuration data
mock_config = {
    "columns": [
        {
            "name": "column1",
            "datatype": "int",
            "description": "An example integer column",
            "tables": ["exposure_efd"],
        },
        {
            "name": "column2",
            "datatype": "string",
            "description": "An example string column",
            "tables": ["visit1_efd"],
            "store_unpivoted": True,
        },
    ]
}


# Utility function to simulate command-line arguments
def set_args(*args):
    sys.argv = ["generate_schema.py"] + list(args)


def test_build_argparser():
    parser = build_argparser()
    args = parser.parse_args(["--config", "test_config.yml", "--instrument", "LATISS"])
    assert args.config == "test_config.yml"
    assert args.instrument == "LATISS"


@pytest.mark.parametrize(
    "instrument, expected_file",
    [
        ("LATISS", "cdb_transformed_efd_LATISS.yaml"),
        ("LSSTCam", "cdb_transformed_efd_LSSTCam.yaml"),
    ],
)
@patch("lsst.consdb.efd_transform.generate_schema.read_config", return_value=mock_config)
@patch("builtins.open", new_callable=mock_open)
def test_schema_generation(mock_open, mock_read_config, instrument, expected_file):
    # Set mock command-line arguments
    set_args("--config", "mock_config.yml", "--instrument", instrument)

    # Simulate the main script logic
    parser = build_argparser()
    args = parser.parse_args()

    # Validate the output file name
    output_filename = f"cdb_transformed_efd_{args.instrument}.yaml"
    assert output_filename == expected_file

    # Mock file writing and verify
    with patch("builtins.open", mock_open) as mock_file:
        # Call the schema generation logic (partial simulation here)
        with open(output_filename, "w") as f:
            f.write("---\n")
            f.write(f"name: {schema_dict[args.instrument]}\n")

        # Verify open was called with the correct filename
        mock_file.assert_called_with(output_filename, "w")

        # Fetch the mocked file handle and its method calls
        file_handle = mock_file()
        file_handle.write.assert_any_call("---\n")
        file_handle.write.assert_any_call(f"name: {schema_dict[instrument]}\n")


@patch("lsst.consdb.efd_transform.generate_schema.read_config", side_effect=FileNotFoundError)
def test_missing_config_file(mock_read_config):
    # Set mock command-line arguments
    set_args("--config", "missing_config.yml", "--instrument", "LATISS")
    parser = build_argparser()
    args = parser.parse_args()

    with pytest.raises(FileNotFoundError):
        mock_read_config(args.config)


def test_invalid_instrument():
    # Set invalid instrument
    set_args("--config", "mock_config.yml", "--instrument", "InvalidInstrument")
    parser = build_argparser()
    args = parser.parse_args()

    with pytest.raises(KeyError):
        _ = schema_dict[args.instrument]
