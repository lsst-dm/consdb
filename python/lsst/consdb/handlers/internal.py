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

from fastapi import APIRouter
from safir.metadata import get_metadata

from ..cdb_schema import AllowedFlexTypeEnum, ObsTypeEnum
from ..config import config
from ..models import IndexResponseModel

internal_router = APIRouter()
"""FastAPI router for all internal handlers."""


@internal_router.get(
    "/",
    description="Metadata and health check endpoint.",
    include_in_schema=False,
    summary="Application metadata",
)
def internal_root() -> IndexResponseModel:
    """Root URL for liveness checks.

    Returns
    -------
    json_dict: `dict` [ `str`, `Any` ]
        JSON response with a list of instruments, observation types, and
        data types.
    """
    global instrument_tables

    metadata = get_metadata(
        package_name="consdb",
        application_name=config.name,
    )

    return IndexResponseModel.parse_obj(
        {
            **metadata.dict(),
            "instruments": instrument_tables.instrument_list,
            "obs_types": [o.value for o in ObsTypeEnum],
            "dtypes": [d.value for d in AllowedFlexTypeEnum],
        }
    )
