#!/bin/bash

# List of database names to upgrade and downgrade
databases=("latiss" "lsstcomcam" "lsstcomcamsim")
# "startrackerfast" "startrackernarrow" "startrackerwide")  # Replace with your actual database names
# Loop through each database and perform the sequence of Alembic commands
for db_name in "${databases[@]}"; do
    echo "Processing database: $db_name"

    # First upgrade to the latest version
    echo "Upgrading $db_name to the latest version..."
    alembic -n "$db_name" upgrade head
    echo "------------------------------------------"

    # Downgrade by one version
    echo "Downgrading $db_name by one version..."
    alembic -n "$db_name" downgrade -1
    echo "------------------------------------------"

    # Final upgrade back to the latest version
    echo "Upgrading $db_name back to the latest version..."
    alembic -n "$db_name" upgrade head
    echo "------------------------------------------"
done
