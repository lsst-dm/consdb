import datetime

import numpy as np
import pandas as pd
import pytest
from astropy.time import Time
from lsst.consdb.transformed_efd.summary import Summary  # Replace with the actual module path if different


# --- Fixtures ---
@pytest.fixture
def valid_dataframe():
    """Provide a valid DataFrame."""
    times = [
        "2023-01-01 00:00:00",
        "2023-01-01 00:00:30",
        "2023-01-01 00:01:00",
        "2023-01-01 00:01:30",
        "2023-01-01 00:02:00",
    ]
    # parse and localize to UTC
    idx = pd.to_datetime(times).tz_localize("UTC")
    return pd.DataFrame({"value": [1, 2, 3, 4, 5]}, index=idx)


@pytest.fixture
def exposure_times():
    """UTC‐aware astropy Time start/end."""
    start = Time("2023-01-01T00:00:00.000", scale="utc")
    end = Time("2023-01-01T00:02:00.000", scale="utc")
    return start, end


@pytest.fixture
def summary_instance(valid_dataframe, exposure_times):
    """Provide a Summary instance initialized with valid data."""
    start, end = exposure_times
    return Summary(dataframe=valid_dataframe, exposure_start=start, exposure_end=end)


# --- Tests ---


# 1. Test __init__
def test_init_with_valid_data(valid_dataframe, exposure_times):
    start, end = exposure_times
    summary = Summary(dataframe=valid_dataframe, exposure_start=start, exposure_end=end)

    # data_array shape unchanged
    assert summary.data_array.shape == (5, 1)

    # timestamps must be timezone-aware UTC
    tzinfo = summary.timestamps.tz
    assert tzinfo is not None, "Index is not timezone-aware"
    assert tzinfo == datetime.timezone.utc, f"Expected UTC tz, got {tzinfo}"
    assert summary.timestamps[0] == pd.Timestamp("2023-01-01 00:00:00", tz="UTC")

    # exposure_range preserved correctly
    assert summary.exposure_start.isot == "2023-01-01T00:00:00.000"
    assert summary.exposure_end.isot == "2023-01-01T00:02:00.000"


def test_init_with_invalid_index():
    df = pd.DataFrame({"value": [1, 2, 3]}, index=[1, 2, 3])
    start, end = Time("2023-01-01T00:00:00"), Time("2023-01-01T00:02:00")
    with pytest.raises(ValueError, match="The DataFrame index must be a DatetimeIndex."):
        Summary(dataframe=df, exposure_start=start, exposure_end=end)


def test_init_with_invalid_exposure_times(valid_dataframe):
    start, end = Time("2023-01-01T00:02:00"), Time("2023-01-01T00:00:00")
    with pytest.raises(ValueError, match="Exposure start time must be earlier than exposure end time."):
        Summary(dataframe=valid_dataframe, exposure_start=start, exposure_end=end)


def test_init_with_exposure_outside_dataframe(valid_dataframe):
    start, end = Time("2022-12-31T23:00:00"), Time("2022-12-31T23:59:00")
    with pytest.raises(ValueError, match="The DataFrame index must encompass the exposure time range."):
        Summary(dataframe=valid_dataframe, exposure_start=start, exposure_end=end)


# 2. Test __repr__
def test_repr(summary_instance):
    result = repr(summary_instance)
    # Check data_shape formatting
    assert "data_shape=(5, 1)" in result

    # Build expected time_range with UTC-aware timestamps
    time_min = summary_instance.timestamps.min()
    time_max = summary_instance.timestamps.max()
    expected_time_range = f"time_range=({time_min}, {time_max})"
    assert expected_time_range in result

    # Check exposure_range with isot strings
    expected_exposure = (
        f"exposure_range=({summary_instance.exposure_start.isot}, {summary_instance.exposure_end.isot})"
    )
    assert expected_exposure in result


# 3. Test mean
def test_mean(summary_instance):
    assert summary_instance.mean() == 3.0


# 4. Test stddev
def test_stddev(summary_instance):
    assert summary_instance.stddev() == pytest.approx(1.5811, rel=1e-3)


def test_stddev_with_insufficient_values(valid_dataframe, exposure_times):
    df = pd.DataFrame({"value": [np.nan]}, index=pd.to_datetime(["2023-01-01"]))
    start, end = exposure_times
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert summary.stddev() is None


# 5. Test max
def test_max(summary_instance):
    assert summary_instance.max() == 5


# 6. Test min
def test_min(summary_instance):
    assert summary_instance.min() == 1


# 7. Test rms_from_polynomial_fit
def test_rms_from_polynomial_fit_index_basis(summary_instance):
    assert summary_instance.rms_from_polynomial_fit(degree=4, fit_basis="index") == pytest.approx(2.0)


def test_rms_from_polynomial_fit_time_basis(summary_instance):
    assert summary_instance.rms_from_polynomial_fit(degree=4, fit_basis="time") == pytest.approx(2.0)


# 8. Test most_recent_value_in_last_minute
def test_most_recent_value_in_last_minute(summary_instance):
    assert summary_instance.most_recent_value_in_last_minute() == 5


def test_most_recent_value_in_last_minute_no_values_in_range(valid_dataframe):
    start, end = Time("2023-01-01T00:03:00"), Time("2023-01-01T00:04:00")
    with pytest.raises(ValueError, match="The DataFrame index must encompass the exposure time range."):
        Summary(dataframe=valid_dataframe, exposure_start=start, exposure_end=end)


# 9. Test apply
def test_apply_mean(summary_instance):
    result = summary_instance.apply("mean")
    assert result == 3.0


def test_apply_stddev(summary_instance):
    result = summary_instance.apply("stddev")
    assert result == pytest.approx(1.5811, rel=1e-3)


def test_apply_invalid_method(summary_instance):
    with pytest.raises(AttributeError, match="Method not found: method=invalid_method"):
        summary_instance.apply("invalid_method")


def test_apply_with_empty_data():
    df = pd.DataFrame({"value": []}, index=pd.DatetimeIndex([]))
    start, end = Time("2023-01-01T00:00:00"), Time("2023-01-01T00:02:00")
    with pytest.raises(ValueError, match="The DataFrame must not be empty."):  # <-- Updated error message
        Summary(dataframe=df, exposure_start=start, exposure_end=end)
