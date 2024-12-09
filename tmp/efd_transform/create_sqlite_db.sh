#!/bin/bash

# Check if the instrument argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <instrument>"
  echo "Allowed instruments: LATISS, LSSTComCam, LSSTComCamSim, LSSTCam, LSSTCamSim, startracker"
  exit 1
fi

# Set the instrument from the first argument
INSTRUMENT="$1"

# Validate the instrument against the allowed options
case "$INSTRUMENT" in
  LATISS|LSSTComCam|LSSTComCamSim|LSSTCam|LSSTCamSim|startracker)
    ;;
  *)
    echo "Error: Invalid instrument '$INSTRUMENT'."
    echo "Allowed instruments: LATISS, LSSTComCam, LSSTComCamSim, LSSTCam, LSSTCamSim, startracker"
    exit 1
    ;;
esac

# Set the configuration file based on the instrument
CONFIG="config_${INSTRUMENT}.yaml"
echo "Using configuration file: $CONFIG"

# Navigate to the directory containing the schema generation script
echo "Navigating to the schema generation directory..."
cd python/lsst/consdb/efd_transform || exit

# Generate the schema using the configuration and instrument
echo "Generating schema for $INSTRUMENT..."
python generate_schema.py --config "$CONFIG" --instrument "$INSTRUMENT"

# Check if the schema generation was successful
if [ ! -f "cdb_transformed_efd_${INSTRUMENT}.yaml" ]; then
  echo "Error: Failed to generate cdb_transformed_efd_${INSTRUMENT}.yaml"
  exit 1
fi
echo "Schema generated: cdb_transformed_efd_${INSTRUMENT}.yaml"

# Remove the old transformed file in the test directory
echo "Removing old transformed schema file (if any)..."
rm -f ../../../../tmp/efd_transform/cdb_transformed_efd_${INSTRUMENT}.yaml

# Copy the new transformed file to the test directory
echo "Copying the new transformed schema file to the test directory..."
cp "cdb_transformed_efd_${INSTRUMENT}.yaml" ../../../../tmp/efd_transform/

# Navigate to the test directory
echo "Navigating to the test directory..."
cd ../../../../tmp/efd_transform/ || exit

# Remove the old database file for the instrument
echo "Removing old database file (if any)..."
rm -f "${INSTRUMENT}.db"

# Create the SQL file with Felis
echo "Creating the SQL file with Felis..."
felis create --dry-run --engine-url sqlite://// "cdb_transformed_efd_${INSTRUMENT}.yaml" > "${INSTRUMENT}-sqlite.sql"
felis create --engine-url sqlite:///${INSTRUMENT}.db "cdb_transformed_efd_${INSTRUMENT}.yaml"

# Create postgresql code for the database
echo "Creating the SQL file with Felis for postgres..."
felis create --dry-run --engine-url postgresql+psycopg2://username:password@localhost/database "cdb_transformed_efd_${INSTRUMENT}.yaml" > "${INSTRUMENT}-pg.sql"
