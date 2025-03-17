from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from astropy.time import Time, TimeDelta
from lsst.consdb.transformed_efd.queue_manager import QueueManager

# Mock logger
mock_logger = MagicMock()

# Mock DAO
mock_dao = MagicMock()


# Helper function to create mock tasks
def create_mock_task(end_time=None):
    if end_time is None:
        end_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    return {"end_time": end_time}


@pytest.fixture
def queue_manager():
    with patch("lsst.consdb.efd_transform.queue_manager.TransformdDao", return_value=mock_dao):
        return QueueManager("mock_db_uri", "mock_schema", mock_logger)


def test_initialization(queue_manager):
    assert queue_manager.db_uri == "mock_db_uri"
    assert queue_manager.log == mock_logger
    assert isinstance(queue_manager.dao, MagicMock)


def test_create_time_intervals(queue_manager):
    start_time = Time(datetime(2025, 1, 13, 0, 0, tzinfo=timezone.utc))
    end_time = Time(datetime(2025, 1, 13, 0, 20, tzinfo=timezone.utc))
    intervals = queue_manager.create_time_intervals(start_time, end_time, process_interval=10, time_window=2)

    assert len(intervals) == 2
    assert intervals[0][0].datetime.replace(tzinfo=timezone.utc) == datetime(
        2025, 1, 12, 23, 58, tzinfo=timezone.utc
    )


def test_recent_tasks_to_run(queue_manager):
    fixed_time = datetime(2025, 1, 13, 17, 19, 46, tzinfo=timezone.utc)
    mock_dao.select_recent.return_value = [
        {"task_id": 1, "end_time": fixed_time},
        {"task_id": 2, "end_time": fixed_time},
    ]

    with patch("lsst.consdb.efd_transform.queue_manager.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        tasks = queue_manager.recent_tasks_to_run(limit=2)

    assert len(tasks) == 2
    mock_dao.select_recent.assert_called_with(fixed_time, 2)


def test_next_task_to_run(queue_manager):
    # Mock task in the past
    past_task = create_mock_task(datetime.now(timezone.utc) - timedelta(minutes=10))
    mock_dao.select_next.return_value = past_task

    task = queue_manager.next_task_to_run()
    assert task == past_task

    # Mock task in the future
    future_task = create_mock_task(datetime.now(timezone.utc) + timedelta(minutes=10))
    mock_dao.select_next.return_value = future_task

    task = queue_manager.next_task_to_run()
    assert task is None
    mock_logger.debug.assert_called_with(
        f"Task end time {future_task['end_time']} is in the future. Skipping task."
    )


@patch("lsst.consdb.efd_transform.queue_manager.QueueManager.create_time_intervals")
@patch("lsst.consdb.efd_transform.queue_manager.datetime")  # Mock datetime globally in the module
def test_create_tasks(mock_datetime, mock_create_intervals, queue_manager):
    # Set fixed current time
    fixed_now = datetime(2025, 1, 13, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_now
    mock_datetime.side_effect = datetime

    # Define process_interval and time_window
    process_interval = 5  # 5 minutes
    time_window = 1  # 1 minute

    # Mock the intervals as astropy Time objects
    mock_create_intervals.return_value = [
        [
            Time("2025-01-13T00:00:00", format="isot", scale="utc"),
            Time("2025-01-13T00:05:00", format="isot", scale="utc"),
        ],
        [
            Time("2025-01-13T00:05:00", format="isot", scale="utc"),
            Time("2025-01-13T00:10:00", format="isot", scale="utc"),
        ],
    ]

    # Mock the DAO's select_last function to return the last task's end_time
    mock_dao.select_last.return_value = {
        "end_time": Time("2025-01-12T23:55:00", format="isot", scale="utc").datetime
    }

    # Mock the insert function to simply return the task
    mock_dao.insert.side_effect = lambda x: x

    # Calculate expected start_time and end_time
    expected_start_time = Time(
        "2025-01-12T23:54:00", format="isot", scale="utc"
    )  # Last task's end_time - time_window
    adjusted_now = fixed_now.replace(second=0, microsecond=0)  # Align with code logic
    expected_end_time = Time(
        adjusted_now.strftime("%Y-%m-%dT%H:%M:%S"), format="isot", scale="utc"
    ) - TimeDelta(
        60, format="sec"
    )  # Subtract time_window

    # Run create_tasks with mocked process_interval and time_window
    tasks = queue_manager.create_tasks(process_interval=process_interval, time_window=time_window)

    # Verify that create_time_intervals was called with the correct arguments
    mock_create_intervals.assert_called_once_with(
        start_time=expected_start_time,
        end_time=expected_end_time,
        process_interval=process_interval,
        time_window=time_window,
    )

    # Verify the tasks created
    assert len(tasks) == 2
    assert tasks[0]["start_time"] == Time("2025-01-13T00:00:00", format="isot", scale="utc").datetime.replace(
        tzinfo=timezone.utc
    )
    assert tasks[0]["end_time"] == Time("2025-01-13T00:05:00", format="isot", scale="utc").datetime.replace(
        tzinfo=timezone.utc
    )
    assert tasks[1]["start_time"] == Time("2025-01-13T00:05:00", format="isot", scale="utc").datetime.replace(
        tzinfo=timezone.utc
    )
    assert tasks[1]["end_time"] == Time("2025-01-13T00:10:00", format="isot", scale="utc").datetime.replace(
        tzinfo=timezone.utc
    )

    # Ensure the logger and DAO interactions occurred as expected
    mock_logger.info.assert_called_with("Created 2 new tasks.")
    assert mock_dao.insert.call_count == 2
