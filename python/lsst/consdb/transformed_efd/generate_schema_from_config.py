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
from pathlib import Path
from typing import Optional

from lsst.consdb.transformed_efd.transform_efd import read_config

schema_dict = {
    "latiss": "efd_latiss",
    "lsstcomcam": "efd_lsstcomcam",
    "lsstcomcamsim": "efd_lsstcomcamsim",
    "lsstcam": "efd_lsstcam",
}


def generate_schema(config_path: Path, instrument: str, output_dir: Optional[Path] = None) -> Path:
    """Generate database schema YAML file based on configuration

    Args:
        config_path: Path to the configuration file
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
    config = read_config(config_path)
    if "columns" not in config:
        raise ValueError("Configuration file must contain 'columns' section")

    # Determine output path
    output_dir = output_dir or config_path.parent.parent / "schemas"
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    schema_name = schema_dict[instrument.lower()]
    schema_path = output_dir / f"{schema_name}.yaml"

    # Generate schema content
    with open(schema_path, "w") as f:
        # Header
        f.write(
            f"""---
name: {schema_name}
"@id": "#{schema_name}"
description: Transformed EFD Consolidated Database for {instrument}
tables:
"""
        )

        # Exposure tables
        write_exposure_tables(f, config)
        write_visit_tables(f, config)
        write_scheduler_table(f)

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
  - "#exposure_efd.exposure_id"
  constraints:
  - name: un_exposure_id
    "@id": "#exposure_efd.un_exposure_id"
    "@type": Unique
    description: Ensure exposure_id is unique.
    columns:
    - "#exposure_efd.exposure_id"
  columns:
  - name: exposure_id
    "@id": "#exposure_efd.exposure_id"
    datatype: long
    description: Exposure unique ID.
  - name: created_at
    "@id": "#exposure_efd.created_at"
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'
    description: Timestamp when the record was created, default is current timestamp
"""
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
  - "#exposure_efd_unpivoted.exposure_id"
  - "#exposure_efd_unpivoted.property"
  - "#exposure_efd_unpivoted.field"
  constraints:
  - name: un_exposure_property_field
    "@id": "#exposure_efd_unpivoted.un_exposure_property_field"
    "@type": Unique
    description: Ensure combination of exposure_id, property, and field is unique.
    columns:
    - "#exposure_efd_unpivoted.exposure_id"
    - "#exposure_efd_unpivoted.property"
    - "#exposure_efd_unpivoted.field"
  columns:
  - name: exposure_id
    "@id": "#exposure_efd_unpivoted.exposure_id"
    datatype: long
    nullable: False
    description: Unique identifier for the exposure
  - name: property
    "@id": "#exposure_efd_unpivoted.property"
    datatype: string
    length: 64
    nullable: False
    value: default_property
    description: Property name for unpivoted data
  - name: field
    "@id": "#exposure_efd_unpivoted.field"
    datatype: string
    length: 32
    nullable: False
    value: default_field
    description: Field name for unpivoted data
  - name: value
    "@id": "#exposure_efd_unpivoted.value"
    datatype: float
    nullable: True
    description: Value corresponding to the parameter
  - name: created_at
    "@id": "#exposure_efd_unpivoted.created_at"
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'
    description: Timestamp when record was created, default current timestamp
"""
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
  - "#visit1_efd.visit_id"
  constraints:
  - name: un_visit_id
    "@id": "#visit1_efd.un_visit_id"
    "@type": Unique
    description: Ensure visit_id is unique.
    columns:
    - "#visit1_efd.visit_id"
  columns:
  - name: visit_id
    "@id": "#visit1_efd.visit_id"
    datatype: long
    description: Visit unique ID.
  - name: created_at
    "@id": "#visit1_efd.created_at"
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'
    description: Timestamp when record was created, default current timestamp
"""
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
  - "#visit1_efd_unpivoted.visit_id"
  - "#visit1_efd_unpivoted.property"
  - "#visit1_efd_unpivoted.field"
  constraints:
  - name: un_visit_property_field
    "@id": "#visit1_efd_unpivoted.un_visit_property_field"
    "@type": Unique
    description: Ensure combination of visit_id, property, and field is unique.
    columns:
    - "#visit1_efd_unpivoted.visit_id"
    - "#visit1_efd_unpivoted.property"
    - "#visit1_efd_unpivoted.field"
  columns:
  - name: visit_id
    "@id": "#visit1_efd_unpivoted.visit_id"
    datatype: long
    nullable: False
    description: Unique identifier for the visit
  - name: property
    "@id": "#visit1_efd_unpivoted.property"
    datatype: string
    length: 64
    nullable: False
    value: default_property
    description: Property name for unpivoted data
  - name: field
    "@id": "#visit1_efd_unpivoted.field"
    datatype: string
    length: 32
    nullable: False
    value: default_field
    description: Field name for unpivoted data
  - name: value
    "@id": "#visit1_efd_unpivoted.value"
    datatype: float
    nullable: True
    description: Value corresponding to the parameter
  - name: created_at
    "@id": "#visit1_efd_unpivoted.created_at"
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'
    description: Timestamp when record was created, default current timestamp
