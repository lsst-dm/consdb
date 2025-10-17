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
"""Provides the `Summary` class to perform the EDF transformations."""
from typing import Optional, Union

import numpy as np
import pandas as pd
from astropy.time import Time


class Summary:
    """Class to summarize numeric time-series data with a DatetimeIndex.
    Attributes
    ----------
        data_array (np.ndarray): The numeric values of the DataFrame.
        timestamps (pd.DatetimeIndex): The time index of the DataFrame.
        exposure_start (Time): The start of the exposure period.
        exposure_end (Time): The end of the exposure period.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        exposure_start: Time,
        exposure_end: Time,
        datatype: Optional[str] = None,
    ):
        """Initialize Summary class with a pandas DataFrame.
        Args:
        ----
            dataframe (pd.DataFrame): A DataFrame with a DatetimeIndex
                and numeric or boolean data.
            exposure_start (Time): Start of the exposure period as an
                astropy.time.Time object.
            exposure_end (Time): End of the exposure period as an
                astropy.time.Time object.
            datatype (Optional[str]): Desired NumPy dtype for the data
                conversion.
        Raises:
        ------
            ValueError: If the DataFrame index is not a DatetimeIndex or
                contains invalid data types.
            ValueError: If exposure times are invalid or not compatible
                with the DataFrame index.
        """
        if not isinstance(dataframe.index, pd.DatetimeIndex):
            raise ValueError("The DataFrame index must be a DatetimeIndex.")
        if len(dataframe) == 0:
            raise ValueError("The DataFrame must not be empty.")
        if not isinstance(exposure_start, Time) or not isinstance(exposure_end, Time):
            raise ValueError("Exposure times must be astropy.time.Time objects.")
        if exposure_start >= exposure_end:
            raise ValueError("Exposure start time must be earlier than exposure end time.")

        self._raw_dataframe: Optional[pd.DataFrame] = dataframe
        self._datatype = datatype
        self.exposure_start = exposure_start
        self.exposure_end = exposure_end

        self._data_array: Optional[np.ndarray] = None
        self._timestamps: Optional[pd.DatetimeIndex] = None
        self._flat_numeric_values: Optional[np.ndarray] = None
        self._numeric_timestamps: Optional[np.ndarray] = None
        self._time_indices: Optional[np.ndarray] = None
        self._is_all_nan: Optional[bool] = None

    def _process_dataframe(self):
        """Lazily process the raw dataframe into the final array and index."""
        if self._data_array is not None:
            return

        df = self._raw_dataframe.dropna().convert_dtypes()
        if not all(
            pd.api.types.is_numeric_dtype(dtype) or pd.api.types.is_bool_dtype(dtype) for dtype in df.dtypes
        ):
            raise ValueError("All columns in the DataFrame must be numeric or boolean.")

        self._data_array = df.to_numpy(dtype=self._datatype) if self._datatype else df.to_numpy()
        self._timestamps = df.index
        self._raw_dataframe = None

    @property
    def data_array(self) -> np.ndarray:
        if self._data_array is None:
            self._process_dataframe()
        return self._data_array

    @property
    def timestamps(self) -> pd.DatetimeIndex:
        if self._timestamps is None:
            self._process_dataframe()
        return self._timestamps

    def _get_numeric_values(self) -> np.ndarray:
        """Flatten and ensure numeric values. Result cached for performance."""
        if self._flat_numeric_values is None:
            self._flat_numeric_values = self.data_array.astype(np.float64).flatten()
        return self._flat_numeric_values

    def mean(self, pre_aggregate_interval=None) -> float:
        """Calculate the mean ignoring NaN values."""
        return np.nanmean(self._get_numeric_values())

    def stddev(self, ddof: int = 1) -> Optional[float]:
        """Calculate the standard deviation ignoring NaN values."""
        values = self._get_numeric_values()
        if np.count_nonzero(~np.isnan(values)) > 1:
            return np.nanstd(values, ddof=ddof)
        return None

    def max(self) -> Union[float, int, bool]:
        """Find the maximum value ignoring NaN values."""
        return np.nanmax(self._get_numeric_values())

    def min(self) -> Union[float, int, bool]:
        """Find the minimum value ignoring NaN values."""
        return np.nanmin(self._get_numeric_values())

    def rms_from_polynomial_fit(self, degree=1, fit_basis="index") -> Optional[float]:
        """Calculate RMS after fitting a polynomial."""
        try:
            if fit_basis == "time":
                if self._numeric_timestamps is None:
                    ts = self.timestamps.values.astype(np.float64)
                    ts -= ts[0]
                    self._numeric_timestamps = ts
                x = self._numeric_timestamps
            else:
                if self._time_indices is None:
                    self._time_indices = np.arange(len(self.timestamps))
                x = self._time_indices

            y = self.data_array
            if len(x) <= degree:
                return np.nan

            coeffs = np.polyfit(x, y, degree)
            residuals = y - np.polyval(coeffs, x)
            return np.sqrt(np.mean(residuals**2))
        except Exception as e:
            raise ValueError(f"RMS calculation failed: error={e}")

    def most_recent_value(self, start_offset: Union[float, int] = 0) -> Optional[Union[float, int, bool]]:
        """Return the most‐recent scalar."""
        try:
            if self._data_array is None and self._raw_dataframe is not None:
                if self._raw_dataframe.empty:
                    return None
                return self._raw_dataframe.iloc[-1, 0]
            return self.data_array[-1, 0]
        except Exception as e:
            raise ValueError(f"Error finding recent value: error={e}")

    def apply(self, method_name: str, **kwargs) -> Optional[float]:
        """Apply a transformation method specified by method_name.
        Args:
        ----
            method_name: Name of the method to apply.
            **kwargs: Additional keyword arguments.
        Returns:
        -------
            Result of the transformation method or None if the method is not
                callable.
        """
        if self.data_array.size == 0:
            return None

        if self._is_all_nan is None:
            self._is_all_nan = np.all(np.isnan(self._get_numeric_values()))
        if self._is_all_nan:
            return None

        method = getattr(self, method_name, None)
        if callable(method):
            try:
                return method(**kwargs)
            except Exception as e:
                raise ValueError(f"Error in method: method={method_name} error={e}")
        raise AttributeError(f"Method not found: method={method_name}")

    def __repr__(self):
        """Provide a string representation of the Summary object.
        Returns
        -------
            str: A concise summary of key attributes.
        """
        try:
            # Trigger processing to get accurate shape and time range for repr
            data_shape = self.data_array.shape
            time_range = (self.timestamps.min(), self.timestamps.max())
        except ValueError:
            data_shape = "N/A (processing failed)"
            time_range = ("N/A", "N/A")

        return (
            f"Summary("
            f"data_shape={data_shape}, "
            f"time_range=({time_range[0]}, {time_range[1]}), "
            f"exposure_range=({self.exposure_start.isot}, {self.exposure_end.isot}))"
        )
