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

import hashlib
import logging
import threading
import time
from functools import cache
from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, Path, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import AfterValidator
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from .cdb_schema import InstrumentTable
from .config import config
from .exceptions import UnknownInstrumentException

__all__ = ["get_db", "get_logger", "require_writer"]

_database_url = None
_engine = None
_SessionLocal = None
_instrument_tables: dict[str, InstrumentTable] = {}

_bearer = HTTPBearer(
    auto_error=False,
    description="Gafaelfawr token, required by write endpoints if write authorization is enabled.",
)

# Maps a SHA-256 hash of a token to its owner and the time of expiration of
# the cached entry.
_token_owner_cache: dict[str, tuple[str, float]] = {}
_token_owner_lock = threading.Lock()


def get_engine():
    global _database_url, _engine

    # Set up the database engine...
    if _database_url is None:
        try:
            _database_url = config.database_url
        except ValueError:
            log = logging.getLogger(__name__)
            log.warning("Database URL was not available.")
            raise

    if _engine is None:
        _engine = create_engine(
            config.database_url,
            pool_pre_ping=True,
            pool_recycle=config.pool_recycle_time,
        )

    return _engine


def get_db():
    global _SessionLocal

    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, bind=get_engine())

    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_logger(request: Request):
    endpoint_name = request.url.path
    return logging.getLogger(endpoint_name)


def get_instrument_table(instrument: str, engine: Engine = Depends(get_engine)):
    # global _instrument_tables

    instrument = validate_instrument_name(instrument)
    logger = logging.getLogger("consdb.pqserver")

    if instrument in _instrument_tables:
        instrument_table = _instrument_tables[instrument]
    else:
        instrument_table = InstrumentTable(engine=engine, instrument=instrument, get_db=get_db, logger=logger)
        _instrument_tables[instrument] = instrument_table

    return instrument_table


@cache
def get_instrument_list():
    inspector = inspect(get_engine())
    return [name[4:] for name in inspector.get_schema_names() if name.startswith("cdb_")]


def validate_instrument_name(
    instrument: str = Path(description="Must be a valid instrument name (e.g., ``LATISS``)"),
) -> str:
    instrument_lower = instrument.lower()
    instrument_list = get_instrument_list()
    if instrument_lower not in [i.lower() for i in instrument_list]:
        raise UnknownInstrumentException(instrument, instrument_list)
    return instrument_lower


InstrumentName = Annotated[str, AfterValidator(validate_instrument_name)]


def _get_token_owner(token: str) -> str:
    """Return the username that owns a Gafaelfawr token.

    Results are cached for ``config.write_auth_cache_seconds``, or until the
    token expires if that is sooner.

    Raises
    ------
    HTTPException
        401 if Gafaelfawr rejects the token, 503 if Gafaelfawr could not be
        reached or returned an unexpected response.
    """
    # Check the cache
    key = hashlib.sha256(token.encode()).hexdigest()
    now = time.time()
    with _token_owner_lock:
        cached = _token_owner_cache.get(key)
    if cached and cached[1] > now:
        return cached[0]

    logger = logging.getLogger("consdb.pqserver")
    if not config.gafaelfawr_url:
        logger.error("Write authorization is enabled but GAFAELFAWR_URL is not set")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify token",
        )
    url = f"{config.gafaelfawr_url.rstrip('/')}/auth/api/v1/token-info"
    try:
        response = httpx.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=config.gafaelfawr_timeout,
        )
    except httpx.HTTPError as e:
        logger.error(f"Unable to reach Gafaelfawr at {url}: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify token",
        ) from e

    if response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if response.status_code != status.HTTP_200_OK:
        logger.error(f"Unexpected {response.status_code} response from Gafaelfawr: {response.text}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify token",
        )

    info = response.json()
    username = info["username"]
    expires_at = now + config.write_auth_cache_seconds
    if info.get("expires") is not None:
        expires_at = min(expires_at, float(info["expires"]))
    with _token_owner_lock:
        _token_owner_cache[key] = (username, expires_at)
    return username


def require_writer(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> str | None:
    """Require that the caller is allowed to write to the database.

    Does nothing unless ``config.write_auth_enabled`` is true. Otherwise the
    request must carry an ``Authorization: Bearer`` Gafaelfawr token whose
    owner, as reported by Gafaelfawr, is listed in ``config.allowed_writers``.

    The token is verified with Gafaelfawr rather than trusting
    ``X-Auth-Request-User``, because clients inside the cluster can reach
    pqserver directly and could set that header themselves.

    Returns
    -------
    username : `str` | `None`
        The verified username, or `None` if write authorization is disabled.

    Raises
    ------
    HTTPException
        401 if no valid token was provided, 403 if the token's owner is not
        an allowed writer, 503 if the token could not be verified.
    """
    if not config.write_auth_enabled:
        return None

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A bearer token is required to write to consdb",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = _get_token_owner(credentials.credentials)
    if username not in config.allowed_writers:
        logging.getLogger("consdb.pqserver").warning(
            f"Rejected write by {username} to {request.method} {request.url.path}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{username} is not permitted to write to consdb",
        )
    return username


def reset_dependencies():
    global _database_url, _engine, _SessionLocal, _instrument_tables
    _database_url = None
    _engine = None
    _SessionLocal = None
    _instrument_tables = {}
    get_instrument_list.cache_clear()
    with _token_owner_lock:
        _token_owner_cache.clear()
