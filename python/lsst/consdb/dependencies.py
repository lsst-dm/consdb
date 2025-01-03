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

import logging

from fastapi import Path, Request
from pydantic import AfterValidator
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from typing import Annotated

from .config import config
from .cdb_schema import InstrumentTable
from .exceptions import UnknownInstrumentException

__all__ = ["get_logger", "get_db"]

_database_url = None
_engine = None
_SessionLocal = None


def get_engine():
    global _database_url, _engine

    # Set up the database engine...
    if _database_url is None:
        try:
            _database_url = config.database_url
            print(f"{_database_url=}")
        except ValueError:
            log = logging.getLogger(__name__)
            log.warning("Database URL was not available.")
            raise

    if _engine is None:
        _engine = create_engine(config.database_url)

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


instrument_tables: dict[str, InstrumentTable] = dict()
instrument_list: list[str] | None = None


def get_instrument_table(instrument: str):
    global instrument_list
    global instrument_tables

    instrument = instrument.lower()
    logger = logging.getLogger()
    engine = get_engine()

    # Check whether the instrument name is valid
    if instrument_list is None:
        inspector = inspect(engine)
        instrument_list = [name[4:] for name in inspector.get_schema_names() if name.startswith("cdb_")]

    if instrument not in [i.lower() for i in instrument_list]:
        raise UnknownInstrumentException(instrument)

    if instrument in instrument_tables:
        instrument_table = instrument_tables[instrument]
    else:
        instrument_table = InstrumentTable(
            engine=engine, instrument=instrument, get_db=get_db, logger=logger
        )
        instrument_tables[instrument] = instrument_table

    return instrument_table


def get_instrument_list():
    global instrument_list
    if instrument_list is None:
        inspector = inspect(get_engine())
        instrument_list = [name[4:] for name in inspector.get_schema_names() if name.startswith("cdb_")]

    return instrument_list


def validate_instrument_name(
    instrument: str = Path(description="Must be a valid instrument name (e.g., ``LATISS``)"),
) -> str:
    print(f"validate_instrument_name({instrument=})")
    instrument_lower = instrument.lower()
    if instrument_lower not in [i.lower() for i in get_instrument_list()]:
        raise UnknownInstrumentException(instrument)
    return instrument


InstrumentName = Annotated[str, AfterValidator(validate_instrument_name)]


def reset_dependencies():
    global _database_url, _engine, _SessionLocal, instrument_table, instrument_list
    _database_url = None
    _engine = None
    _SessionLocal = None
    instrument_table = None
    instrument_list = None
