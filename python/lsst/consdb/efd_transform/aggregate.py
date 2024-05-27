from typing import List, Optional, Union

import numpy


class Aggregate:
    """
    A class that performs various transformations on a list or numpy
    array of values.
    """

    def __init__(self, values: Union[List[Union[float, int, bool]], numpy.ndarray]):
        """
        Initialize the Transform object.

        Args:
            values: A list or numpy array of values.

        Returns:
            None
        """
        self.values = numpy.array(values)

    def apply(self, method_name: str) -> Union[float, None]:
        """
        Apply a transformation method specified by method_name.

        Args:
            method_name: Name of the method to apply.

        Returns:
            The result of the transformation method or None if the method is not found.
        """
        method = getattr(self, method_name, None)
        if method:
            return method()
        else:
            return None

    def mean(self) -> float:
        """
        Calculate the mean of the values.

        Returns:
            The mean value as a float.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmean(self.values)

    def std(self, ddof: Optional[int] = 1) -> float:
        """
        Calculate the standard deviation of the values.

        Args:
            ddof: Delta degrees of freedom.

        Returns:
            The standard deviation as a float.
        """
        return numpy.nanstd(self.values, ddof=ddof)

    def max(self) -> Union[float, int, bool]:
        """
        Find the maximum value in the values.

        Returns:
            The maximum value as a float, int, or bool.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmax(self.values)

    def min(self) -> Union[float, int, bool]:
        """
        Find the minimum value in the values.

        Returns:
            The minimum value as a float, int, or bool.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmin(self.values)

    def logical_and(self) -> Union[bool, numpy.ndarray]:
        """
        Perform element-wise logical AND operation on the values.

        Returns:
            The result of the logical AND operation as a bool or numpy array.
        """
        return numpy.logical_and(self.values)

    def logical_or(self) -> Union[bool, numpy.ndarray]:
        """
        Perform element-wise logical OR operation on the values.

        Returns:
            The result of the logical OR operation as a bool or numpy array.
        """
        return numpy.logical_or(self.values)

    def logical_not(self) -> numpy.ndarray:
        """
        Perform element-wise logical NOT operation on the values.

        Returns:
            The result of the logical NOT operation as a numpy array.
        """
        return numpy.logical_not(self.values)

    def logical_xor(self, other_values: Union[List[Union[float, int, bool]], numpy.ndarray]) -> numpy.ndarray:
        """
        Perform element-wise logical XOR operation between the values
        and other values.

        Args:
            other_values: A list or numpy array of other values.

        Returns:
            The result of the logical XOR operation as a numpy array.
        """
        other_values = numpy.array(other_values)
        return numpy.logical_xor(self.values, other_values)

    def percentile(self, q: float) -> Union[float, int, bool]:
        """
        Calculate the q-th percentile of the values.

        Args:
            q: The percentile value.

        Returns:
            The q-th percentile value as a float, int, or bool.
        """
        return numpy.nanpercentile(self.values, q)
