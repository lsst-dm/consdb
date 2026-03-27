# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Tests for multi-database write support in DBBase."""

import logging
from unittest.mock import MagicMock, patch

import pytest
from lsst.consdb.transformed_efd.dao.base import DBBase


@pytest.fixture
def logger():
    log = logging.getLogger("test_multi_db")
    log.setLevel(logging.DEBUG)
    if not log.handlers:
        log.addHandler(logging.StreamHandler())
    return log


class TestDBBaseInit:
    def test_single_uri_string(self, logger):
        """Single URI string should be normalized to a one-element list."""
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase("sqlite:///test.db", logger=logger)
        assert db.db_uris == ["sqlite:///test.db"]
        assert db.db_uri == "sqlite:///test.db"
        assert len(db._engines) == 1

    def test_single_uri_in_list(self, logger):
        """A list with one URI should behave identically to a string."""
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase(["sqlite:///test.db"], logger=logger)
        assert db.db_uris == ["sqlite:///test.db"]
        assert db.db_uri == "sqlite:///test.db"
        assert len(db._engines) == 1

    def test_multiple_uris(self, logger):
        """Multiple URIs should be stored; primary is the first."""
        uris = ["postgresql://prod/db", "postgresql://dev/db"]
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase(uris, logger=logger)
        assert db.db_uris == uris
        assert db.db_uri == "postgresql://prod/db"
        assert len(db._engines) == 2

    def test_dialect_from_primary(self, logger):
        """Dialect should be inferred from the primary URI."""
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase("sqlite:///test.db", logger=logger)
        from sqlalchemy.dialects import sqlite

        assert db.dialect is sqlite

    def test_unsupported_dialect_raises(self, logger):
        with pytest.raises(Exception, match="not yet been implemented"):
            DBBase("mysql://localhost/db", logger=logger)


class TestWriteToAllEngines:
    def test_single_engine_returns_result(self, logger):
        """With one engine, _write_to_all_engines should return
        write_fn result."""
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase("sqlite:///test.db", logger=logger)

        mock_engine = MagicMock()
        db._engines = [mock_engine]

        result = db._write_to_all_engines(lambda engine: 42)
        assert result == 42

    def test_multiple_engines_returns_primary_result(self, logger):
        """Should return the primary engine's result."""
        uris = ["postgresql://prod/db", "postgresql://dev/db"]
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase(uris, logger=logger)

        mock_primary = MagicMock()
        mock_secondary = MagicMock()
        db._engines = [mock_primary, mock_secondary]

        results = []

        def write_fn(engine):
            if engine is mock_primary:
                results.append("primary")
                return 10
            else:
                results.append("secondary")
                return 5

        result = db._write_to_all_engines(write_fn)
        assert result == 10
        assert results == ["primary", "secondary"]

    def test_primary_failure_raises(self, logger):
        """If primary fails, the exception should propagate."""
        uris = ["postgresql://prod/db", "postgresql://dev/db"]
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase(uris, logger=logger)

        mock_primary = MagicMock()
        mock_secondary = MagicMock()
        db._engines = [mock_primary, mock_secondary]

        def write_fn(engine):
            if engine is mock_primary:
                raise ConnectionError("Primary down")
            return 5

        with pytest.raises(ConnectionError, match="Primary down"):
            db._write_to_all_engines(write_fn)

    def test_secondary_failure_logs_and_continues(self, logger):
        """If secondary fails, should log error and return primary result."""
        uris = ["postgresql://prod/db", "postgresql://dev/db"]
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase(uris, logger=logger)

        mock_primary = MagicMock()
        mock_secondary = MagicMock()
        db._engines = [mock_primary, mock_secondary]

        def write_fn(engine):
            if engine is mock_secondary:
                raise ConnectionError("Secondary down")
            return 10

        result = db._write_to_all_engines(write_fn)
        assert result == 10

    def test_all_secondaries_fail_returns_primary(self, logger):
        """Even if all secondaries fail, primary result is returned."""
        uris = ["postgresql://prod/db", "postgresql://dev1/db", "postgresql://dev2/db"]
        with patch.object(DBBase, "get_db_engine"):
            db = DBBase(uris, logger=logger)

        mock_engines = [MagicMock(), MagicMock(), MagicMock()]
        db._engines = mock_engines

        def write_fn(engine):
            if engine is mock_engines[0]:
                return 10
            raise ConnectionError("Secondary down")

        result = db._write_to_all_engines(write_fn)
        assert result == 10
