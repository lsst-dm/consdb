import logging

import astropy.time
import pandas
import pytest

pytest.importorskip("lsst.daf.butler")
from lsst.consdb.transformed_efd.transform import Transform


def make_transform() -> Transform:
    transform = Transform.__new__(Transform)
    transform.log = logging.getLogger(__name__)
    return transform


def test_compute_column_value_end_reference(monkeypatch):
    transform = make_transform()
    start_time = astropy.time.Time("2026-01-01T10:00:00", scale="utc")
    end_time = astropy.time.Time("2026-01-01T10:05:00", scale="utc")
    exposure_times = []

    class RecordingSummary:
        def __init__(self, dataframe, exposure_start, exposure_end):
            exposure_times.append((exposure_start, exposure_end))
            self.dataframe = dataframe

        def apply(self, _function):
            return self.dataframe.iloc[-1, 0]

    monkeypatch.setattr("lsst.consdb.transformed_efd.transform.Summary", RecordingSummary)
    series = pandas.DataFrame(
        {"value": [1.0, 2.0, 3.0]},
        index=pandas.to_datetime(
            [
                "2026-01-01T09:45:00Z",
                "2026-01-01T10:00:00Z",
                "2026-01-01T10:03:00Z",
            ],
            utc=True,
        ),
    )
    topics = [{"series": series}]

    assert (
        transform._compute_column_value(start_time, end_time, topics, "most_recent_value", start_offset=-0.5)
        == 3.0
    )
    assert (
        transform._compute_column_value(
            start_time,
            end_time,
            topics,
            "most_recent_value",
            start_offset=-0.5,
            end_reference="start",
        )
        == 2.0
    )
    assert exposure_times == [(start_time, end_time), (start_time, end_time)]


def test_compute_column_value_start_reference_without_offset():
    transform = make_transform()
    start_time = astropy.time.Time("2026-01-01T10:00:00", scale="utc")
    end_time = astropy.time.Time("2026-01-01T10:05:00", scale="utc")
    series = pandas.DataFrame(
        {"value": [1.0, 2.0]},
        index=pandas.to_datetime(["2026-01-01T10:00:00Z", "2026-01-01T10:03:00Z"], utc=True),
    )

    assert (
        transform._compute_column_value(
            start_time,
            end_time,
            [{"series": series}],
            "most_recent_value",
            end_reference="start",
        )
        == 1.0
    )


def test_process_interval_propagates_end_reference(monkeypatch):
    transform = make_transform()
    start_time = astropy.time.Time("2026-01-01T10:00:00", scale="utc")
    end_time = astropy.time.Time("2026-01-01T10:05:00", scale="utc")
    captured_topics = []

    monkeypatch.setattr(transform, "_get_topic_interval", lambda *_: [start_time, end_time])
    monkeypatch.setattr(
        transform,
        "_map_topics",
        lambda: {
            ("topic", False, None, None, None): {
                "name": "topic",
                "fields": [],
                "columns": [{"name": "lookback", "end_reference": "start"}],
            },
            ("offset_topic", False, -0.5, None, None): {
                "name": "offset_topic",
                "fields": [],
                "columns": [{"name": "normal"}],
            },
        },
    )
    monkeypatch.setattr(
        transform,
        "_process_topic",
        lambda topic, *_args, **_kwargs: captured_topics.append(topic),
    )

    transform._process_interval([], [], start_time, end_time)

    assert captured_topics[0]["columns"][0]["function_args"]["end_reference"] == "start"
    assert captured_topics[1]["columns"][0]["function_args"]["end_reference"] == "end"
    assert captured_topics[1]["columns"][0]["function_args"]["start_offset"] == -0.5
