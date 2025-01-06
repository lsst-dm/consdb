#!/usr/bin/env python

#
# How to use this script:
# 1. Install required packages and sdm_schemas, set environment variables:
#        pip install lsst-felis testing.postgresql alembic sqlalchemy pyyaml \
#           black psycopg2-binary
#        git clone https://github.com/lsst/sdm_schemas
#        cd sdm_schemas
#        export SDM_SCHEMAS_DIR=`pwd```
# 2. From the root of the consdb git repo, invoke the script. Supply a
#    revision message as the command line argument:
#        python alembic-autogenerate.py this is my revision message "\n" \
#            the message can span multiple lines "\n" \
#            if desired
# 3. Revise your auto-generated code as needed.
# 4. Remove the autogenerated creation of sql views (visit1, ccdvisit1).
#

import os
import sys

from felis.tests.postgresql import setup_postgres_test_db
from sqlalchemy.sql import text

from alembic import command
from alembic.config import Config

if len(sys.argv) <= 1:
    print(
        """
    Usage:
        {sys.argv[0]} put a revision message here")

    """
    )
    sys.exit(1)

revision_message = " ".join(sys.argv[1:])

# Configuration for Alembic
alembic_ini_path = "alembic.ini"

# Loop over each of the instruments
pattern = os.environ["SDM_SCHEMAS_DIR"] + "/yml/cdb_*.yaml"
instruments = ["latiss", "lsstcomcam", "lsstcomcamsim"]
for instrument in instruments:
    # Set up a temporary PostgreSQL instance using testing.postgresql
    with setup_postgres_test_db() as instance:
        os.environ["CONSDB_URL"] = instance.url
        # Create schema
        with instance.engine.connect() as connection:
            connection.execute(text("CREATE SCHEMA cdb;"))
            connection.execute(text(f"CREATE SCHEMA cdb_{instrument};"))
            connection.commit()

        # Initialize Alembic configuration
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("sqlalchemy.url", instance.url)
        alembic_cfg.config_ini_section = instrument

        # Apply the HEAD schema to the database
        command.upgrade(alembic_cfg, "head")

        # Autogenerate a new migration
        command.revision(alembic_cfg, autogenerate=True, message=revision_message)

print(
    """
==========================================
 Don't forget to edit your migration files.
 You might need to shuffle data around
 to accommodate the new schema!
==========================================
"""
)
