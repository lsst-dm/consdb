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
        datatype: Optional[str] = "object",  # Keep the default datatype to "object"
    ):
        """
        Initialize Summary with a DataFrame of numeric and boolean values.
        """

        # Handle NaN values within the DataFrame before conversion
        dataframe = dataframe.fillna(numpy.nan)  # Ensure NaN values are correctly represented

        # Convert the DataFrame to a NumPy array with the specified datatype
        self.values = numpy.array(dataframe.to_numpy(), dtype=datatype)
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

    def mean_columnwise(self, **kwargs) -> float:
        """Calculate column-wise mean."""
        return numpy.apply_along_axis(numpy.nanmean, axis=0, arr=self.values)

    def stddev_columnwise(self, ddof: int = 1, **kwargs) -> float:
        """Calculate column-wise standard deviation."""
        return numpy.apply_along_axis(numpy.nanstd, axis=0, arr=self.values, ddof=ddof)

    def max_columnwise(self, **kwargs) -> Union[float, int, bool]:
        """Find column-wise maximum value."""
        return numpy.apply_along_axis(numpy.nanmax, axis=0, arr=self.values)

    def min_columnwise(self, **kwargs) -> Union[float, int, bool]:
        """Find column-wise minimum value."""
        return numpy.apply_along_axis(numpy.nanmin, axis=0, arr=self.values)

    def rms_from_polynomial_fit(self, degree=1, **kwargs) -> float:
        """Calculate RMS after fitting a nth-degree polynomial."""

        values = self.values.astype(numpy.float64).flatten()
        try:
            index = numpy.isfinite(values)
            x, y = numpy.arange(len(values))[index], values[index]

            if len(x) <= degree:
                return numpy.nan

            coeffs = numpy.polyfit(x, y, degree)
            y_fit = numpy.polyval(coeffs, x)
            rms_value = numpy.sqrt(numpy.nanmean(y - y_fit) ** 2)
            return rms_value
        except Exception as e:
            print(f"Error occurred during RMS calculation: {str(e)}")
            return numpy.nan

    def rms_from_polynomial_fit_columnwise(self, degree=1, **kwargs) -> float:
        """Calculate RMS after fitting a nth-degree polynomial, columnwise."""
        return numpy.apply_along_axis(
            self.rms_from_polynomial_fit,
            axis=0,
            arr=self.values,
            **kwargs,
        )

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
