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
import pytest
from lsst.consdb.transformed_efd.config_model import (
    Column,
    Field,
    Topic,
)
from pydantic import ValidationError


def test_column_invalid_unpivoted_tables():
    with pytest.raises(ValidationError) as exc_info:
        Column(
            name="invalid_column",
            tables=["exposure_efd"],
            store_unpivoted=True,
            function="avg",
            datatype="float",
            description="Invalid test column",
            packed_series=False,
            topics=[Topic(name="TestTopic", fields=[Field(name="TestField")])],
        )
    assert "Invalid tables provided" in str(exc_info.value)


def test_column_end_reference():
    column_kwargs = {
        "name": "hexapod_u",
        "function": "most_recent_value",
        "datatype": "float",
        "description": "Test end_reference",
        "packed_series": False,
        "topics": [Topic(name="TestTopic", fields=[Field(name="u")])],
    }

    assert Column(**column_kwargs).end_reference == "end"
    assert Column(**column_kwargs, end_reference="start").model_dump()["end_reference"] == "start"

    with pytest.raises(ValidationError):
        Column(**column_kwargs, end_reference="effective_start")
