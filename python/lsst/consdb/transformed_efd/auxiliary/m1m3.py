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
"""M1M3 glass thermocouple map owned by consdb.

Do not import ``lsst.ts.xml`` at runtime. See ``GLASS_THERMOCOUPLES``
for how to rebuild the snapshot when the hardware map changes.
"""

import re

# GEC tel_temperature packing (ts_ess_common GecThermalscannerDataClient):
#   https://github.com/lsst-ts/ts_ess_common/blob/develop/python/lsst/ts/ess/common/data_client/gec_thermalscanner_data_client.py
# Two independent axes:
#   - scanner: physical box, salIndex 114–117 (TS_01–TS_04)
#   - topic n/6: one EFD message of 16 temperatureItems from that scanner
# sensorName is "{scanner} n/6" with n = 1..6 (the client uses tn + 1).
# Elana Urbach, 2026-08-27: 1/6 → hardware channels 0–15; 2/6 → 16–31; …
# Each scanner has one cold junction: hardware channel 0 = 1/6 item 0.
# Item 0 of 2/6–6/6 is channel 16, 32, … (not a cold junction).
# With n taken from sensorName (1-based): channel = 16 * (n - 1) + item_idx
# ts_eas GlassTemperatureModel uses 16 * n + i with the same n, so 1/6
# becomes channels 16–31 there. Do not change this to match ts_eas.
_SENSOR_NAME_RE = re.compile(r"m1m3-ts-\d+ (\d+)/\d+")
_TEMPERATURE_ITEM_RE = re.compile(r"^temperatureItem(\d+)$")
_CHANNELS_PER_SEQUENCE = 16

# Snapshot of lsst.ts.xml.tables.m1m3.ThermocoupleTable.
# Each entry is (salIndex, channel). Scanner.TS_01..TS_04 = 114..117.
# Channel 0 is the cold junction and is not in the table.
# To rebuild after a ts.xml hardware-map change (do not add this import
# to runtime code):
#   from lsst.ts.xml.tables.m1m3 import ThermocoupleTable
#   sorted((int(tc.scanner), int(tc.channel)) for tc in ThermocoupleTable)
# This replaces find_thermocouple(scanner, channel) is not None.
GLASS_THERMOCOUPLES = frozenset(
    {
        (114, 1),
        (114, 2),
        (114, 3),
        (114, 4),
        (114, 5),
        (114, 7),
        (114, 8),
        (114, 9),
        (114, 10),
        (114, 13),
        (114, 14),
        (114, 15),
        (114, 16),
        (114, 17),
        (114, 18),
        (114, 19),
        (114, 20),
        (114, 21),
        (114, 22),
        (114, 24),
        (114, 25),
        (114, 26),
        (114, 27),
        (114, 28),
        (114, 29),
        (114, 31),
        (114, 33),
        (114, 34),
        (114, 35),
        (114, 36),
        (114, 37),
        (114, 38),
        (114, 39),
        (114, 40),
        (114, 43),
        (114, 44),
        (114, 45),
        (115, 1),
        (115, 2),
        (115, 5),
        (115, 6),
        (115, 7),
        (115, 8),
        (115, 9),
        (115, 10),
        (115, 11),
        (115, 12),
        (115, 13),
        (115, 14),
        (115, 15),
        (115, 16),
        (115, 17),
        (115, 19),
        (115, 20),
        (115, 21),
        (115, 22),
        (115, 24),
        (115, 25),
        (115, 27),
        (115, 29),
        (115, 30),
        (115, 31),
        (115, 32),
        (115, 34),
        (115, 35),
        (115, 36),
        (115, 37),
        (115, 38),
        (115, 39),
        (115, 40),
        (115, 41),
        (115, 42),
        (115, 43),
        (116, 2),
        (116, 3),
        (116, 4),
        (116, 5),
        (116, 6),
        (116, 7),
        (116, 8),
        (116, 9),
        (116, 10),
        (116, 11),
        (116, 12),
        (116, 13),
        (116, 14),
        (116, 15),
        (116, 17),
        (116, 18),
        (116, 19),
        (116, 20),
        (116, 21),
        (116, 22),
        (116, 23),
        (116, 24),
        (116, 25),
        (116, 26),
        (116, 28),
        (116, 30),
        (116, 31),
        (116, 32),
        (116, 33),
        (116, 37),
        (116, 38),
        (116, 39),
        (116, 40),
        (116, 41),
        (116, 42),
        (116, 43),
        (116, 45),
        (117, 1),
        (117, 2),
        (117, 3),
        (117, 4),
        (117, 5),
        (117, 6),
        (117, 7),
        (117, 8),
        (117, 9),
        (117, 10),
        (117, 11),
        (117, 13),
        (117, 14),
        (117, 15),
        (117, 16),
        (117, 17),
        (117, 18),
        (117, 19),
        (117, 20),
        (117, 21),
        (117, 22),
        (117, 23),
        (117, 24),
        (117, 25),
        (117, 26),
        (117, 27),
        (117, 28),
        (117, 29),
        (117, 30),
        (117, 31),
        (117, 32),
        (117, 33),
        (117, 36),
        (117, 37),
        (117, 38),
        (117, 39),
    }
)


def is_glass_thermocouple(sal_index: int, channel: int) -> bool:
    """Return True if ``(sal_index, channel)`` is a glass thermocouple."""
    return (sal_index, channel) in GLASS_THERMOCOUPLES


def sequence_number(sensor_name: str) -> int | None:
    """Return the 1-based topic index n from ``sensorName``, or None.

    Example: ``m1m3-ts-04 1/6`` → 1.
    """
    match = _SENSOR_NAME_RE.match(sensor_name)
    if match is None:
        return None
    return int(match.group(1))


def temperature_item_index(column_name: str) -> int | None:
    """Return the item index from a ``temperatureItemN`` column name.

    Returns ``None`` when the name is not a packed GEC temperature item,
    so extra numeric fields cannot shift the channel mapping.
    """
    match = _TEMPERATURE_ITEM_RE.match(column_name)
    if match is None:
        return None
    return int(match.group(1))


def item_channel(sequence_num: int, item_idx: int) -> int:
    """Return the hardware channel for topic index n and temperatureItem i.

    ``1/6`` maps to channels 0–15, ``2/6`` to 16–31 (Elana Urbach,
    2026-08-27). Cold junction is channel 0 (``1/6`` item 0) only.
    ``n`` is 1-based from ``sensorName``. ts_eas
    ``GlassTemperatureModel`` uses ``16 * n + i`` and is one topic ahead;
    do not change this to match ts_eas.
    """
    return _CHANNELS_PER_SEQUENCE * (sequence_num - 1) + item_idx
