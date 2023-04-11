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
import asyncio
import os
import pathlib
import unittest

import yaml

from lsst.ts import salobj
from lsst.ts_genericcamera import GenericCameraCsc, run_genericcamera
from lsst.consdb import ConsDB

STD_TIMEOUT = 15
SHORT_TIMEOUT = 5
TEST_CONFIG_DIR = pathlib.Path(__file__).parents[1].joinpath("tests", "data", "config")


class CscTestCase(salobj.BaseCscTestCase, unittest.IsolatedAsyncioTestCase):
    def make_csc(
        self,
        initial_state=salobj.State.STANDBY,
        config_dir=None,
        simulation_mode=1,
        **kwargs,
    ):
        return ConsDB(
            initial_state=initial_state,
            config_dir=config_dir,
            simulation_mode=simulation_mode,
            **kwargs,
        )

    async def asyncSetUp(self) -> None:
        self.server = self.make_csc()
        await self.server.start()

    async def asyncTearDown(self) -> None:
        await self.server.stop()

    async def test_configuration(self):
        run_genericcamera()
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=TEST_CONFIG_DIR
        ):

            cameras = self.server.get_remotes()
            self.assertGreater(0, len(cameras), "ConsDB did not attach to the camera")

            state = await self.remote.evt_summaryState.next(
                flush=False, timeout=STD_TIMEOUT
            )
            self.assertEqual(state.summaryState, salobj.State.STANDBY)

            for bad_config_name in ("no_such_file.yaml", "bad_port.yaml"):
                with self.subTest(bad_config_name=bad_config_name):
                    with salobj.assertRaisesAckError():
                        await self.remote.cmd_start.set_start(
                            configurationOverride=bad_config_name, timeout=STD_TIMEOUT
                        )

            os.environ["TEST_HOST"] = "127.0.0.1"

            self.remote.evt_summaryState.flush()

            await self.remote.cmd_start.set_start(
                configurationOverride="host_as_env.yaml", timeout=STD_TIMEOUT
            )

            state = await self.remote.evt_summaryState.next(
                flush=False, timeout=STD_TIMEOUT
            )
            self.assertEqual(state.summaryState, salobj.State.DISABLED)

            settings = await self.remote.evt_settingsAppliedTcp.aget(
                timeout=STD_TIMEOUT
            )

            self.assertEqual(settings.ip, os.environ["TEST_HOST"])

            await self.remote.cmd_standby.start(timeout=STD_TIMEOUT)

            state = await self.remote.evt_summaryState.aget(timeout=STD_TIMEOUT)
            self.assertEqual(state.summaryState, salobj.State.STANDBY)

            self.remote.evt_summaryState.flush()

            await self.remote.cmd_start.set_start(
                configurationOverride="all.yaml", timeout=STD_TIMEOUT
            )

            state = await self.remote.evt_summaryState.next(
                flush=False, timeout=STD_TIMEOUT
            )
            self.assertEqual(
                state.summaryState,
                salobj.State.DISABLED,
                f"got {salobj.State(state.summaryState)!r} expected {salobj.State.DISABLED!r}",
            )

            with open(TEST_CONFIG_DIR / "all.yaml") as fp:
                config_all = yaml.safe_load(fp)

            settings_tcp = await self.remote.evt_settingsAppliedTcp.aget(
                timeout=STD_TIMEOUT
            )

            self.assertEqual(settings_tcp.ip, config_all["host"])
            self.assertEqual(settings_tcp.port, config_all["port"])


    async def test_callback(self):
        # Need a dummy camer really to send a end of miage metadata message.

        async with self.make_csc(initial_state=salobj.State.STANDBY):
            await self.remote.cmd_start.start(timeout=STD_TIMEOUT)
            await self.remote.cmd_enable.start(timeout=STD_TIMEOUT)

if __name__ == "__main__":
    unittest.main()
