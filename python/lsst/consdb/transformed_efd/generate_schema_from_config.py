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

import argparse
import importlib.resources
from pathlib import Path
from typing import Optional

from lsst.consdb.transformed_efd.transform_efd import read_config

schema_dict = {
    "latiss": "efd2_latiss",
    "lsstcomcam": "efd2_lsstcomcam",
    "lsstcomcamsim": "efd2_lsstcomcamsim",
    "lsstcam": "efd2_lsstcam",
}


def generate_schema(instrument: str, output_dir: Optional[Path] = None) -> Path:
    """Generate database schema YAML file based on configuration

    Args:
        instrument: Instrument name
        output_dir: Optional output directory (defaults to schemas/ directory)

    Returns:
        Path to the generated schema file

    Raises:
        ValueError: If instrument is invalid or config is missing required data
    """
    # Validate instrument
    if instrument.lower() not in schema_dict:
        raise ValueError(f"Invalid instrument: {instrument}. Valid options: {list(schema_dict.keys())}")

    # Read configuration
    config_files = importlib.resources.files("lsst.consdb.transformed_efd.config")
    config_path = config_files / f"config_{instrument.lower()}.yaml"
    config = read_config(config_path)
    if "columns" not in config:
        raise ValueError("Configuration file must contain 'columns' section")

    # Determine output path
    if output_dir is None:
        output_dir = importlib.resources.files("lsst.consdb.transformed_efd").joinpath("schemas", "yml")
    output_dir.mkdir(parents=True, exist_ok=True)

    schema_name = schema_dict[instrument.lower()]
    schema_path = output_dir / f"{schema_name}.yaml"

    # Generate schema content
    with open(schema_path, "w") as f:
        # Header
        f.write(
            f"""---
name: {schema_name}
"@id": "#{schema_name}"
description: Transformed EFD Consolidated Database for {instrument}.
version:
  current: {config["version"]}
tables:"""
        )

        # Exposure tables
        write_exposure_tables(f, config)
        write_visit_tables(f, config)

    return schema_path


def write_exposure_tables(f, config):
    """Write exposure-related tables to schema file"""
    # exposure_efd table
    f.write(
        """
- name: exposure_efd
  "@id": "#exposure_efd"
  description: Transformed EFD topics by exposure.
  primaryKey:
  - "#exposure_efd.day_obs"
  - "#exposure_efd.seq_num"
  constraints:
  - name: un_exposure_efd_exposure_id
    "@id": "#exposure_efd.un_exposure_efd_exposure_id"
    "@type": Unique
    description: Ensure exposure_id is unique.
    columns:
    - "#exposure_efd.exposure_id"
  columns:
  - name: day_obs
    "@id": "#exposure_efd.day_obs"
    description: Day of observation in YYYYMMDD format.
    datatype: int
    nullable: false
    ivoa:ucd: meta.id.part
  - name: seq_num
    "@id": "#exposure_efd.seq_num"
    description: Sequence number for the exposure.
    datatype: int
    ivoa:ucd: meta.id.part
  - name: exposure_id
    "@id": "#exposure_efd.exposure_id"
    description: Exposure unique ID.
    datatype: long
    nullable: false
    ivoa:ucd: meta.id
  - name: created_at
    "@id": "#exposure_efd.created_at"
    description: Timestamp when the record was created, default is current timestamp.
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'\n"""
    )

    # Add dynamic columns from config
    for column in config["columns"]:
        if "exposure_efd" in column.get("tables", []):
            if not column.get("store_unpivoted", False):
                write_column(f, column, "exposure_efd")

    # exposure_efd_unpivoted table
    f.write(
        """
- name: exposure_efd_unpivoted
  "@id": "#exposure_efd_unpivoted"
  description: Unpivoted EFD exposure data.
  primaryKey:
  - "#exposure_efd_unpivoted.day_obs"
  - "#exposure_efd_unpivoted.seq_num"
  - "#exposure_efd_unpivoted.exposure_id"
  - "#exposure_efd_unpivoted.property"
  - "#exposure_efd_unpivoted.field"
  columns:
  - name: day_obs
    "@id": "#exposure_efd_unpivoted.day_obs"
    description: Day of observation in YYYYMMDD format.
    datatype: int
    nullable: false
    ivoa:ucd: meta.id.part
  - name: seq_num
    "@id": "#exposure_efd_unpivoted.seq_num"
    description: Sequence number for the exposure.
    datatype: int
    nullable: false
    ivoa:ucd: meta.id.part
  - name: exposure_id
    "@id": "#exposure_efd_unpivoted.exposure_id"
    description: Unique identifier for the exposure.
    datatype: long
    nullable: false
    ivoa:ucd: meta.id
  - name: property
    "@id": "#exposure_efd_unpivoted.property"
    description: Property name for unpivoted data
    datatype: string
    length: 64
    nullable: false
    value: default_property
  - name: field
    "@id": "#exposure_efd_unpivoted.field"
    description: Field name for unpivoted data.
    datatype: string
    length: 32
    nullable: false
    value: default_field
  - name: value
    "@id": "#exposure_efd_unpivoted.value"
    description: Value corresponding to the parameter
    datatype: float
  - name: created_at
    "@id": "#exposure_efd_unpivoted.created_at"
    description: Timestamp when record was created, default current timestamp.
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'\n"""
    )


