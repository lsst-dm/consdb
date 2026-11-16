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
import logging
from datetime import UTC, datetime
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
def logger():
    """Configure a logger for capturing in tests"""
    logger = logging.getLogger("test_queue_manager")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    try:
        yield logger
    finally:
        logger.removeHandler(handler)
        handler.close()


@pytest.fixture
def queue_manager(mock_dao, logger):
    """Create a QueueManager instance with mocked DAO and logger"""
    with patch(
        "lsst.consdb.transformed_efd.queue_manager.TransformdDao",
        return_value=mock_dao,
    ):
        # Pass instrument and schema before logger
        manager = QueueManager("sqlite:///test.db", "test_instrument", "test_schema", logger)
    return manager


@pytest.fixture
def sample_task():
    """Sample task data structure"""
    return {
        "id": 1,
        "start_time": datetime(2023, 1, 1, 0, 0, tzinfo=UTC),
        "end_time": datetime(2023, 1, 1, 1, 0, tzinfo=UTC),
        "timewindow": 1,
        "status": "pending",
        "butler_repo": "test_repo",
        "retries": 0,
    }


class TestCreateTasks:
    def test_create_tasks_valid_interval(self, queue_manager, sample_task):
        start = Time("2023-01-01T00:00:00", format="isot", scale="utc")
        end = Time("2023-01-01T02:00:00", format="isot", scale="utc")
        queue_manager.dao.bulk_insert.return_value = [sample_task, sample_task]

        tasks = queue_manager.create_tasks(
            start,
            end,
            process_interval=60,
            time_window=5,
            status="ready",
            butler_repo="test_repo",
        )

        queue_manager.dao.bulk_insert.assert_called_once()
        inserted = queue_manager.dao.bulk_insert.call_args.args[0]
        assert inserted.to_dict("records") == [
            {
                "start_time": datetime(2023, 1, 1, 0, 0, tzinfo=UTC),
                "end_time": datetime(2023, 1, 1, 1, 0, tzinfo=UTC),
                "timewindow": 5,
                "status": "ready",
                "butler_repo": "test_repo",
            },
            {
                "start_time": datetime(2023, 1, 1, 1, 0, tzinfo=UTC),
                "end_time": datetime(2023, 1, 1, 2, 0, tzinfo=UTC),
                "timewindow": 5,
                "status": "ready",
                "butler_repo": "test_repo",
            },
        ]
        assert tasks == [sample_task, sample_task]


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

    @pytest.mark.parametrize(("dao_result", "expected"), [({"id": 1}, True), (None, False)])
    def test_check_existing_task(self, queue_manager, mock_dao, dao_result, expected):
        start = Time("2023-01-01T00:00:00")
        end = Time("2023-01-01T01:00:00")
        mock_dao.get_task_by_interval.return_value = dao_result
        result = queue_manager.check_existing_task_by_interval(start, end, "test_repo", "pending")
        assert result is expected


class TestTaskRetrieval:
    def test_next_task_to_run_with_margin(self, queue_manager, sample_task, mock_dao):
        """Test next task retrieval with time margin"""
        # Setup test time objects
        test_time = Time("2023-01-01T00:00:00")

        # Configure test task
        sample_task["end_time"] = test_time.to_datetime(UTC)
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