"""
    )


def write_scheduler_table(f):
    """Write scheduler table to schema file"""
    f.write(
        """
- name: transformed_efd_scheduler
  "@id": "#transformed_efd_scheduler"
  description: Transformed EFD scheduler.
  primaryKey:
  - "#transformed_efd_scheduler.id"
  constraints:
  - name: un_id
    "@id": "#transformed_efd_scheduler.un_id"
    "@type": Unique
    description: Ensure id is unique.
    columns:
    - "#transformed_efd_scheduler.id"
  columns:
  - name: id
    "@id": "#transformed_efd_scheduler.id"
    datatype: int
    nullable: False
    autoincrement: True
    description: Unique ID, auto-incremented
  - name: start_time
    "@id": "#transformed_efd_scheduler.start_time"
    datatype: timestamp
    description: Start time of transformation interval, must be provided
  - name: end_time
    "@id": "#transformed_efd_scheduler.end_time"
    datatype: timestamp
    description: End time of transformation interval, must be provided
  - name: timewindow
    "@id": "#transformed_efd_scheduler.timewindow"
    datatype: int
    description: Time window to expand start/end times by (minutes)
  - name: status
    "@id": "#transformed_efd_scheduler.status"
    datatype: char
    length: 20
    value: "pending"
    description: Process status, default 'pending'
  - name: process_start_time
    "@id": "#transformed_efd_scheduler.process_start_time"
    datatype: timestamp
    description: Timestamp when process started
  - name: process_end_time
    "@id": "#transformed_efd_scheduler.process_end_time"
    datatype: timestamp
    description: Timestamp when process ended
  - name: process_exec_time
    "@id": "#transformed_efd_scheduler.process_exec_time"
    datatype: int
    value: 0
    description: Execution time in seconds, default 0
  - name: exposures
    "@id": "#transformed_efd_scheduler.exposures"
    datatype: int
    value: 0
    description: Number of exposures processed, default 0
  - name: visits1
    "@id": "#transformed_efd_scheduler.visits1"
    datatype: int
    value: 0
    description: Number of visits recorded, default 0
  - name: retries
    "@id": "#transformed_efd_scheduler.retries"
    datatype: int
    value: 0
    description: Number of retries attempted, default 0
  - name: error
    "@id": "#transformed_efd_scheduler.error"
    datatype: text
    description: Error message, if any
  - name: butler_repo
    "@id": "#transformed_efd_scheduler.butler_repo"
    datatype: text
  - name: created_at
    "@id": "#transformed_efd_scheduler.created_at"
    datatype: timestamp
    value: 'CURRENT_TIMESTAMP'
    description: Timestamp when record was created, default current timestamp
"""
    )


def write_column(f, column: dict, table: str):
    """Helper function to write column definitions"""
    column_name = column["name"]
    f.write(f'  - name: "{column_name}"\n')
    f.write(f'    "@id": "#{table}.{column_name}"\n')
    f.write(f'    datatype: {column["datatype"]}\n')
    f.write("    nullable: True\n")
    f.write(f'    description: {column["description"]}\n')


def build_argparser() -> argparse.ArgumentParser:
    """Build CLI argument parser"""
    parser = argparse.ArgumentParser(description="Generate EFD transform schema")
    parser.add_argument("--config", type=Path, required=True, help="Path to configuration file")
    parser.add_argument("--instrument", type=str, required=True, help="Instrument name (case-insensitive)")
    parser.add_argument(
        "--output-dir", type=Path, help="Custom output directory (default: config/../schemas/)"
    )
    return parser


if __name__ == "__main__":
    parser = build_argparser()
    args = parser.parse_args()

    schema_path = generate_schema(
        config_path=args.config, instrument=args.instrument, output_dir=args.output_dir
    )

    print(f"Schema successfully generated at: {schema_path}")
