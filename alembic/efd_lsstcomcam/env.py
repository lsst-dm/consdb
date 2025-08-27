import logging
import os
from logging.config import fileConfig

import yaml
from dotenv import load_dotenv
from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder
from sqlalchemy import engine_from_config, pool

from alembic import context

# TODO: Coordinate appropriately schema locations and remove load_dotenv
load_dotenv()

# Near the top of env.py, after imports
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("alembic").setLevel(logging.DEBUG)


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

# Load the Felis schema from the path specified in the alembic.ini file
sdm_schemas_dir = os.getenv("SDM_SCHEMAS_DIR")
if sdm_schemas_dir is None:
    raise ValueError("SDM_SCHEMAS_DIR not found in environment")

schema_name = context.config.get_main_option("consdb.schema_name")
logger.info(f"Schema name: {schema_name}")
schema_path = f"{sdm_schemas_dir}/yml/{schema_name}.yaml"
logger.info(f"Using schema path: {schema_path}")
yaml_data = yaml.safe_load(open(schema_path, "r"))
schema = Schema.model_validate(yaml_data)
schema_metadata = MetaDataBuilder(schema).build()
logger.info(f"Schema {schema_metadata.schema} loaded successfully")


def include_name(name, type_, parent_names):
    global schema_name
    if type_ == "schema":
        return name == schema_name
    else:
        return True


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in ["ccdvisit1", "visit1"]:
        logger.info(f"Excluding table {object.schema}.{name}")
        return False
    else:
        return True


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = schema_metadata

# Add this after schema_metadata is built
logger.debug(f"Tables in metadata: {list(target_metadata.tables.keys())}")
logger.debug(f"Metadata details: {repr(target_metadata)}")

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        include_object=include_object,
        version_table="efd_lsstcomcam_version",
        # version_table=f"{schema_name}_version",
        version_table_schema="efd2",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            include_object=include_object,
            version_table="efd_lsstcomcam_version",
            # version_table=f"{schema_name}_version",
            version_table_schema="efd2",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