def write_visit_tables(f, config):
    """Write visit-related tables to schema file"""
    # visit1_efd table
    f.write(
        """
- name: visit1_efd
  "@id": "#visit1_efd"
  description: Transformed EFD topics by visit.
  primaryKey:
  - "#visit1_efd.day_obs"
  - "#visit1_efd.seq_num"
  constraints:
  - name: un_visit1_efd_visit_id
    "@id": "#visit1_efd.un_visit1_efd_visit_id"
    "@type": Unique
    description: Ensure visit_id is unique.
    columns:
    - "#visit1_efd.visit_id"
  columns:
  - name: day_obs
    "@id": "#visit1_efd.day_obs"
    description: Day of observation in YYYYMMDD format.
    datatype: int
    nullable: false
    ivoa:ucd: meta.id.part
  - name: seq_num
    "@id": "#visit1_efd.seq_num"
    description: Sequence number for the visit.
    datatype: int
    ivoa:ucd: meta.id.part
  - name: visit_id
    "@id": "#visit1_efd.visit_id"
    description: Visit unique ID.
    datatype: long
    nullable: false
    ivoa:ucd: meta.id
  - name: created_at
    "@id": "#visit1_efd.created_at"
    description: Timestamp when record was created, default current timestamp.
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'\n"""
    )

    # Add dynamic columns from config
    for column in config["columns"]:
        if "visit1_efd" in column.get("tables", []):
            if not column.get("store_unpivoted", False):
                write_column(f, column, "visit1_efd")

    # visit1_efd_unpivoted table
    f.write(
        """
- name: visit1_efd_unpivoted
  "@id": "#visit1_efd_unpivoted"
  description: Unpivoted EFD visit data.
  primaryKey:
  - "#visit1_efd_unpivoted.day_obs"
  - "#visit1_efd_unpivoted.seq_num"
  - "#visit1_efd_unpivoted.visit_id"
  - "#visit1_efd_unpivoted.property"
  - "#visit1_efd_unpivoted.field"
  columns:
  - name: day_obs
    "@id": "#visit1_efd_unpivoted.day_obs"
    description: Day of observation in YYYYMMDD format.
    datatype: int
    nullable: false
    ivoa:ucd: meta.id.part
  - name: seq_num
    "@id": "#visit1_efd_unpivoted.seq_num"
    description: Sequence number for the visit.
    datatype: int
    nullable: false
    ivoa:ucd: meta.id.part
  - name: visit_id
    "@id": "#visit1_efd_unpivoted.visit_id"
    description: Unique identifier for the visit.
    datatype: long
    nullable: false
    ivoa:ucd: meta.id
  - name: property
    "@id": "#visit1_efd_unpivoted.property"
    description: Property name for unpivoted data.
    datatype: string
    length: 64
    nullable: false
    value: default_property
  - name: field
    "@id": "#visit1_efd_unpivoted.field"
    description: Field name for unpivoted data.
    datatype: string
    length: 32
    nullable: false
    value: default_field
  - name: value
    "@id": "#visit1_efd_unpivoted.value"
    description: Value corresponding to the parameter.
    datatype: float
  - name: created_at
    "@id": "#visit1_efd_unpivoted.created_at"
    description: Timestamp when record was created, default current timestamp.
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'\n"""
    )


def write_column(f, column: dict, table: str):
    """Helper function to write column definitions"""
    column_name = column["name"]
    f.write(f"  - name: {column_name}\n")
    f.write(f'    "@id": "#{table}.{column_name}"\n')
    f.write(f'    description: {column["description"]}\n')
    f.write(f'    datatype: {column["datatype"]}\n')
    # Check for 'ivoa' metadata and write it
    if ("ivoa" in column) and column["ivoa"] is not None:
        for key, value in sorted(column["ivoa"].items()):
            f.write(f"    ivoa:{key}: {value}\n")


def build_argparser() -> argparse.ArgumentParser:
    """Build CLI argument parser"""
    parser = argparse.ArgumentParser(description="Generate EFD transform schema.")
    parser.add_argument("--instrument", type=str, required=True, help="Instrument name (case-insensitive).")
    parser.add_argument(
        "--output-dir", type=Path, help="Custom output directory (default: config/../schemas/)."
    )
    return parser


if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()

    schema_path = generate_schema(instrument=args.instrument, output_dir=args.output_dir)

    print(f"Schema successfully generated at: {schema_path}")
