from typing import Optional, Union

import numpy
import pandas


class Summary:
    """Class to summarize and analyze numeric data, handling NaN values and
    key-based filtering.
    """

    def __init__(
        self,
        dataframe: pandas.DataFrame,
        datatype: Optional[str] = None,
    ):
        """
        Initialize Summary with a DataFrame of numeric and boolean values.
        NaN/NA values are handled by dropping rows containing any missing 
        values.
        """
        # Ensure the DataFrame index is a DatetimeIndex
        if not isinstance(dataframe.index, pandas.DatetimeIndex):
            raise ValueError("The DataFrame index must be a DatetimeIndex.")

        # Handle invalid values (NaN, pandas.NA) by dropping rows with
        # any NaN or pandas.NA values
        dataframe = dataframe.dropna()

        # Infer object types if any, and handle nullable dtypes
        dataframe = dataframe.convert_dtypes()

        # Convert the DataFrame to a NumPy array, allowing NumPy to infer
        # datatype if None is passed
        self.values = dataframe.to_numpy(dtype=datatype) if datatype else dataframe.to_numpy()
        self.time = dataframe.index

    def mean(self, **kwargs) -> float:
        """Calculate the mean ignoring NaN values."""
        values = self.values.astype(numpy.float64).flatten()
        return numpy.nanmean(values)

    def stddev(self, ddof: int = 1, **kwargs) -> float:
        """Calculate the standard deviation ignoring NaN values."""
        values = self.values.astype(numpy.float64).flatten()
        if numpy.count_nonzero(~numpy.isnan(values)) > 1:
            return numpy.nanstd(values, ddof=ddof)
        return None

    def max(self, **kwargs) -> Union[float, int, bool]:
        """Find the maximum value ignoring NaN values."""
        values = self.values.astype(numpy.float64).flatten()
        return numpy.nanmax(values)

    def min(self, **kwargs) -> Union[float, int, bool]:
        """Find the minimum value ignoring NaN values."""
        values = self.values.astype(numpy.float64).flatten()
        return numpy.nanmin(values)

    def rms_from_polynomial_fit(self, degree=1, fit_basis="index", **kwargs) -> float:
        """Calculate RMS after fitting a nth-degree polynomial."""
        try:
            if fit_basis == "time":
                x = self.time.values.astype("datetime64[ns]").astype("int") / 1e9
                x -= x[0]
            else:
                x = numpy.arange(len(self.time))
            y = self.values
            if len(x) <= degree:
                return numpy.nan

            coeffs = numpy.polyfit(x, y, degree)
            y_fit = numpy.polyval(coeffs, x)
            residuals = numpy.array(y) - numpy.array(y_fit)
            rms_value = numpy.sqrt(numpy.mean(residuals**2))
            return rms_value
        except Exception as e:
            print(f"Error occurred during RMS calculation: {str(e)}")
            return numpy.nan

    def most_recent_value_in_last_minute(self, **kwargs) -> Union[float, int, bool]:
        """Find the most recent value in the last minute."""
        if len(self.time) == 0:
            return None
        last_minute = self.time[-1] - pandas.Timedelta(minutes=1)
        recent_values = self.values[self.time >= last_minute]
        if len(recent_values) == 0:
            return None
        return recent_values[-1]

    def apply(self, method_name: str, **kwargs) -> Union[float, None]:
        """
        Apply a transformation method specified by method_name with optional
        kwargs.

        Args:
            method_name: Name of the method to apply.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the transformation method or None if the
            method is not found.
        """
        # Handle empty or all-NaN arrays after conversion to numpy array
        if self.values.size == 0 or numpy.all(numpy.isnan(self.values.astype(float))):
            return None

        method = getattr(self, method_name, None)
        if method and callable(method):
            try:
                return method(**kwargs)  # Pass values and kwargs directly to the method
            except Exception as e:
                print(f"Error occurred during method '{method_name}' invocation: {str(e)}")
                return None
        else:
            print(f"Method '{method_name}' not found or not callable.")
            return None
