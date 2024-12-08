import argparse

from transform_efd import read_config

schema_dict = {
    "LATISS": "cdb_latiss",
    "LSSTComCam": "cdb_lsstcomcam",
    "LSSTComCamSim": "cdb_lsstcomcamsim",
    "LSSTCam": "cdb_lsstcam",
}


def build_argparser() -> argparse.ArgumentParser:
    """
    Build the argument parser for the script.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="Generate the schema for the EFD transform.")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="The path to the configuration file.",
    )
    parser.add_argument(
        "--instrument",
        type=str,
        required=True,
        help="The instrument name.",
    )

    return parser


if __name__ == "__main__":

    # run example:
    # python generate_schema.py --config config.yml --instrument latiss

    parse = build_argparser()
    args = parse.parse_args()
    config = read_config(args.config)

    output = "cdb_transformed_efd_" + args.instrument + ".yaml"
    print(output)
    with open(output, "w") as f:
        # Generate the schema for the EFD transform.
        f.write("---\n")
        f.write(f"name: {schema_dict[args.instrument]}\n")
        f.write(f'"@id": "#{schema_dict[args.instrument]}"\n')
        f.write(f"description: Transformed EFD Consolidated Database for {args.instrument}\n")
        f.write("tables:\n")

        # Generate exposure_efd table.
        f.write("- name: exposure_efd\n")
        f.write('  "@id": "#exposure_efd"\n')
        f.write("  description: Transformed EFD topics by exposure.\n")
        f.write("  primaryKey:\n")
        f.write('  - "#exposure_efd.exposure_id"\n')
        f.write('  - "#exposure_efd.instrument"\n')
        f.write("  constraints:\n")
        f.write("  - name: un_exposure_id_instrument\n")
        f.write('    "@id": "#exposure_efd.un_exposure_id_instrument"\n')
        f.write('    "@type": Unique\n')
        f.write("    description: Ensure exposure_id is unique.\n")
        f.write("    columns:\n")
        f.write('    - "#exposure_efd.exposure_id"\n')
        f.write('    - "#exposure_efd.instrument"\n')
        f.write("  columns:\n")
        f.write("  - name: exposure_id\n")
        f.write('    "@id": "#exposure_efd.exposure_id"\n')
        f.write("    datatype: long\n")
        f.write("    description: Exposure unique ID.\n")
        f.write("  - name: created_at\n")
        f.write('    "@id": "#exposure_efd.created_at"\n')
        f.write("    datatype: timestamp\n")
        f.write("    value: 'CURRENT_TIMESTAMP'\n")
        f.write("    description: Timestamp when the record was created, default is the current timestamp\n")
        f.write("  - name: instrument\n")
        f.write('    "@id": "#exposure_efd.instrument"\n')
        f.write("    datatype: char\n")
        f.write("    length: 20\n")
        f.write("    description: Instrument name.\n")
        # Iterate over columns in the config file
        for column in config["columns"]:
            if "exposure_efd" in column["tables"] and not column.get("store_unpivoted", False):
                column_name = column["name"]
                f.write(f'  - name: "{column_name}"\n')
                f.write(f'    "@id": "#exposure_efd.{column_name}"\n')
                datatype = column["datatype"]
                f.write(f"    datatype: {datatype}\n")
                f.write("    nullable: True\n")
                column_description = column["description"]
                f.write(f"    description: {column_description}\n")
        f.write("\n")

        # Generate exposure_efd_unpivoted table
        f.write("- name: exposure_efd_unpivoted\n")
        f.write('  "@id": "#exposure_efd_unpivoted"\n')
        f.write("  description: Unpivoted EFD exposure data.\n")
        f.write("  primaryKey:\n")
        f.write('  - "#exposure_efd_unpivoted.exposure_id"\n')
        f.write('  - "#exposure_efd_unpivoted.property"\n')
        f.write('  - "#exposure_efd_unpivoted.field"\n')
        f.write("  constraints:\n")
        f.write("  - name: un_exposure_property_field\n")
        f.write('    "@id": "#exposure_efd_unpivoted.un_exposure_property_field"\n')
        f.write('    "@type": Unique\n')
        f.write("    description: Ensure the combination of exposure_id, property, and field is unique.\n")
        f.write("    columns:\n")
        f.write('    - "#exposure_efd_unpivoted.exposure_id"\n')
        f.write('    - "#exposure_efd_unpivoted.property"\n')
        f.write('    - "#exposure_efd_unpivoted.field"\n')
        f.write("  columns:\n")
        f.write("  - name: exposure_id\n")
        f.write('    "@id": "#exposure_efd_unpivoted.exposure_id"\n')
        f.write("    datatype: int\n")
        f.write("    nullable: False\n")
        f.write("    description: Unique identifier for the exposure\n")
        f.write("  - name: property\n")
        f.write('    "@id": "#exposure_efd_unpivoted.property"\n')
        f.write("    datatype: char\n")
        f.write("    length: 255\n")
        f.write("    nullable: False\n")
        f.write("    value: default_property\n")
        f.write("    description: Property name for the unpivoted data\n")
        f.write("  - name: field\n")
        f.write('    "@id": "#exposure_efd_unpivoted.field"\n')
        f.write("    datatype: char\n")
        f.write("    length: 255\n")
        f.write("    nullable: False\n")
        f.write("    value: default_field\n")
        f.write("    description: Field name for the unpivoted data\n")
        f.write("  - name: value\n")
        f.write('    "@id": "#exposure_efd_unpivoted.value"\n')
        f.write("    datatype: double\n")
        f.write("    nullable: True\n")
        f.write("    description: Value corresponding to the parameter\n")
        f.write("  - name: created_at\n")
        f.write('    "@id": "#exposure_efd_unpivoted.created_at"\n')
        f.write("    datatype: timestamp\n")
        f.write("    value: 'CURRENT_TIMESTAMP'\n")
        f.write("    description: Timestamp when the record was created, default is the current timestamp\n")
        f.write("\n")

        # Generate visit1_efd table.
        f.write("- name: visit1_efd\n")
        f.write('  "@id": "#visit1_efd"\n')
        f.write("  description: Transformed EFD topics by visit.\n")
        f.write("  primaryKey:\n")
        f.write('  - "#visit1_efd.visit_id"\n')
        f.write('  - "#visit1_efd.instrument"\n')
        f.write("  constraints:\n")
        f.write("  - name: un_visit_id_instrument\n")
        f.write('    "@id": "#visit1_efd.un_visit_id_instrument"\n')
        f.write('    "@type": Unique\n')
        f.write("    description: Ensure visit_id is unique.\n")
        f.write("    columns:\n")
        f.write('    - "#visit1_efd.visit_id"\n')
        f.write('    - "#visit1_efd.instrument"\n')
        f.write("  columns:\n")
        f.write("  - name: visit_id\n")
        f.write('    "@id": "#visit1_efd.visit_id"\n')
        f.write("    datatype: long\n")
        f.write("    description: Visit unique ID.\n")
        f.write("  - name: created_at\n")
        f.write('    "@id": "#visit1_efd.created_at"\n')
        f.write("    datatype: timestamp\n")
        f.write("    value: 'CURRENT_TIMESTAMP'\n")
        f.write("    description: Timestamp when the record was created, default is the current timestamp\n")
        f.write("  - name: instrument\n")
        f.write('    "@id": "#visit1_efd.instrument"\n')
        f.write("    datatype: char\n")
        f.write("    length: 20\n")
        f.write("    description: Instrument name.\n")
        # Iterate over columns in the config file
        for column in config["columns"]:
            if "visit1_efd" in column["tables"] and not column.get("store_unpivoted", False):
                column_name = column["name"]
                f.write(f'  - name: "{column_name}"\n')
                f.write(f'    "@id": "#visit1_efd.{column_name}"\n')
                datatype = column["datatype"]
                f.write(f"    datatype: {datatype}\n")
                f.write("    nullable: True\n")
                column_description = column["description"]
                f.write(f"    description: {column_description}\n")
        f.write("\n")

        # Generate visit1_efd_unpivoted table
        f.write("- name: visit1_efd_unpivoted\n")
        f.write('  "@id": "#visit1_efd_unpivoted"\n')
        f.write("  description: Unpivoted EFD visit data.\n")
        f.write("  primaryKey:\n")
        f.write('  - "#visit1_efd_unpivoted.visit_id"\n')
        f.write('  - "#visit1_efd_unpivoted.property"\n')
        f.write('  - "#visit1_efd_unpivoted.field"\n')
        f.write("  constraints:\n")
        f.write("  - name: un_visit_property_field\n")
        f.write('    "@id": "#visit1_efd_unpivoted.un_visit_property_field"\n')
        f.write('    "@type": Unique\n')
        f.write("    description: Ensure the combination of visit_id, property, and field is unique.\n")
        f.write("    columns:\n")
        f.write('    - "#visit1_efd_unpivoted.visit_id"\n')
        f.write('    - "#visit1_efd_unpivoted.property"\n')
        f.write('    - "#visit1_efd_unpivoted.field"\n')
        f.write("  columns:\n")
        f.write("  - name: visit_id\n")
        f.write('    "@id": "#visit1_efd_unpivoted.visit_id"\n')
        f.write("    datatype: int\n")
        f.write("    nullable: False\n")
        f.write("    description: Unique identifier for the visit\n")
        f.write("  - name: property\n")
        f.write('    "@id": "#visit1_efd_unpivoted.property"\n')
        f.write("    datatype: char\n")
        f.write("    length: 255\n")
        f.write("    nullable: False\n")
        f.write("    value: default_property\n")
        f.write("    description: Property name for the unpivoted data\n")
        f.write("  - name: field\n")
        f.write('    "@id": "#visit1_efd_unpivoted.field"\n')
        f.write("    datatype: char\n")
        f.write("    length: 255\n")
        f.write("    nullable: False\n")
        f.write("    value: default_field\n")
        f.write("    description: Field name for the unpivoted data\n")
        f.write("  - name: value\n")
        f.write('    "@id": "#visit1_efd_unpivoted.value"\n')
        f.write("    datatype: double\n")
        f.write("    nullable: True\n")
        f.write("    description: Value corresponding to the parameter\n")
        f.write("  - name: created_at\n")
        f.write('    "@id": "#visit1_efd_unpivoted.created_at"\n')
        f.write("    datatype: timestamp\n")
        f.write("    value: 'CURRENT_TIMESTAMP'\n")
        f.write("    description: Timestamp when the record was created, default is the current timestamp\n")
        f.write("\n")

        # Generate transformed_efd scheduler table.
        f.write("- name: transformed_efd_scheduler\n")
        f.write('  "@id": "#transformed_efd_scheduler"\n')
        f.write("  description: Transformed EFD scheduler.\n")
        f.write("  primaryKey:\n")
        f.write('  - "#transformed_efd_scheduler.id"\n')
        f.write("  constraints:\n")
        f.write("  - name: un_id\n")
        f.write('    "@id": "#transformed_efd_scheduler.un_id"\n')
        f.write('    "@type": Unique\n')
        f.write("    description: Ensure id is unique.\n")
        f.write("    columns:\n")
        f.write('    - "#transformed_efd_scheduler.id"\n')
        f.write("  columns:\n")
        f.write("  - name: id\n")
        f.write('    "@id": "#transformed_efd_scheduler.id"\n')
        f.write("    datatype: int\n")
        f.write("    nullable: False\n")
        f.write("    autoincrement: True\n")
        f.write("    description: Unique ID, auto-incremented\n")
        f.write("  - name: start_time\n")
        f.write('    "@id": "#transformed_efd_scheduler.start_time"\n')
        f.write("    datatype: timestamp\n")
        f.write("    description: Start time of the transformation interval, must be provided\n")
        f.write("  - name: end_time\n")
        f.write('    "@id": "#transformed_efd_scheduler.end_time"\n')
        f.write("    datatype: timestamp\n")
        f.write("    description: End time of the transformation interval, must be provided\n")
        f.write("  - name: timewindow\n")
        f.write('    "@id": "#transformed_efd_scheduler.timewindow"\n')
        f.write("    datatype: int\n")
        f.write("    description: Time window used to expand start and end times by, in minutes\n")
        f.write("  - name: status\n")
        f.write('    "@id": "#transformed_efd_scheduler.status"\n')
        f.write("    datatype: char\n")
        f.write("    length: 20\n")
        f.write('    value: "pending"\n')
        f.write("    description: Status of the process, default is 'pending'\n")
        f.write("  - name: process_start_time\n")
        f.write('    "@id": "#transformed_efd_scheduler.process_start_time"\n')
        f.write("    datatype: timestamp\n")
        f.write("    description: Timestamp when the process started\n")
        f.write("  - name: process_end_time\n")
        f.write('    "@id": "#transformed_efd_scheduler.process_end_time"\n')
        f.write("    datatype: timestamp\n")
        f.write("    description: Timestamp when the process ended\n")
        f.write("  - name: process_exec_time\n")
        f.write('    "@id": "#transformed_efd_scheduler.process_exec_time"\n')
        f.write("    datatype: int\n")
        f.write("    value: 0\n")
        f.write("    description: Execution time of the process in seconds, default is 0\n")
        f.write("  - name: exposures\n")
        f.write('    "@id": "#transformed_efd_scheduler.exposures"\n')
        f.write("    datatype: int\n")
        f.write("    value: 0\n")
        f.write("    description: Number of exposures processed, default is 0\n")
        f.write("  - name: visits1\n")
        f.write('    "@id": "#transformed_efd_scheduler.visits1"\n')
        f.write("    datatype: int\n")
        f.write("    value: 0\n")
        f.write("    description: Number of visits recorded, default is 0\n")
        f.write("  - name: retries\n")
        f.write('    "@id": "#transformed_efd_scheduler.retries"\n')
        f.write("    datatype: int\n")
        f.write("    value: 0\n")
        f.write("    description: Number of retries attempted, default is 0\n")
        f.write("  - name: error\n")
        f.write('    "@id": "#transformed_efd_scheduler.error"\n')
        f.write("    datatype: text\n")
        f.write('    description: "Error message, if any"\n')
        f.write("  - name: created_at\n")
        f.write('    "@id": "#transformed_efd_scheduler.created_at"\n')
        f.write("    datatype: timestamp\n")
        f.write("    value: 'CURRENT_TIMESTAMP'\n")
        f.write("    description: Timestamp when the record was created, default is the current timestamp\n")

    f.close()
