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
"""Provides the `Summary` class to perform the EFD transformations."""

import numpy as np
import pandas as pd
from astropy.time import Time
from lsst.consdb.transformed_efd.auxiliary.m1m3 import (
    is_glass_thermocouple,
    item_channel,
    sequence_number,
)

# Never fold these into data_array (even when numeric / string-encoded ints).
# salIndex was polluting bulk stats and disabling glass-thermocouple filtering.
_METADATA_COLUMNS = frozenset({"salIndex", "sensorName"})


class Summary:
    """Class to summarize numeric time-series data with a DatetimeIndex.
    Attributes
    ----------
        data_array (np.ndarray): The numeric values of the DataFrame.
        timestamps (pd.DatetimeIndex): The time index of the DataFrame.
        exposure_start (Time): The start of the exposure period.
        exposure_end (Time): The end of the exposure period.
        metadata (pd.DataFrame | None): Non-numeric columns preserved for
            custom transformation functions (e.g. ``sensorName``,
            ``salIndex``).
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        exposure_start: Time,
        exposure_end: Time,
        datatype: str | None = None,
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
            TypeError: If the DataFrame index is not a DatetimeIndex or
                contains invalid data types.
            ValueError: If exposure times are invalid or not compatible
                with the DataFrame index.
        """
        if not isinstance(dataframe.index, pd.DatetimeIndex):
            raise TypeError("The DataFrame index must be a DatetimeIndex.")
        if len(dataframe) == 0:
            raise ValueError("The DataFrame must not be empty.")
        if not isinstance(exposure_start, Time) or not isinstance(exposure_end, Time):
            raise TypeError("Exposure times must be astropy.time.Time objects.")
        if exposure_start >= exposure_end:
            raise ValueError("Exposure start time must be earlier than exposure end time.")

        self._raw_dataframe: pd.DataFrame | None = dataframe
        self._datatype = datatype
        self.exposure_start = exposure_start
        self.exposure_end = exposure_end

        self._data_array: np.ndarray | None = None
        self._timestamps: pd.DatetimeIndex | None = None
        self._metadata: pd.DataFrame | None = None
        self._flat_numeric_values: np.ndarray | None = None
        self._numeric_timestamps: np.ndarray | None = None
        self._time_indices: np.ndarray | None = None
        self._is_all_nan: bool | None = None

    def _process_dataframe(self):
        """Lazily process the raw dataframe into the final array and index.

        Numeric and boolean columns go to ``_data_array``; non-numeric
        columns are preserved in ``_metadata`` for custom transformation
        functions.  ``dropna`` is not called — individual functions skip
        NaN via ``np.nanmean`` / ``np.nanmedian``.
        """
        if self._data_array is not None:
            return

        df = self._raw_dataframe.convert_dtypes()

        numeric_cols = [
            col
            for col in df.columns
            if col not in _METADATA_COLUMNS
            and (pd.api.types.is_numeric_dtype(df[col].dtype) or pd.api.types.is_bool_dtype(df[col].dtype))
        ]
        non_numeric_cols = [col for col in df.columns if col not in numeric_cols]

        # EFD / pandas may return telemetry as object (e.g. all-null or
        # string-encoded numbers). Coerce lossless or all-null columns to
        # numeric so statistics still run; leave true strings as metadata.
        # Never coerce known metadata ids (salIndex, sensorName) into values.
        if non_numeric_cols:
            for col in list(non_numeric_cols):
                if col in _METADATA_COLUMNS:
                    continue
                coerced = pd.to_numeric(df[col], errors="coerce")
                original_non_null = int(df[col].notna().sum())
                if original_non_null == 0 or int(coerced.notna().sum()) == original_non_null:
                    df[col] = coerced
            numeric_cols = [
                col
                for col in df.columns
                if col not in _METADATA_COLUMNS
                and (
                    pd.api.types.is_numeric_dtype(df[col].dtype) or pd.api.types.is_bool_dtype(df[col].dtype)
                )
            ]
            non_numeric_cols = [col for col in df.columns if col not in numeric_cols]

        if not numeric_cols:
            raise ValueError("The DataFrame must contain at least one numeric or boolean column.")

        self._data_array = (
            df[numeric_cols].to_numpy(dtype=self._datatype, na_value=np.nan)
            if self._datatype
            else df[numeric_cols].to_numpy(dtype=np.float64, na_value=np.nan)
        )
        self._timestamps = df.index

        if non_numeric_cols:
            self._metadata = df[non_numeric_cols]

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

    @property
    def metadata(self) -> pd.DataFrame | None:
        """Non-numeric metadata columns preserved from the raw DataFrame.

        Only populated when the config lists non-numeric fields
        (e.g. ``salIndex``, ``sensorName``) alongside the numeric
        telemetry fields.  ``None`` otherwise.
        """
        if self._data_array is None:
            self._process_dataframe()
        return self._metadata

    def _get_numeric_values(self) -> np.ndarray:
        """Flatten and ensure numeric values. Result cached for performance."""
        if self._flat_numeric_values is None:
            self._flat_numeric_values = self.data_array.astype(np.float64).flatten()
        return self._flat_numeric_values

    def mean(self, pre_aggregate_interval=None) -> float:
        """Calculate the mean ignoring NaN values."""
        return np.nanmean(self._get_numeric_values())

    def median(self) -> float:
        """Calculate the median ignoring NaN values."""
        return np.nanmedian(self._get_numeric_values())

    # ------------------------------------------------------------------
    # M1M3 bulk glass temperature (DM-55710)
    # ------------------------------------------------------------------

    def m1m3_bulk_temperature_median(self, **kwargs) -> float | None:
        """Median bulk temperature of M1M3 glass thermocouples.

        Row filtering (scanners) is handled by ``subset_field`` /
        ``subset_value`` in the config.  Uses ``sensorName`` from
        metadata and ``is_glass_thermocouple`` to exclude cold-junction
        and unmapped channels.

        Returns
        -------
        float | None
            Median temperature in °C, or ``None`` if no valid
            thermocouple readings are found.
        """
        valid = self._m1m3_bulk_temperatures()
        if not valid:
            return None
        return float(np.median(valid))

    def m1m3_bulk_temperature_mean(self, **kwargs) -> float | None:
        """Mean bulk temperature of M1M3 glass thermocouples.

        Same filtering as ``m1m3_bulk_temperature_median``.

        Returns
        -------
        float | None
            Mean temperature in °C, or ``None`` if no valid thermocouple
            readings are found.
        """
        valid = self._m1m3_bulk_temperatures()
        if not valid:
            return None
        return float(np.mean(valid))

    def _m1m3_bulk_temperatures(self) -> list[float]:
        """Return valid M1M3 thermocouple temperatures from the timespan."""
        # Trigger lazy processing before reading _metadata
        # (same as data_array).
        data = self.data_array
        if self._metadata is None or "sensorName" not in self._metadata.columns:
            return []

        sensor_names = self._metadata["sensorName"].values
        has_sal = "salIndex" in self._metadata.columns
        sal_indices = self._metadata["salIndex"].values if has_sal else None

        valid_temperatures: list[float] = []

        for row_idx in range(len(data)):
            sensor_name = str(sensor_names[row_idx])
            sequence_num = sequence_number(sensor_name)
            if sequence_num is None:
                continue

            sal_idx = None
            if has_sal and sal_indices is not None:
                try:
                    sal_idx = int(str(sal_indices[row_idx]))
                except (ValueError, TypeError):
                    pass

            if sal_idx is None:
                continue

            for item_idx in range(data.shape[1]):
                temp = data[row_idx, item_idx]
                if np.isnan(temp):
                    continue

                channel = item_channel(sequence_num, item_idx)
                if not is_glass_thermocouple(sal_idx, channel):
                    continue  # cold junction or unmapped channel

                valid_temperatures.append(float(temp))

        return valid_temperatures

    # ------------------------------------------------------------------

    def stddev(self, ddof: int = 1) -> float | None:
        """Calculate the standard deviation ignoring NaN values."""
        values = self._get_numeric_values()
        if np.count_nonzero(~np.isnan(values)) > 1:
            return np.nanstd(values, ddof=ddof)
        return None

    def max(self) -> float | int | bool:
        """Find the maximum value ignoring NaN values."""
        return np.nanmax(self._get_numeric_values())

    def min(self) -> float | int | bool:
        """Find the minimum value ignoring NaN values."""
        return np.nanmin(self._get_numeric_values())

    def rms_from_polynomial_fit(self, degree=1, fit_basis="index") -> float | None:
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

    def most_recent_value(self, start_offset: float = 0) -> float | int | bool | None:
        """Return the most‐recent scalar."""
        try:
            if self._data_array is None and self._raw_dataframe is not None:
                if self._raw_dataframe.empty:
                    return None
                return self._raw_dataframe.iloc[-1, 0]
            return self.data_array[-1, 0]
        except Exception as e:
            raise ValueError(f"Error finding recent value: error={e}")

    def apply(self, method_name: str, **kwargs) -> float | None:
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
