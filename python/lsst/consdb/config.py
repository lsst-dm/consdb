"""Configuration definition."""

import logging
import re
import sys

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

__all__ = ["Configuration", "config"]


class Configuration(BaseSettings):
    """Configuration for consdb."""

    name: str = Field("pqserver", title="Application name")

    version: str = Field("NOVERSION", title="Application version number")

    url_prefix: str = Field("/consdb", title="URL prefix")

    db_host: str = Field("localhost", title="The hostname for the SQL database.")

    db_user: str | None = Field(None, title="The database username for the SQL database.")

    db_pass: str | None = Field(None, title="The SQL database password.")

    db_name: str | None = Field(None, title="The name of the SQL database to connect to.")

    log_config: str = Field(
        "",
        title="Log levels",
        description="""Log levels.

            Use the LOG_CONFIG environment variable to specify logging levels for
            any components. Examples:
             * `lsst.consdb=DEBUG`
             * `consdb.pqserver=DEBUG INFO`
             * `consdb.hinfo=DEBUG consdb.pqserver=WARNING`
             * `.=CRITICAL`
            The "." can be used as a shorthand to mean the `lsst` root.
        """,
    )

    postgres_url: str | None = Field(None, title="Database URL set by POSTGRES_URL.")

    consdb_url: str | None = Field(None, title="Database URL set by CONSDB_URL")

    description: str | None = Field(
        "A web interface to the Rubin Observatory Consolidated Database.", title="Application description."
    )

    repository_url: str | None = Field(
        "https://github.com/lsst-dm/consdb", title="Source repository for this code."
    )

    documentation_url: str | None = Field(
        "https://consdb.lsst.io/index.html", title="URL for documentation of this project."
    )

    @property
    def database_url(self) -> str:
        """Infers the database URL based on the provided configuration.

        The URL is constructed as follows, in order of priority:
        * If POSTGRES_URL environment variable is set, this is
          used as the database URL.
        * If CONSDB_URL environment variable is set, this is used.
        * If all of DB_HOST, DB_USER, DB_PASS, and DB_NAME are
          set, the URL is constructed from this information.
        """

        if self.postgres_url:
            return self.postgres_url

        if self.consdb_url:
            return self.consdb_url

        if all([self.db_host, self.db_user, self.db_pass, self.db_name]):
            url = f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}"
            self.postgres_url = url
            return url

        raise ValueError("Database connection not specified")

    @field_validator("log_config")
    @classmethod
    def configure_logging(cls, log_config, values):
        logging.basicConfig(
            level=logging.INFO,
            format="{levelname} {asctime} {name} ({filename}:{lineno}) - {message}",
            style="{",
            stream=sys.stderr,
            force=True,
        )

        # Set up logging using the logspec field
        # One-line "component=LEVEL" logging specification parser.
        for component, level in re.findall(r"(?:([\w.]*)=)?(\w+)", log_config):
            if component == ".":
                # Specially handle "." as a component to mean the lsst root
                component = "lsst"
            logging.getLogger(component).setLevel(level)

        return log_config


config = Configuration()
"""Configuration for consdb."""
