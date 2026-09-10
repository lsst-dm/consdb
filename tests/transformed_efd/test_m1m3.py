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
from lsst.consdb.transformed_efd.auxiliary.m1m3 import (
    GLASS_THERMOCOUPLES,
    is_glass_thermocouple,
    item_channel,
    sequence_number,
    temperature_item_index,
)


def test_glass_thermocouple_snapshot():
    assert len(GLASS_THERMOCOUPLES) == 146
    assert is_glass_thermocouple(114, 1)
    assert is_glass_thermocouple(117, 16)
    assert not is_glass_thermocouple(114, 0)
    assert not is_glass_thermocouple(114, 6)


def test_sequence_number():
    assert sequence_number("m1m3-ts-04 1/6") == 1
    assert sequence_number("m1m3-ts-04 2/6") == 2
    assert sequence_number("not-a-valid-m1m3-sensor") is None


def test_item_channel_matches_gec_packing():
    # 1/6 → 0–15 (0 = cold junction); 2/6 → 16–31.
    assert item_channel(1, 0) == 0
    assert item_channel(1, 15) == 15
    assert item_channel(2, 0) == 16
    assert item_channel(2, 15) == 31


def test_temperature_item_index():
    assert temperature_item_index("temperatureItem0") == 0
    assert temperature_item_index("temperatureItem15") == 15
    assert temperature_item_index("pressure") is None
    assert temperature_item_index("temperatureItem") is None
