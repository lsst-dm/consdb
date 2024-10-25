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
CONFIG="config_${INSTRUMENT}.yml"
echo "Using configuration file: $CONFIG"

# Navigate to the directory containing the schema generation script
echo "Navigating to the schema generation directory..."
cd python/lsst/consdb/efd_transform || exit

# Generate the schema using the configuration and instrument
echo "Generating schema for $INSTRUMENT..."
python generate_schema.py --config "$CONFIG" --instrument "$INSTRUMENT"

# Check if the schema generation was successful
if [ ! -f "cdb_transformed_efd_${INSTRUMENT}.yml" ]; then
  echo "Error: Failed to generate cdb_transformed_efd_${INSTRUMENT}.yml"
  exit 1
fi
echo "Schema generated: cdb_transformed_efd_${INSTRUMENT}.yml"

# Remove the old transformed file in the test directory
echo "Removing old transformed schema file (if any)..."
rm -f ../../../../tests/efd_transform/cdb_transformed_efd_${INSTRUMENT}.yml

# Copy the new transformed file to the test directory
echo "Copying the new transformed schema file to the test directory..."
cp "cdb_transformed_efd_${INSTRUMENT}.yml" ../../../../tests/efd_transform/

# Navigate to the test directory
echo "Navigating to the test directory..."
cd ../../../../tests/efd_transform/ || exit

# Remove the old database file for the instrument
echo "Removing old database file (if any)..."
rm -f "${INSTRUMENT}.db"

# Create the SQL file with Felis
echo "Creating the SQL file with Felis..."
felis create --dry-run --engine-url sqlite:/// "cdb_transformed_efd_${INSTRUMENT}.yml" > "${INSTRUMENT}.sql"

# Check if the SQL file creation was successful
if [ ! -f "${INSTRUMENT}.sql" ]; then
  echo "Error: Failed to create ${INSTRUMENT}.sql"
  exit 1
fi
echo "SQL file created: ${INSTRUMENT}.sql"

# Load the SQL file into a new SQLite database
echo "Loading SQL into the new SQLite database..."
sqlite3 "${INSTRUMENT}.db" < "${INSTRUMENT}.sql"

# Confirm successful completion
if [ $? -eq 0 ]; then
  echo "Database ${INSTRUMENT}.db created successfully."
else
  echo "Error: Failed to create the SQLite database."
  exit 1
fi
