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
import datetime

import numpy as np
import pandas as pd
import pytest
from astropy.time import Time

# Replace with the actual module path if different
from lsst.consdb.transformed_efd.auxiliary.m1m3 import GLASS_THERMOCOUPLES
from lsst.consdb.transformed_efd.summary import Summary


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
    assert tzinfo == datetime.UTC, f"Expected UTC tz, got {tzinfo}"
    assert summary.timestamps[0] == pd.Timestamp("2023-01-01 00:00:00", tz="UTC")

    # exposure_range preserved correctly
    assert summary.exposure_start.isot == "2023-01-01T00:00:00.000"
    assert summary.exposure_end.isot == "2023-01-01T00:02:00.000"


def test_init_with_invalid_index():
    df = pd.DataFrame({"value": [1, 2, 3]}, index=[1, 2, 3])
    start, end = Time("2023-01-01T00:00:00"), Time("2023-01-01T00:02:00")
    with pytest.raises(TypeError, match="The DataFrame index must be a DatetimeIndex."):
        Summary(dataframe=df, exposure_start=start, exposure_end=end)


def test_init_with_invalid_exposure_times(valid_dataframe):
    start, end = Time("2023-01-01T00:02:00"), Time("2023-01-01T00:00:00")
    with pytest.raises(ValueError, match="Exposure start time must be earlier than exposure end time."):
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


# 3b. Test median
def test_median(summary_instance):
    assert summary_instance.median() == 3.0


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


def test_rms_from_polynomial_fit_with_missing_values(exposure_times):
    """Gaps must be filtered before polyfit, not propagate NaN into RMS."""
    times = pd.to_datetime(
        [
            "2023-01-01 00:00:00",
            "2023-01-01 00:00:30",
            "2023-01-01 00:01:00",
            "2023-01-01 00:01:30",
            "2023-01-01 00:02:00",
        ]
    ).tz_localize("UTC")
    y = np.array([1.0, 2.0, np.nan, 4.0, 5.0])
    df = pd.DataFrame({"value": y}, index=times)
    start, end = exposure_times
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)

    x = np.arange(len(y), dtype=np.float64)
    y2 = y.reshape(-1, 1)
    mask = np.isfinite(x) & np.all(np.isfinite(y2), axis=1)
    coeffs = np.polyfit(x[mask], y2[mask], 1)
    expected = np.sqrt(np.mean((y2[mask] - np.polyval(coeffs, x[mask])) ** 2))
    result = summary.rms_from_polynomial_fit(degree=1, fit_basis="index")
    assert np.isfinite(result)
    assert result == pytest.approx(expected)


def test_rms_from_polynomial_fit_insufficient_finite_samples(exposure_times):
    times = pd.to_datetime(
        [
            "2023-01-01 00:00:00",
            "2023-01-01 00:00:30",
            "2023-01-01 00:01:00",
        ]
    ).tz_localize("UTC")
    df = pd.DataFrame({"value": [1.0, np.nan, np.nan]}, index=times)
    start, end = exposure_times
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert np.isnan(summary.rms_from_polynomial_fit(degree=1, fit_basis="index"))


# 8. Test most_recent_value
def test_most_recent_value(summary_instance):
    assert summary_instance.most_recent_value() == 5


def test_most_recent_value_skips_trailing_nan(exposure_times):
    times = pd.to_datetime(
        [
            "2023-01-01 00:00:00",
            "2023-01-01 00:00:30",
            "2023-01-01 00:01:00",
        ]
    ).tz_localize("UTC")
    df = pd.DataFrame({"value": [1.0, 2.0, np.nan]}, index=times)
    start, end = exposure_times
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert summary.most_recent_value() == pytest.approx(2.0)


# 9. Test apply
def test_apply_mean(summary_instance):
    result = summary_instance.apply("mean")
    assert result == 3.0


def test_apply_stddev(summary_instance):
    result = summary_instance.apply("stddev")
    assert result == pytest.approx(1.5811, rel=1e-3)


def test_apply_median(summary_instance):
    result = summary_instance.apply("median")
    assert result == 3.0


