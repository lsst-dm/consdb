import logging
import os
import shutil
import sys
from logging.config import fileConfig
from pathlib import Path

import yaml
from dotenv import load_dotenv
from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder
from lsst.consdb.transformed_efd.generate_schema_from_config import generate_schema
from sqlalchemy import engine_from_config, pool

from alembic import context
from alembic.script import ScriptDirectory

# Load environment variables
# TODO: Substitute by the default env values
load_dotenv()

# Global variables
new_revision_id = None
schema_name = None

# Configuration paths
CONFIG_LATISS_PATH = Path(os.getenv("CONFIG_LATISS_PATH"))
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "versions", "config_snapshots")

# Ensure snapshot directory exists
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

# Set the consdb connection string in the config, overriding the dummy value
consdb_url = os.getenv("CONSDB_URL")
if consdb_url is None:
    raise ValueError("CONSDB_URL not found in environment")
config.set_main_option("sqlalchemy.url", consdb_url)
logger.info(f"Using connection string: {consdb_url}")

# Schema setup
schema_name = config.get_main_option("consdb.schema_name")


# Function to generate schema from config
def prepare_schema(config_path):
    """Generate schema from config and return MetaData."""
    schema_path = generate_schema(config_path=config_path, instrument="latiss")
    return schema_path


# Function to save config snapshot for a migration
def save_config_snapshot(revision):
    """Save config_latiss.yaml snapshot for a migration."""
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{revision}_config_latiss.yaml")
    shutil.copy(CONFIG_LATISS_PATH, snapshot_path)
    logger.info(f"Saved config snapshot: {snapshot_path}")


# Function to restore config snapshot and create a backup
def restore_config_snapshot(revision):
    """Restore config_latiss.yaml from a migration snapshot and create a backup."""
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{revision}_config_latiss.yaml")

    if os.path.exists(snapshot_path):
        # Backup existing config file before restore
        if os.path.exists(CONFIG_LATISS_PATH):
            backup_filename = "previous_" + os.path.basename(CONFIG_LATISS_PATH)
            backup_path = os.path.join(os.path.dirname(CONFIG_LATISS_PATH), backup_filename)
            shutil.copy(CONFIG_LATISS_PATH, backup_path)  # Backup the current config file
            logger.info(f"Backup created: {backup_path}")

        # Restore from snapshot
        shutil.copy(snapshot_path, CONFIG_LATISS_PATH)
        logger.info(f"Restored config from snapshot: {snapshot_path}")
    else:
        logger.warning(f"Snapshot not found for revision: {revision}")


# Function to get config path (current or snapshot)
def get_config_path(revision, is_downgrade):
    """Return path to config_latiss.yaml (current or snapshot)."""
    if is_downgrade:
        return os.path.join(SNAPSHOT_DIR, f"{revision}_config_latiss.yaml")
    return CONFIG_LATISS_PATH


# Function to include schema based on name and type
def include_name(name, type_, parent_names):
    """Filter schemas by name."""
    if type_ == "schema":
        return name == schema_name
    return True


# Function to include objects based on table name
def include_object(object, name, type_, reflected, compare_to):
    """Exclude specific tables (ccdvisit1, visit1)."""
    if type_ == "table" and name in ["ccdvisit1", "visit1"]:
        logger.info(f"Excluding table {object.schema}.{name}")
        return False
    return True


# Function to handle revision directives
def process_revision_directives(context, revision, directives):
    """Store generated revision ID."""
    global new_revision_id
    script = directives[0]
    new_revision_id = script.rev_id  # Store the generated revision ID


# Function to resolve revision from label (head or absolute ID)
def resolve_revision(rev_label):
    """Convert Alembic revision label (absolute revision ID or 'head') into a revision ID."""
    script = ScriptDirectory.from_config(config)

    if rev_label == "head":
        try:
            return script.get_revisions("head")[0].revision
        except IndexError:
            raise ValueError("No revisions found in the migration history.")

    try:
        return script.get_revision(rev_label).revision
    except Exception:
        raise ValueError(f"Invalid revision: {rev_label}")


# Prepare the schema
schema_path = prepare_schema(CONFIG_LATISS_PATH)
logger.info(f"Using schema path: {schema_path}")

# Load schema data from the generated YAML
yaml_data = yaml.safe_load(open(schema_path, "r"))

# Create schema and metadata objects
schema = Schema.model_validate(yaml_data)
schema_metadata = MetaDataBuilder(schema).build()

# Log schema metadata
logger.info(f"Schema {schema_metadata.schema} loaded successfully")


# Function to run migrations in online mode
def run_migrations_online() -> None:
    """Run migrations in 'online' mode with database connection."""
    global new_revision_id

    # Handle revision operations (upgrade/downgrade)
    if "downgrade" in sys.argv:
        target_rev_index = sys.argv.index("downgrade") + 1
        if target_rev_index < len(sys.argv):
            target_revision_id = resolve_revision(sys.argv[target_rev_index])
            restore_config_snapshot(target_revision_id)
        else:
            raise ValueError("Target revision not specified for downgrade")

    if "upgrade" in sys.argv:
        target_rev_index = sys.argv.index("upgrade") + 1
        if target_rev_index < len(sys.argv):
            target_revision_id = resolve_revision(sys.argv[target_rev_index])
            restore_config_snapshot(target_revision_id)
        else:
            raise ValueError("Target revision not specified for upgrade")

    # Set up database engine and connection
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=schema_metadata,
            include_schemas=True,
            include_name=include_name,
            include_object=include_object,
            version_table=f"{schema_name}_version",
            version_table_schema=schema_name,
            process_revision_directives=process_revision_directives,
        )

        # Run migrations within transaction
        with context.begin_transaction():
            context.run_migrations()

        # Log new revision and snapshot if applicable
        if new_revision_id:
            print(f"New revision ID: {new_revision_id}")
            if "--autogenerate" in sys.argv:
                logger.info(f"Autogenerating revision: {new_revision_id}")
                save_config_snapshot(new_revision_id)


# Main script execution
if context.is_offline_mode():
    logger.warning("Offline mode is not supported for this migration.")
else:
    run_migrations_online()
