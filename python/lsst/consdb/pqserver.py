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

# The main application factory for consdb.pqserver.

from fastapi import FastAPI
from safir.middleware.x_forwarded import XForwardedMiddleware

from .config import config
from .handlers.external import external_router
from .handlers.internal import internal_router

__all__ = ["app", "config"]

app = FastAPI(
    title="consdb-pqserver",
    description="HTTP API for consdb",
    openapi_url=f"{config.url_prefix}/openapi.json",
    docs_url=f"{config.url_prefix}/docs",
    redoc_url=f"{config.url_prefix}/redoc",
)
"""The main FastAPI application for consdb.pqserver."""

# Attach the routers.
app.include_router(internal_router)
app.include_router(external_router, prefix=config.url_prefix)

# Add the middleware
app.add_middleware(XForwardedMiddleware)
