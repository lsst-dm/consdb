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
from datetime import datetime, timezone

from lsst.consdb.transformed_efd import failure_monitor


def _patch_now(monkeypatch, fixed_now: datetime) -> None:
    class _FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now if tz is None else fixed_now.astimezone(tz)

    monkeypatch.setattr(failure_monitor, "datetime", _FixedDateTime)


def test_day_obs_window_before_noon_utc(monkeypatch):
    _patch_now(monkeypatch, datetime(2026, 1, 2, 11, 59, tzinfo=timezone.utc))

    day_start, day_end = failure_monitor._day_obs_window(window_days=1)

    assert day_start == 20260101
    assert day_end == 20260101


def test_day_obs_window_at_or_after_noon_utc(monkeypatch):
    _patch_now(monkeypatch, datetime(2026, 1, 2, 12, 0, tzinfo=timezone.utc))

    day_start, day_end = failure_monitor._day_obs_window(window_days=2)

    assert day_start == 20260101
    assert day_end == 20260102
