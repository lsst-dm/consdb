#!/bin/bash

# List of database names to check
databases=("latiss" "lsstcomcam" "lsstcomcamsim" "startrackerfast" "startrackernarrow" "startrackerwide")  # Replace with your actual database names

# Loop through each database and run Alembic commands
for db_name in "${databases[@]}"; do
    echo "Checking Alembic status for database: $db_name"

    echo "Running 'alembic current' for $db_name..."
    alembic -n "$db_name" current
    echo
    echo
    echo

    echo "Running 'alembic history' for $db_name..."
    alembic -n "$db_name" history
    echo
    echo "------------------------------------------"
done
