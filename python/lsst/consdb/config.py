"""Configuration definition."""

import logging
import re
import sys

from pydantic import Field, field_validator, model_validator
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

    pool_recycle_time: int | None = Field(
        # Based on idle_session_timeout at summit, 60 minutes.
        # This should be a bit less to avoid a possible race condition.
        50 * 60,
        title="Maximum time to allow a database connection to idle (seconds).",
    )

    statement_timeout_seconds: int = Field(
        600,
        title="Timeout duration for sqlalchemy queries (seconds).",
    )

    max_rows: int = Field(1_000_000, title="Maximum rows allowed by the query endpoint.")

    fetch_size: int = Field(10_000, title="Number of rows to fetch at once in the query endpoint.")

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

    write_auth_enabled: bool = Field(
        False,
        title="Require a Gafaelfawr token to write",
        description="""If true, the insert and flexible metadata write endpoints
            require an ``Authorization: Bearer`` Gafaelfawr token belonging to
            one of the users in ``allowed_writers``. Set by WRITE_AUTH_ENABLED.
        """,
    )

    allowed_writers: list[str] = Field(
        [],
        title="Usernames allowed to write",
        description="""Gafaelfawr usernames (normally service token users such
            as ``bot-rapid-analysis``) allowed to use the write endpoints when
            ``write_auth_enabled`` is true. Set by ALLOWED_WRITERS as a JSON
            list.
        """,
    )

    gafaelfawr_url: str | None = Field(
        None,
        title="Base URL of Gafaelfawr",
        description="""Base URL used to verify tokens, such as
            ``https://summit-lsp.lsst.codes``. Gafaelfawr only accepts traffic
            from its ingress, so this must be the external URL rather than a
            cluster-internal service URL. Set by GAFAELFAWR_URL.
        """,
    )

    gafaelfawr_timeout: float = Field(10.0, title="Timeout for Gafaelfawr requests (seconds).")

    write_auth_cache_seconds: int = Field(
        600,
        title="How long to cache verified token owners (seconds).",
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

    @model_validator(mode="after")
    def check_write_auth(self) -> "Configuration":
        if self.write_auth_enabled and not self.gafaelfawr_url:
            raise ValueError("GAFAELFAWR_URL must be set when WRITE_AUTH_ENABLED is true")
        return self

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
