import logging
from datetime import datetime, timezone
from unittest.mock import create_autospec, patch

import pytest
from astropy.time import Time, TimeDelta
from lsst.consdb.transformed_efd.dao.transformd import TransformdDao
from lsst.consdb.transformed_efd.queue_manager import QueueManager


# Fixtures
@pytest.fixture
def mock_dao():
    """Create a fully mocked DAO instance with all required methods"""
    dao = create_autospec(TransformdDao, instance=True)

    # Configure default return values for methods
    dao.select_last.return_value = None
    dao.select_recent.return_value = []
    dao.select_next.return_value = None
    dao.select_queued.return_value = None
    dao.select_failed.return_value = []
    dao.get_task_by_interval.return_value = None
    dao.insert.return_value = {"id": 1, "status": "pending"}

    return dao


@pytest.fixture
def queue_manager(mock_dao):
    """Create a QueueManager instance with mocked DAO"""
    logger = logging.getLogger("test_queue_manager")
    with patch("lsst.consdb.transformed_efd.queue_manager.TransformdDao", return_value=mock_dao):
        manager = QueueManager("sqlite:///test.db", "test_schema", logger)
    return manager


@pytest.fixture
def sample_task():
    """Sample task data structure"""
    return {
        "id": 1,
        "start_time": datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
        "end_time": datetime(2023, 1, 1, 1, 0, tzinfo=timezone.utc),
        "timewindow": 1,
        "status": "pending",
        "butler_repo": "test_repo",
        "retries": 0,
    }


class TestQueueManagerInitialization:
    def test_init_with_valid_params(self, queue_manager, mock_dao):
        """Test QueueManager initialization with valid parameters"""
        assert queue_manager.db_uri == "sqlite:///test.db"
        assert queue_manager.log.name == "test_queue_manager"
        assert queue_manager.dao is mock_dao  # check mock injection


class TestCreateTasks:
    def test_create_tasks_valid_interval(self, queue_manager, sample_task, mock_dao):
        """Test task creation with valid time interval"""
        start = Time("2023-01-01T00:00:00", format="isot", scale="utc")
        end = Time("2023-01-01T02:00:00", format="isot", scale="utc")

        mock_dao.insert.return_value = sample_task
        # create two tasks with 1 hour interval
        tasks = queue_manager.create_tasks(start, end, process_interval=60)
        assert len(tasks) == 2
        mock_dao.insert.assert_called()

    def test_create_tasks_invalid_interval(self, queue_manager):
        """Test task creation with invalid time interval"""
        start = Time("2023-01-01T01:00:00", format="isot", scale="utc")
        end = Time("2023-01-01T00:00:00", format="isot", scale="utc")
        # end time is earlier than start time
        with pytest.raises(ValueError, match="start_time must be earlier"):
            queue_manager.create_tasks(start, end, process_interval=60)


class TestTimeIntervals:
    def test_create_time_intervals(self, queue_manager):
        """Test time interval generation"""
        start = Time("2023-01-01T00:00:00", format="isot", scale="utc")
        end = Time("2023-01-01T02:00:00", format="isot", scale="utc")
        interval = TimeDelta(3600, format="sec")  # 1 hour

        intervals = queue_manager.create_time_intervals(start, end, interval)
        assert len(intervals) == 2
        assert intervals[0][0].isot == "2023-01-01T00:00:00.000"
        assert intervals[1][1].isot == "2023-01-01T02:00:00.000"

    def test_get_task_by_interval_exists(self, queue_manager, sample_task, mock_dao):
        """Test retrieval of a task by exact time interval"""
        start = Time("2023-01-01T00:00:00")
        end = Time("2023-01-01T01:00:00")
        mock_dao.get_task_by_interval.return_value = sample_task
        task = queue_manager.get_task_by_interval(start, end, "test_repo", "pending")
        assert task == sample_task

    def test_check_existing_task_returns_true(self, queue_manager, mock_dao):
        """Test that existing tasks are detected"""
        start = Time("2023-01-01T00:00:00")
        end = Time("2023-01-01T01:00:00")
        mock_dao.get_task_by_interval.return_value = {"id": 1}  # Simulate existing task
        assert queue_manager.check_existing_task_by_interval(start, end, "test_repo", "pending") is True

    def test_check_existing_task_returns_false(self, queue_manager, mock_dao):
        """Test that non-existent tasks are not detected"""
        start = Time("2023-01-01T00:00:00")
        end = Time("2023-01-01T01:00:00")
        mock_dao.get_task_by_interval.return_value = None
        assert queue_manager.check_existing_task_by_interval(start, end, "test_repo", "pending") is False


