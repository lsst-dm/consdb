from typing import Optional, Union

import numpy as np
import pandas as pd
from astropy.time import Time


class Summary:
    """
    Class to summarize and analyze numeric time-series data with a DatetimeIndex.

    Attributes:
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
        """
        Initializes the Summary class with a pandas DataFrame.

        Args:
            dataframe (pd.DataFrame): A DataFrame with a DatetimeIndex and numeric or boolean data.
            exposure_start (Time): Start of the exposure period as an astropy.time.Time object.
            exposure_end (Time): End of the exposure period as an astropy.time.Time object.
            datatype (Optional[str]): Desired NumPy dtype for the data conversion.

        Raises:
            ValueError: If the DataFrame index is not a DatetimeIndex or contains invalid data types.
            ValueError: If exposure times are invalid or not compatible with the DataFrame index.
        """
        if not isinstance(dataframe.index, pd.DatetimeIndex):
            raise ValueError("The DataFrame index must be a DatetimeIndex.")

        if not isinstance(exposure_start, Time) or not isinstance(exposure_end, Time):
            raise ValueError("Exposure times must be astropy.time.Time objects.")
        if exposure_start >= exposure_end:
            raise ValueError("Exposure start time must be earlier than exposure end time.")

        df_time = Time(dataframe.index.to_pydatetime())
        if exposure_start > df_time[-1] or exposure_end < df_time[0]:
            raise ValueError("The DataFrame index must encompass the exposure time range.")

        dataframe = dataframe.dropna().convert_dtypes()
        if not all(
            pd.api.types.is_numeric_dtype(dtype) or pd.api.types.is_bool_dtype(dtype)
            for dtype in dataframe.dtypes
        ):
            raise ValueError("All columns in the DataFrame must be numeric or boolean.")

        self.data_array = dataframe.to_numpy(dtype=datatype) if datatype else dataframe.to_numpy()
        self.timestamps = dataframe.index
        self.exposure_start = exposure_start
        self.exposure_end = exposure_end

    def _get_numeric_values(self) -> np.ndarray:
        """Helper method to flatten and ensure numeric values."""
        return self.data_array.astype(np.float64).flatten()

    def mean(self) -> float:
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
            x = (
                self.timestamps.values.astype("datetime64[ns]").astype(float)
                if fit_basis == "time"
                else np.arange(len(self.timestamps))
            )
            x -= x[0]  # Normalize time
            y = self.data_array
            if len(x) <= degree:
                return np.nan

            coeffs = np.polyfit(x, y, degree)
            residuals = y - np.polyval(coeffs, x)
            return np.sqrt(np.mean(residuals**2))
        except Exception as e:
            raise ValueError(f"RMS calculation failed: {e}")

    def most_recent_value_in_last_minute(self) -> Optional[Union[float, int, bool]]:
        """
        Find the most recent value within the last minute of the exposure_end.

        Returns:
            Optional[Union[float, int, bool]]: The most recent value in the last minute or None if not found.
        """
        try:
            # Convert exposure_end (astropy Time) to pandas Timestamp
            end_time = pd.Timestamp(self.exposure_end.iso)
            last_minute = end_time - pd.Timedelta(minutes=1)

            # Filter timestamps and find the most recent value
            mask = (self.timestamps >= last_minute) & (self.timestamps <= end_time)
            recent_values = self.data_array[mask]
            return recent_values[-1] if len(recent_values) > 0 else None
        except Exception as e:
            raise ValueError(f"Error finding recent value: {e}")

    def apply(self, method_name: str, **kwargs) -> Optional[float]:
        """
        Apply a transformation method specified by method_name.

        Args:
            method_name: Name of the method to apply.
            **kwargs: Additional keyword arguments.

        Returns:
            Result of the transformation method or None if the method is not callable.
        """
        if self.data_array.size == 0 or np.all(np.isnan(self._get_numeric_values())):
            return None

        method = getattr(self, method_name, None)
        if callable(method):
            try:
                return method(**kwargs)
            except Exception as e:
                raise ValueError(f"Error in method '{method_name}': {e}")
        raise AttributeError(f"Method '{method_name}' not found.")

    def __repr__(self):
        """
        Provide a string representation of the Summary object.

        Returns:
            str: A concise summary of key attributes.
        """
        return (
            f"Summary("
            f"data_shape={self.data_array.shape}, "
            f"time_range=({self.timestamps.min()}, {self.timestamps.max()}), "
            f"exposure_range=({self.exposure_start.isot}, {self.exposure_end.isot}))"
        )