def test_apply_invalid_method(summary_instance):
    with pytest.raises(AttributeError, match="Method not found: method=invalid_method"):
        summary_instance.apply("invalid_method")


def test_apply_with_empty_data():
    df = pd.DataFrame({"value": []}, index=pd.DatetimeIndex([]))
    start, end = Time("2023-01-01T00:00:00"), Time("2023-01-01T00:02:00")
    with pytest.raises(ValueError, match="The DataFrame must not be empty."):  # <-- Updated error message
        Summary(dataframe=df, exposure_start=start, exposure_end=end)


# ------------------------------------------------------------------
# Tests: metadata separation (_process_dataframe)
# ------------------------------------------------------------------


@pytest.fixture
def dataframe_with_metadata():
    """DataFrame with numeric telemetry and non-numeric metadata columns."""
    times = pd.to_datetime(
        [
            "2023-01-01 00:00:00",
            "2023-01-01 00:00:30",
            "2023-01-01 00:01:00",
        ]
    ).tz_localize("UTC")
    return pd.DataFrame(
        {
            "temperatureItem0": [20.1, 20.2, 20.0],
            "temperatureItem1": [20.3, 20.4, 20.2],
            "salIndex": ["114", "114", "115"],
            "sensorName": [
                "m1m3-ts-1 1/6",
                "m1m3-ts-1 1/6",
                "m1m3-ts-2 3/6",
            ],
        },
        index=times,
    )


@pytest.fixture
def exposure_times_short():
    start = Time("2023-01-01T00:00:00.000", scale="utc")
    end = Time("2023-01-01T00:01:00.000", scale="utc")
    return start, end


def test_metadata_separation(dataframe_with_metadata, exposure_times_short):
    """Non-numeric columns go to metadata, numeric to data_array."""
    start, end = exposure_times_short
    summary = Summary(dataframe=dataframe_with_metadata, exposure_start=start, exposure_end=end)

    # data_array has only numeric columns (temperatureItem0, temperatureItem1)
    assert summary.data_array.shape == (3, 2)

    # metadata has non-numeric columns
    assert summary.metadata is not None
    assert list(summary.metadata.columns) == ["salIndex", "sensorName"]
    assert len(summary.metadata) == 3


def test_mean_with_metadata_present(dataframe_with_metadata, exposure_times_short):
    """mean() ignores metadata columns, same result as if they
    weren't there.
    """
    start, end = exposure_times_short
    summary = Summary(dataframe=dataframe_with_metadata, exposure_start=start, exposure_end=end)
    # mean of all 6 values: (20.1+20.2+20.0+20.3+20.4+20.2) / 6
    expected = np.nanmean([20.1, 20.3, 20.2, 20.4, 20.0, 20.2])
    assert summary.mean() == pytest.approx(expected)


def test_median_with_metadata_present(dataframe_with_metadata, exposure_times_short):
    """median() ignores metadata columns."""
    start, end = exposure_times_short
    summary = Summary(dataframe=dataframe_with_metadata, exposure_start=start, exposure_end=end)
    result = summary.median()
    assert result == pytest.approx(20.2)


def test_no_metadata_when_no_non_numeric_columns(valid_dataframe, exposure_times):
    """metadata is None when DataFrame has only numeric columns."""
    start, end = exposure_times
    summary = Summary(dataframe=valid_dataframe, exposure_start=start, exposure_end=end)
    assert summary.metadata is None


