import logging
import os
from logging.config import fileConfig

import yaml
from felis.datamodel import Schema
from felis.metadata import MetaDataBuilder
from sqlalchemy import engine_from_config, pool

from alembic import context

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
schema_path = f"{sdm_schemas_dir}/yml/{schema_name}.yaml"
logger.info(f"Using schema path: {schema_path}")
yaml_data = yaml.safe_load(open(schema_path, "r"))
schema = Schema.model_validate(yaml_data)
schema_metadata = MetaDataBuilder(schema).build()
logger.info(f"Schema {schema_metadata.schema} loaded successfully")


def generate_upgrade_sqls(schema_metadata, schema_name) -> list[str]:
    sql = []
    for prefix in ("", "ccd"):
        table = schema_metadata.tables[f"{schema_name}.{prefix}exposure"]

        cols = [col.name for col in table.columns]
        view_columns = []
        for col in cols:
            if col == "ccdexposure_id":
                view_columns.append("ccdexposure_id AS ccdvisit_id")
            elif col == "exposure_id":
                view_columns.append("exposure_id AS visit_id")
            else:
                view_columns.append(col)

        view_name = f"{prefix}visit1"
        view_sql = f"""
        CREATE OR REPLACE VIEW {schema_name}.{view_name} AS
        SELECT {', '.join(view_columns)}
        FROM {schema_name}.{prefix}exposure;
        """
        sql.append(view_sql.strip())

        for role in ("usdf", "oods"):
            sql.append(
                f"GRANT SELECT ON {schema_name}.{view_name} TO {role};"
            )

    return sql


def generate_downgrade_sqls(schema_name) -> list[str]:
    return [
        f"CREATE VIEW {schema_name}.ccdvisit1 AS SELECT * FROM {schema_name}.ccdexposure",
        f"CREATE VIEW {schema_name}.visit1 AS SELECT * FROM {schema_name}.exposure",
        f"ALTER TABLE {schema_name}.ccdvisit1 RENAME COLUMN ccdexposure_id TO ccdvisit_id",
        f"ALTER TABLE {schema_name}.ccdvisit1 RENAME COLUMN exposure_id TO visit_id",
        f"ALTER TABLE {schema_name}.visit1 RENAME COLUMN exposure_id TO visit_id",
        f"GRANT SELECT ON {schema_name}.ccdvisit1 TO usdf",
        f"GRANT SELECT ON {schema_name}.ccdvisit1 TO oods",
        f"GRANT SELECT ON {schema_name}.visit1 TO usdf",
        f"GRANT SELECT ON {schema_name}.visit1 TO oods",
    ]


def generate_drop_sqls(schema_name) -> list[str]:
    return [
        f"DROP VIEW IF EXISTS {schema_name}.ccdvisit1",
        f"DROP VIEW IF EXISTS {schema_name}.visit1",
    ]


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

    # Not sure why Alembic insists on adding these redundantly
    elif type_ == "unique_constraint" and name in {
        "un_ccdexposure_ccdexposure_id",
        "un_exposure_day_obs_seq_num",
        "un_exposure_flexdata_day_obs_seq_num_key",
    }:
        logger.info(f"Excluding unique constraint {name}")
        return False

    else:
        return True


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = schema_metadata

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
        version_table=f"{schema_name}_version",
        version_table_schema="cdb",
    )
    context.config.attributes["upgrade_sqls"] = generate_upgrade_sqls(schema_metadata, schema_name)
    context.config.attributes["drop_sqls"] = generate_drop_sqls(schema_name)
    context.config.attributes["downgrade_sqls"] = generate_downgrade_sqls(schema_name)

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
            version_table=f"{schema_name}_version",
            version_table_schema="cdb",
        )
        context.config.attributes["upgrade_sqls"] = generate_upgrade_sqls(schema_metadata, schema_name)
        context.config.attributes["drop_sqls"] = generate_drop_sqls(schema_name)
        context.config.attributes["downgrade_sqls"] = generate_downgrade_sqls(schema_name)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
