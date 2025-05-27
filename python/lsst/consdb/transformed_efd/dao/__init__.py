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

"""Provides tools for interacting with the database access objects (DAOs).

Submodules include:
    - base: Defines the foundational DAO components such as database engine management
        and query execution.
    - butler: Provides data access methods for querying dimensions using a Butler object.
    - exposure_efd: Handles operations related to the "exposure_efd" table.
    - exposure_efd_unpivoted: Manages data for the "exposure_efd_unpivoted" table.
    - influxdb: Interfaces with the InfluxDB API for time-series data queries.
    - transformd: Manages transformed EFD scheduler data.
    - visit_efd: Handles data operations for the "visit1_efd" table.
    - visit_efd_unpivoted: Accesses data for the "visit1_efd_unpivoted" table.

These modules collectively facilitate database operations, data transformation, and
efficient retrieval of time-series and structured data.
"""
