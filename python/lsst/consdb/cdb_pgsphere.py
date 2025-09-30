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

from sqlalchemy import Column, MetaData, cast
from sqlalchemy.dialects.postgresql import base as pg_base
from sqlalchemy.types import UserDefinedType


class SPoly(UserDefinedType):
    """A bare-bones class representing the pgSphere SPOLY type."""
    cache_ok = True

    def get_col_spec(self, **kw):
        return "SPOLY"

    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)

    def column_expression(self, col):
        return col


pg_base.ischema_names.setdefault("spoly", SPoly)


def add_shadow_column(metadata: MetaData) -> None:
    """Find tables with the s_region column, and add a pgs_region column.

    Parameters
    ----------
    metadata : `~sqlalchemy.MetaData`
        The schema metadata to alter. All the tables in the schema
        will be searched for an `s_region` column, and the tables
        will be modified in place.
    """
    for table_name, table in metadata.tables.items():
        if "s_region" in table.columns:
            table.append_column(Column(
                "pgs_region",
                SPoly(),
                nullable=True,
                comment="Spherical region type spoly corresponding to s_region.",
            ))
