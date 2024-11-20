"""Configuration definition."""

import logging
import re
from pydantic import Field
from pydantic_settings import BaseSettings, validator

__all__ = ["Configuration", "config"]


class Configuration(BaseSettings):
    """Configuration for consdb."""

    url_prefix: str = Field("consdb", title="URL prefix")

    db_host: str = Field("localhost", title="The hostname for the SQL database.")

    db_user: str = Field(None, title="The database username for the SQL database.")

    db_pass: str = Field(None, title="The SQL database password.")

    db_name: str = Field(None, title="The name of the SQL database to connect to.")

    log_config: str = Field(
        None,
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

    postgres_url: str = Field(None, title="Database URL set by POSTGRES_URL.")

    consdb_url: str = Field(None, title="Database URL set by CONSDB_URL")

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

        raise ValueError("Database connection info not specified.")

    @validator("log_config")
    def configure_logging(self, log_config):
        # Set up logging using the logspec field
        # One-line "component=LEVEL" logging specification parser.
        for component, level in re.findall(r"(?:([\w.]*)=)?(\w+)", log_config):
            if component == ".":
                # Specially handle "." as a component to mean the lsst root
                component = "lsst"
            logging.getLogger(component).setLevel(level)


config = Configuration()
"""Configuration for consdb."""
