# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Utility functions for consdb services.
"""
import logging
import os
import re
import sys

import sqlalchemy

__all__ = ["setup_postgres", "setup_logging"]


logger = logging.getLogger(__name__)


def setup_postgres() -> sqlalchemy.Engine:
    """Set up a SQLAlchemy Engine to talk to Postgres.

    Uses environment variables to get connection information, with an internal
    default.

    Returns
    -------
    engine: ``sqlalchemy.Engine``
        A SQLAlchemy Engine.
    """
    host = os.environ.get("DB_HOST")
    passwd = os.environ.get("DB_PASS")
    user = os.environ.get("DB_USER")
    dbname = os.environ.get("DB_NAME")
    pg_url = ""
    if host and passwd and user and dbname:
        logger.info(f"Connecting to {host} as {user} to {dbname}")
        pg_url = f"postgresql://{user}:{passwd}@{host}/{dbname}"
    else:
        pg_url = os.environ["POSTGRES_URL"]
        logger.info(f"Using POSTGRES_URL {pg_url}")
    engine = sqlalchemy.create_engine(pg_url, pool_recycle=3600, pool_pre_ping=True)
    if pg_url.startswith("sqlite:///"):
        # For unit tests
        start_pos = len("sqlite:///")
        end_pos = pg_url.rindex("/")
        db_path = pg_url[start_pos:end_pos]
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table("schemas", metadata, autoload_with=engine)
        stmt = sqlalchemy.select(table.c.name, table.c.path)
        schemas = dict()
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                schemas[row.name] = row.path
        with engine.connect() as conn:
            for schema, path in schemas.items():
                path = os.path.join(db_path, path)
                conn.exec_driver_sql(f"ATTACH DATABASE '{path}' AS {schema}")
    return engine


def setup_logging(module: str) -> logging.Logger:
    """Set up logging for a service.

    Levels for any logger component may be set via the LOG_CONFIG environment
    variable as a comma-separated list of "component=LEVEL" settings.  The
    special "." component refers to the root level of the LSST Science
    Pipelines loggers.

    Parameter
    ---------
    module: `str`
        The ``__name__`` of the calling module.

    Returns
    -------
    logger: `logging.Logger`
        The logger to use for the module.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="{levelname} {asctime} {name} ({filename}:{lineno}) - {message}",
        style="{",
        stream=sys.stderr,
        force=True,
    )

    logger = logging.getLogger(module)

    logspec = os.environ.get("LOG_CONFIG")
    if logspec:
        # One-line "component=LEVEL" logging specification parser.
        for component, level in re.findall(r"(?:([\w.]*)=)?(\w+)", logspec):
            if component == ".":
                # Specially handle "." as a component to mean the lsst root
                component = "lsst"
            logging.getLogger(component).setLevel(level)

    return logger