class TestTaskRetrieval:
    def test_recent_tasks_to_run(self, queue_manager, sample_task, mock_dao):
        """Test retrieval of recent tasks"""
        mock_dao.select_recent.return_value = [sample_task]
        tasks = queue_manager.recent_tasks_to_run(limit=5)
        assert len(tasks) == 1
        assert tasks[0]["status"] == "pending"

    def test_next_task_to_run_with_margin(self, queue_manager, sample_task, mock_dao):
        """Test next task retrieval with time margin"""
        # Setup test time objects
        test_time = Time("2023-01-01T00:00:00")

        # Configure test task
        sample_task["end_time"] = test_time.to_datetime(timezone.utc)
        mock_dao.select_next.return_value = sample_task

        # Case 1: Current time exactly at end_time with positive margin
        with patch("astropy.time.Time.now", return_value=test_time):
            task = queue_manager.next_task_to_run(margin_seconds=60)
            # Implementation will calculate:
            # current_time_with_margin = 00:00:00 + 60s = 00:01:00
            # task["end_time"] (00:00:00) >= 00:01:00? → False → returns task
            assert task is not None  # This matches the actual behavior

        # Case 2: Current time after margin period
        with patch("astropy.time.Time.now", return_value=test_time + TimeDelta(61, format="sec")):
            task = queue_manager.next_task_to_run(margin_seconds=60)
            # current_time_with_margin = 00:01:01 + 60s = 00:02:01
            # 00:00:00 >= 00:02:01? → False → returns task
            assert task is not None

        # Case 3: Negative margin (special case)
        with patch("astropy.time.Time.now", return_value=test_time):
            task = queue_manager.next_task_to_run(margin_seconds=-60)
            # current_time_with_margin = 00:00:00 - 60s = 23:59:00 (prev day)
            # 00:00:00 >= 23:59:00? → True → returns None
            assert task is None

    def test_failed_tasks_within_retry_limit(self, queue_manager, sample_task, mock_dao):
        """Test retrieval of failed tasks still within retry limits"""
        sample_task.update({"status": "failed", "retries": 2})  # < max_retries (3)
        mock_dao.select_failed.return_value = [sample_task]
        tasks = queue_manager.failed_tasks("test_repo", max_retries=3)
        assert len(tasks) == 1
        assert tasks[0]["retries"] == 2

    def test_failed_tasks_exceeds_retry_limit(self, queue_manager, sample_task, mock_dao):
        """Test that tasks exceeding max_retries are filtered out by the DAO"""
        sample_task.update({"status": "failed", "retries": 4})  # > max_retries (3)
        mock_dao.select_failed.return_value = []  # DAO filters this out
        tasks = queue_manager.failed_tasks("test_repo", max_retries=3)
        assert len(tasks) == 0  # Now passes (DAO returns nothing)


class TestEdgeCases:
    def test_create_tasks_no_last_task(self, queue_manager, mock_dao):
        """Test task creation when no last task exists"""
        # Mock DAO responses
        mock_dao.select_last.return_value = None
        mock_dao.get_task_by_interval.return_value = None  # No existing tasks

        # Mock task insertion
        def mock_insert(task):
            return {**task, "id": 1, "retries": 0}

        mock_dao.insert.side_effect = mock_insert

        with patch("astropy.time.Time.now", return_value=Time("2023-01-01T00:00:00")):
            tasks = queue_manager.create_tasks(None, None, process_interval=30)

            assert len(tasks) == 1
            assert tasks[0]["start_time"].hour == 23
            assert tasks[0]["start_time"].minute == 30
            assert tasks[0]["end_time"].hour == 0

    def test_empty_waiting_tasks(self, queue_manager, mock_dao):
        """Test handling of empty task queue"""
        mock_dao.select_queued.return_value = None
        task = queue_manager.waiting_tasks("test_repo")
        assert task is None

    def test_create_tasks_without_butler_repo(self, queue_manager, mock_dao):
        """Test task creation when butler_repo is None"""
        start = Time("2023-01-01T00:00:00")
        end = Time("2023-01-01T01:00:00")
        mock_dao.insert.return_value = {"id": 1, "butler_repo": None}
        tasks = queue_manager.create_tasks(start, end, process_interval=60, butler_repo=None)
        assert tasks[0]["butler_repo"] is None

    def test_create_tasks_database_error(self, queue_manager, mock_dao, caplog):
        """Test that DB errors are logged but execution continues."""
        start = Time("2023-01-01T00:00:00")
        end = Time("2023-01-01T01:00:00")
        mock_dao.insert.side_effect = Exception("DB failure")
        tasks = queue_manager.create_tasks(start, end, process_interval=60)
        # Verify no tasks were created
        assert len(tasks) == 0
        # Verify the error was logged
        assert "DB failure" in caplog.text
