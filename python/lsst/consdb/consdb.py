# This file is part of consdb.
#
# Developed for the LSST Telescope and Site Systems.
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

__all__ = ["ConsDB", "run_consdb"]

import asyncio
import types

import yaml
from lsst.ts import salobj

from . import __version__

CONFIG_SCHEMA = yaml.safe_load(
    """
$schema: http://json-schema.org/draft-07/schema#
$id: https://github.com/lsst/consdb/blob/main/schema/ConsDB.yaml
title: ConsDB v1
Description: Schema for ConsDB configuration files
type: object
properties:
  instances:
    type: array
    description: Configuration for each trigger event
    minItem: 1
    items:
      type: object
      properties:
        trigger:
          type: string
          description: name of SAL event to trigger on
        tables:
          type: array
          description: List of ConsDB tables to update
          minItem: 1
          items:
            type: object
            properties:
              table:
                type: string
                description: ConsDB table to insert/update
              key:
                type: string
                description: Name of primary key column in ConsDB table
              columns:
                type: array
                description: List of ConsDB columns to insert/update
                minItem: 1
                items:
                  type: object
                  properties:
                    column:
                      type: string
                      description: Name of ConsDB column to insert/update
                    query:
                      type: string
                      description: EFD query to execute
                  required:
                    - column
                    - query
                  additionalProperties: false
            required:
              - table
              - columns
            additionalProperties: false
      required:
        - trigger
        - tables
      additionalProperties: false
"""
)


class ConsDB(salobj.ConfigurableCsc):
    """CSC to populate the Consolidated Database.

    Parameters
    ----------
    config_dir: `str`, optional
        Directory of configuration files (for unit testing).
    initial_state: `salobj.State`, optional
        The initial state of the CSC.  This is provided for unit testing.
    override: `str`, optional
        Configuration override file to appliy if ``initial_state`` is
        `salobj.State.DISABLED` or `salobj.State.ENABLED`.
    simulation_mode: `int` (optional)
        Simulation mode (default = 0, do not simulate).

    Raises
    ------
    ValueError
        If ``config_dir`` is not a directory or ``initial_state`` is invalid.
    salobj.ExpectedError
        If ``simulation_mode`` is invalid.
    """

    # Move to config file ?
    cameras = ['ATCamera', 'MTCamera', 'CCCamera']
    valid_simulation_modes = (0, 1)
    version = __version__
    remotes = {}  # list of remotes we listen to

    def __init__(
        self,
        config_dir: str | None = None,
        initial_state: salobj.State = salobj.State.STANDBY,
        override: str = "",
        simulation_mode: int = 0,
    ):
        super().__init__(
            "ConsDB",
            index=None,
            config_schema=CONFIG_SCHEMA,
            config_dir=config_dir,
            initial_state=initial_state,
            override=override,
            simulation_mode=simulation_mode,
        )
        self.create_callbacks()

    @classmethod
    def get_config_pkg(cls) -> str:
        return "consdb_config"

    async def configure(self, config: types.SimpleNamespace) -> None:
        pass

    async def handle_summary_state(self) -> None:
        pass

    async def end_enable(self, data):
        """Executed after state is enabled.
        So start listening and updateing the ConcsDB"""
        pass

    def get_remotes(self):
        return self.remotes

    def create_callbacks(self):
        """Get the remote(s) and set the callback function(s).
        We may be able to make this work on a single callback."""

        async with salobj.Domain() as domain:
            remote = None
            for camera in self.cameras:
                remote = salobj.Remote(domain=domain, name=camera)
                # Assume that may fail
                if remote:
                    self.remotes[camera] = remote
                    getattr(remote, 'evt_endOfImageTelemetry').callback = \
                        self.handle_callback
                else:
                    self.log.warn(f"Failed to create remote for {camera}")

    def handle_callback(self, data):
        """ One callback function can handle any/all cameras"""
        pass

    def set_cameras(self, cameras):
        """ Mainly for testing:
        cameras : [String] List of cameras"""
        self.cameras = cameras


def run_consdb() -> None:
    """Run the ConsDB CSC."""
    asyncio.run(ConsDB.amain())
