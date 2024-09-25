#!/usr/bin/env python

#
# How to use this script:
# 1. Load the LSST environment and setup sdm_schemas and felis.
#        source loadLSST.bash
#        setup felis
#        setup -r /path/to/sdm_schemas
# 2. Set the SDM_SCHEMAS_DIR environment variable to point to your sdm_schemas
#    tree. The schema yaml files should be in
#    $SDM_SCHEMAS_DIR/yml/cdb_latiss.yaml,
#    $SDM_SCHEMAS_DIR/yml/cdb_lsstcomcam.yaml, etc.
# 3. From the root of the consdb git repo, invoke the script. Supply a
#    revision message as the command line argument:
#        python alembic-autogenerate.py this is my revision message "\n" \
#            the message can span multiple lines "\n" \
#            if desired
# 4. Heed the message at the end to revise your auto-generated code as needed.
#

import glob
import os
import re
import sys

from alembic.config import Config
from alembic import command
from sqlalchemy.sql import text

from felis.tests.postgresql import setup_postgres_test_db

if len(sys.argv) <= 1:
    print("""
    Usage:
        {sys.argv[0]} put a revision message here")

    """)
    sys.exit(1)

revision_message = ' '.join(sys.argv[1:])

# Configuration for Alembic
alembic_ini_path = "alembic.ini"

# Loop over each of the instruments
pattern = os.environ["SDM_SCHEMAS_DIR"] + "/yml/cdb_*.yaml"
instruments = [re.search(r"cdb_(.+)\.yaml$", file).group(1) for file in glob.glob(pattern)]
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

print("""
==========================================
 Don't forget to edit your migration
 files! You'll need to remove the visit1
 and ccdvisit1 tables, and you might need
 to shuffle data around to accomodate the
 new schema!
==========================================
""")
