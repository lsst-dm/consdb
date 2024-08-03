from typing import List, Optional, Union

import numpy


class Summary:
    """
    A class that performs various transformations on a list or numpy
    array of values.
    """

    def __init__(self, values: Union[List[Union[float, int, bool, str]], numpy.ndarray]):
        """
        Initialize the Transform object.

        Args:
            values: A list or numpy array of values.

        Returns:
            None
        """
        self.values = numpy.array(values) if not isinstance(values, str) else values

    def apply(self, method_name: str) -> Union[float, None]:
        """
        Apply a transformation method specified by method_name.

        Args:
            method_name: Name of the method to apply.

        Returns:
            The result of the transformation method or None if the
            method is not found.
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

    def col_mean(self) -> float:
        """
        Calculate the mean of the values by column.

        Returns:
            The mean value as a float.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmean(self.values, axis=0)

    def std(self, ddof: Optional[int] = 1) -> float:
        """
        Calculate the standard deviation of the values.

        Args:
            ddof: Delta degrees of freedom.

        Returns:
            The standard deviation as a float.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanstd(self.values, ddof=ddof)

    def col_std(self, ddof: Optional[int] = 1) -> float:
        """
        Calculate the standard deviation of the values by column.

        Args:
            ddof: Delta degrees of freedom.

        Returns:
            The standard deviation as a float.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanstd(self.values, ddof=ddof, axis=0)

    def max(self) -> Union[float, int, bool]:
        """
        Find the maximum value in the values.

        Returns:
            The maximum value as a float, int, or bool.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmax(self.values)

    def col_max(self) -> Union[float, int, bool]:
        """
        Find the maximum value in the values by column.

        Returns:
            The maximum value as a float, int, or bool.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmax(self.values, axis=0)

    def min(self) -> Union[float, int, bool]:
        """
        Find the minimum value in the values.

        Returns:
            The minimum value as a float, int, or bool.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmin(self.values)

    def col_min(self) -> Union[float, int, bool]:
        """
        Find the minimum value in the values by column.

        Returns:
            The minimum value as a float, int, or bool.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.nanmin(self.values, axis=0)

    def logical_and(self) -> Union[bool, numpy.ndarray]:
        """
        Perform element-wise logical AND operation on the values.

        Returns:
            The result of the logical AND operation as a bool or numpy array.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.all(self.values)

    def col_logical_and(self) -> Union[bool, numpy.ndarray]:
        """
        Perform element-wise logical AND operation on the values.

        Returns:
            The result of the logical AND operation as a bool or numpy array.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.all(self.values, axis=0)

    def logical_or(self) -> Union[bool, numpy.ndarray]:
        """
        Perform element-wise logical OR operation on the values by column.

        Returns:
            The result of the logical OR operation as a bool or numpy array.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.any(self.values)

    def col_logical_or(self) -> Union[bool, numpy.ndarray]:
        """
        Perform element-wise logical OR operation on the values.

        Returns:
            The result of the logical OR operation as a bool or numpy array.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return numpy.any(self.values, axis=0)

    def logical_not(self) -> numpy.ndarray:
        """
        Perform element-wise logical NOT operation on the values.

        Returns:
            The result of the logical NOT operation as a numpy array.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return ~numpy.all(self.values)

    def col_logical_not(self) -> numpy.ndarray:
        """
        Perform element-wise logical NOT operation on the values by column.

        Returns:
            The result of the logical NOT operation as a numpy array.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan

        return ~numpy.all(self.values, axis=0)

    def comma_unique(self) -> str:
        """
        Returns a string with unique values separated by commas.

        If the input string is empty, it returns NaN.

        Returns:
            str: A string with unique values separated by commas.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan
        values = self.values.split(",")
        return ",".join(numpy.unique(values))

    def semicolon_unique(self) -> str:
        """
        Returns a string with semicolon-separated unique values.

        If the input string is empty, it returns NaN.
        This method splits the input string by semicolons and returns a
        new string with only the unique values, separated by semicolons.

        Returns:
            str: A string with semicolon-separated unique values.
        """
        if numpy.size(self.values) == 0:
            return numpy.nan
        values = self.values.split(";")
        return ";".join(numpy.unique(values))