def test_nan_values_preserved_in_data_array(exposure_times_short):
    """NaN values survive into data_array (no dropna)."""
    times = pd.to_datetime(["2023-01-01 00:00:00", "2023-01-01 00:00:30"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "temp0": [20.0, np.nan],
            "temp1": [np.nan, 20.5],
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    # Both values preserved; mean skips NaN
    assert summary.mean() == pytest.approx(20.25)
    assert summary.median() == pytest.approx(20.25)


# ------------------------------------------------------------------
# Tests: M1M3 bulk temperature (DM-55710)
# ------------------------------------------------------------------


def _glass_thermocouple_samples():
    """Return (salIndex, sensorName, temperatureItem_index) for glass TCs."""
    samples = []
    for sal_idx, channel in sorted(GLASS_THERMOCOUPLES):
        sequence_num = channel // 16 + 1
        item_idx = channel % 16
        sensor_name = f"m1m3-ts-{sal_idx} {sequence_num}/6"
        samples.append((sal_idx, sensor_name, item_idx))
    return samples


def _build_m1m3_dataframe(samples, rng=None):
    """Build a minimal M1M3 DataFrame from thermocouple samples.

    Each sample becomes one row with a single valid temperatureItem;
    all other temperatureItems are NaN.
    """
    if rng is None:
        rng = np.random.default_rng(42)

    rows = []
    for sal_idx, sensor_name, item_idx in samples[:10]:  # cap at 10 rows
        temps = [np.nan] * 16
        temps[item_idx] = rng.uniform(19.0, 22.0)
        row = {f"temperatureItem{i}": temps[i] for i in range(16)}
        row["salIndex"] = str(sal_idx)
        row["sensorName"] = sensor_name
        rows.append(row)

    times = pd.to_datetime([f"2023-01-01 00:00:{i:02d}" for i in range(len(rows))]).tz_localize("UTC")
    return pd.DataFrame(rows, index=times)


@pytest.fixture
def m1m3_dataframe():
    """Mock M1M3 thermocouple data for 2 scanners, 2 sensorNames each."""
    times = pd.to_datetime(
        [
            "2023-01-01 00:00:00",
            "2023-01-01 00:00:30",
        ]
    ).tz_localize("UTC")
    # 2 temperatureItems per row for simplicity (real data has 16)
    return pd.DataFrame(
        {
            "temperatureItem0": [20.1, 20.5],
            "temperatureItem1": [20.3, np.nan],
            "salIndex": ["114", "115"],
            "sensorName": [
                "m1m3-ts-1 1/6",  # item0=ch0 cold junction; item1=ch1 glass
                "m1m3-ts-2 2/6",  # item0=ch16 glass
            ],
        },
        index=times,
    )


def test_m1m3_bulk_temperature_median(m1m3_dataframe, exposure_times_short):
    """Bulk median over valid thermocouple readings."""
    start, end = exposure_times_short
    summary = Summary(dataframe=m1m3_dataframe, exposure_start=start, exposure_end=end)
    result = summary.m1m3_bulk_temperature_median()
    # 20.1 is ch0 (cold junction); valid: 20.3, 20.5
    assert result == pytest.approx(np.median([20.3, 20.5]))


def test_m1m3_bulk_temperature_mean(m1m3_dataframe, exposure_times_short):
    """Bulk mean over valid thermocouple readings."""
    start, end = exposure_times_short
    summary = Summary(dataframe=m1m3_dataframe, exposure_start=start, exposure_end=end)
    result = summary.m1m3_bulk_temperature_mean()
    assert result == pytest.approx(np.mean([20.3, 20.5]))


def test_m1m3_bulk_no_metadata_returns_none(valid_dataframe, exposure_times):
    """Returns None when metadata is not available."""
    start, end = exposure_times
    summary = Summary(dataframe=valid_dataframe, exposure_start=start, exposure_end=end)
    assert summary.m1m3_bulk_temperature_median() is None
    assert summary.m1m3_bulk_temperature_mean() is None


def test_m1m3_bulk_no_sensor_name_returns_none(exposure_times_short):
    """Returns None when sensorName is not in metadata."""
    times = pd.to_datetime(["2023-01-01 00:00:00"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "temperatureItem0": [20.0],
            "salIndex": ["114"],  # string → non-numeric → metadata
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert summary.m1m3_bulk_temperature_median() is None


def test_m1m3_bulk_invalid_sensor_name(exposure_times_short):
    """Rows with non-matching sensorName are skipped."""
    times = pd.to_datetime(["2023-01-01 00:00:00"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "temperatureItem0": [20.0],
            "salIndex": [114],
            "sensorName": ["not-a-valid-m1m3-sensor"],
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    # sensorName doesn't match regex → no valid temperatures
    assert summary.m1m3_bulk_temperature_median() is None


def test_m1m3_bulk_all_nan_returns_none(exposure_times_short):
    """All-NaN temperatureItems return None."""
    times = pd.to_datetime(["2023-01-01 00:00:00"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "temperatureItem0": [np.nan],
            "temperatureItem1": [np.nan],
            # String so salIndex stays in metadata.
            "salIndex": ["114"],
            "sensorName": ["m1m3-ts-1 1/6"],
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert summary.m1m3_bulk_temperature_median() is None
    assert summary.m1m3_bulk_temperature_mean() is None


def test_m1m3_bulk_via_apply(m1m3_dataframe, exposure_times_short):
    """Bulk functions work through apply()."""
    start, end = exposure_times_short
    summary = Summary(dataframe=m1m3_dataframe, exposure_start=start, exposure_end=end)
    result = summary.apply("m1m3_bulk_temperature_median")
    assert result == pytest.approx(np.median([20.3, 20.5]))


def test_m1m3_bulk_salindex_not_in_value_pool(exposure_times_short):
    """salIndex must stay in metadata and not pollute median/mean."""
    times = pd.to_datetime(["2023-01-01 00:00:00"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "temperatureItem0": [11.0],
            "temperatureItem1": [12.0],
            "salIndex": ["115"],  # would coerce to 115 and inflate mean if treated as value
            "sensorName": ["m1m3-ts-02 2/6"],
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert summary.metadata is not None
    assert "salIndex" in summary.metadata.columns
    assert summary.data_array.shape == (1, 2)
    assert summary.m1m3_bulk_temperature_median() == pytest.approx(11.5)
    assert summary.m1m3_bulk_temperature_mean() == pytest.approx(11.5)


def test_m1m3_bulk_numeric_salindex_stays_metadata(exposure_times_short):
    """Even numeric salIndex must not enter data_array."""
    times = pd.to_datetime(["2023-01-01 00:00:00"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "temperatureItem0": [11.0],
            "salIndex": [117],
            "sensorName": ["m1m3-ts-04 2/6"],
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert summary.data_array.shape == (1, 1)
    assert "salIndex" in summary.metadata.columns
    assert summary.m1m3_bulk_temperature_mean() == pytest.approx(11.0)


def test_m1m3_bulk_with_glass_thermocouples(exposure_times_short):
    """Bulk temperature using the consdb glass thermocouple snapshot."""
    df = _build_m1m3_dataframe(_glass_thermocouple_samples())
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)

    median_result = summary.m1m3_bulk_temperature_median()
    mean_result = summary.m1m3_bulk_temperature_mean()

    assert median_result is not None
    assert mean_result is not None
    assert np.isfinite(median_result)
    assert np.isfinite(mean_result)


def test_m1m3_bulk_uses_column_name_not_position(exposure_times_short):
    """Extra numeric columns must not shift temperatureItem channel mapping."""
    times = pd.to_datetime(["2023-01-01 00:00:00"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "pressure": [999.0],
            "temperatureItem0": [99.0],
            "temperatureItem1": [20.3],
            "salIndex": ["114"],
            "sensorName": ["m1m3-ts-1 1/6"],
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    # pressure and cold-junction item0 skipped; item1 is glass channel 1
    assert summary.m1m3_bulk_temperature_median() == pytest.approx(20.3)


def test_m1m3_bulk_skips_cold_junction(exposure_times_short):
    """Channel 0 (cold junction) is not a glass thermocouple."""
    times = pd.to_datetime(["2023-01-01 00:00:00"]).tz_localize("UTC")
    df = pd.DataFrame(
        {
            "temperatureItem0": [99.0],
            "salIndex": [114],
            "sensorName": ["m1m3-ts-1 1/6"],
        },
        index=times,
    )
    start, end = exposure_times_short
    summary = Summary(dataframe=df, exposure_start=start, exposure_end=end)
    assert summary.m1m3_bulk_temperature_median() is None
    assert summary.m1m3_bulk_temperature_mean() is None
