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
import pathlib
import unittest


from lsst.ts import salobj
from lsst.ts.genericcamera import GenericCameraCsc
from lsst.consdb import ConsDB, MockCamera


STD_TIMEOUT = 15
SHORT_TIMEOUT = 5
TEST_CONFIG_DIR = pathlib.Path(__file__).parents[1].\
    joinpath("tests", "data", "config")


class CscTestCase(salobj.BaseCscTestCase, unittest.IsolatedAsyncioTestCase):

    the_csc = None
    def make_csc(
        self,
        initial_state=salobj.State.STANDBY,
        config_dir=TEST_CONFIG_DIR,
        simulation_mode=1,
        **kwargs,
    ):
        print("Called  make csc")
        CscTestCase.the_csc = ConsDB(
            initial_state=initial_state,
            config_dir=config_dir,
            simulation_mode=simulation_mode,
            **kwargs,
        )
        return CscTestCase.the_csc

    def basic_make_csc(self, initial_state, config_dir, simulation_mode,
                       override):
        print("Called basic make csc")
        assert simulation_mode == 0
        CscTestCase.the_csc =  ConsDB(
            initial_state=initial_state,
            config_dir=config_dir,
            override=override,
        )
        return CscTestCase.the_csc

    async def asyncTearDown(self) -> None:
        pass

    async def test_bin_script(self):
        """Test that run_atdometrajectory runs the CSC."""
        await self.check_bin_script(
            name="ConsDB",
            index=None,
            exe_name="run_consdb",
        )

    async def test_configuration(self):
        #mcamera = MockCamera(initial_state=salobj.State.ENABLED)
        mcamera = GenericCamera(initial_state=salobj.State.ENABLED)
        ConsDB.set_cameras([mcamera.name])
        async with self.make_csc(
            initial_state=salobj.State.STANDBY, config_dir=TEST_CONFIG_DIR
        ):

            cameras = CscTestCase.the_csc.get_remotes()
            self.assertGreater(0, len(cameras), "ConsDB did not attach to the camera")

    async def test_callback(self):
        # Need a dummy camera really to send an end of image metadata message.
        async with self.make_csc(initial_state=salobj.State.STANDBY):
            await CscTestCase.the_csc.disabled_or_enabled()
        self .assertTrue(CscTestCase.the_csc.summary_state() == salobj.State.ENABLED,
                         "CSC is not enabled")
        self.assertTrue(False, "Fail for good measure")


if __name__ == "__main__":
    unittest.main()
