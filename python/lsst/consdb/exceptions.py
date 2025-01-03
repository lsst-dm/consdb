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

from typing import Any


class BadValueException(Exception):
    """Exception raised for an invalid value.

    Reports the bad value and, if available, a list of valid values.

    Parameters
    ----------
    kind: `str`
        Kind of value that failed to validate.
    value: `Any`
        The invalid value.
    valid: `list` [ `Any` ], optional
        List of valid values.
    """

    status_code = 404

    def __init__(self, kind: str, value: Any, valid: list[Any] | None = None):
        self.kind = kind
        self.value = value
        self.valid = valid

    def to_dict(self) -> dict[str, Any]:
        """Convert the exception to a dictionary for JSON conversion.

        Returns
        -------
        json_dict: `dict` [ `str`, `Any` ]
            Dictionary with a message, value, and, if available, list of
            valid values.
        """
        data = {
            "message": f"Unknown {self.kind}",
            "value": self.value,
        }
        if self.valid:
            data["valid"] = self.valid
        return data


class UnknownInstrumentException(Exception):
    """Exception raised for an unknown instrument.

    Parameters
    ----------
    instrument: `str`
        Name of the unknown instrument.
    """

    status_code = 404

    def __init__(self, instrument: str):
        self.instrument = instrument

    def to_dict(self) -> dict[str, Any]:
        """Convert the exception to a dictionary for JSON conversion.

        Returns
        -------
        json_dict: `dict` [ `str`, `Any` ]
            Dictionary with a message and the unknown instrument name.
        """
        return {
            "message": "Unknown instrument",
            "value": self.instrument,
        }
