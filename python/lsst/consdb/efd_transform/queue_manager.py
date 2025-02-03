"""Provides tools for managing queues and scheduling workflows for data processing.

This implementation ensures that tasks are created only per interval without handling gaps.
Includes features for task creation, retrieval, and management.
"""

import logging
import math
from datetime import timezone
from typing import List, Optional

from astropy.time import Time, TimeDelta
from lsst.consdb.efd_transform.dao.transformd import TransformdDao


class QueueManager:
    """Manages the creation, retrieval, and execution of tasks in a queue.

    Attributes
    ----------
        db_uri (str): The database URI.
        log (logging.Logger): Logger for logging messages.
        dao (TransformdDao): Data Access Object for interacting with the database.

    """

    def __init__(
        self,
        db_uri: str,
        schema: str,
        logger: logging.Logger,
    ):
        """Initialize the `QueueManager`.

        Args:
        ----
            db_uri (str): The URI of the database.
            schema (str): The schema name in the database.
            logger (Logger): Logger instance for logging queue operations.

        """
        self.dao = TransformdDao(db_uri, schema=schema)
        self.db_uri = db_uri
        self.log = logger

    def create_tasks(
        self,
        start_time: Time,
        end_time: Time,
        process_interval: int,
        time_window: int = 1,
        status: str = "pending",
        butler_repo: str = None,
    ) -> List[dict]:
        """Create tasks based on the given time range and process interval.

        This method generates tasks within the specified time range, divided by
        the process interval. Tasks are created strictly per interval.

        Args:
        ----
            start_time (Time): The start time for the tasks.
            end_time (Time): The end time for the tasks.
            process_interval (int): The interval in minutes between each task.
            time_window (int): The overlaping time window. Defaults to 1.
            status (str): The processing status of the task. Defaults to "pending"

        Returns:
        -------
            list[dict]: A list of dictionaries, each containing the
                'start_time' and 'end_time' for a task.

        """
        # Validate inputs
        if start_time and end_time and start_time >= end_time:
            raise ValueError("start_time must be earlier than end_time.")
        if not isinstance(process_interval, int) or process_interval <= 0:
            raise ValueError("process_interval must be a positive integer.")
        if not isinstance(status, str) or not status.strip():
            raise ValueError("status must be a non-empty string.")

        # Setting the starting times
        # Convert process_interval to TimeDelta once
        process_interval_td = TimeDelta(process_interval * 60, format="sec")

        # Handle start_time logic
        if start_time is None:
            last_task = self.dao.select_last()
            current_utc = Time.now().utc  # Get current time in UTC using Astropy's built-in method

            if last_task is None:
                # First task: [current - interval, current]
                start_time = current_utc - process_interval_td
            else:
                # Subsequent tasks: start at previous task's end_time
                start_time = Time(last_task["end_time"], format="datetime", scale="utc")

        # Handle end_time logic
        if end_time is None:
            end_time = Time.now().utc  # Current UTC time
            # Ensure at least one interval exists
            if (end_time - start_time) < process_interval_td:
                end_time = start_time + process_interval_td

        # Generate time intervals
        intervals = self.create_time_intervals(
            start_time=start_time,
            end_time=end_time,
            process_interval=process_interval_td,
        )

        rows = []
        for t in intervals:

            # Check if task already exists and is idle to avoid duplicates
            if self.check_existing_task_by_interval(t[0], t[1], butler_repo, "idle"):
                self.log.debug(
                    f"Task already exists and is idle for interval {t[0]} to {t[1]}. "
                    f" Skipping task creation."
                )
            else:
                task = {
                    "start_time": t[0].to_datetime(timezone=timezone.utc),
                    "end_time": t[1].to_datetime(timezone=timezone.utc),
                    "timewindow": time_window,
                    "status": status,
                    "butler_repo": butler_repo,
                }
                rows.append(task)

        # Insert tasks into the database
        self.log.debug("Inserting tasks into the database")
        affected_rows = 0
        tasks = []
        for row in rows:
            try:
                task = self.dao.insert(row)
                tasks.append(task)
                affected_rows += 1
            except Exception as e:
                self.log.error(f"Failed to insert task {row}: {e}")

        self.log.info(f"Created {affected_rows} new tasks.")
        return tasks

    def create_time_intervals(
        self,
        start_time: Time,
        end_time: Time,
        process_interval: TimeDelta,
    ) -> List[List[Time]]:
        """Create time intervals between a start and end time.

        Args:
        ----
        start_time : Time
            The starting time for the intervals.
        end_time : Time
            The ending time for the intervals.
        process_interval : TimeDelta
            The length of each processing interval in minutes.

        Returns:
        -------
        intervals : list of list of Time
            A list of intervals, where each interval is represented as a list
            containing the start and end times.

        """
        time_span = (end_time - start_time).sec
        n_intervals = math.ceil(time_span / process_interval.sec)
        intervals = []
        for n in range(n_intervals):
            start = start_time + (n * process_interval)
            end = start + process_interval
            intervals.append([start, end])

        return intervals

    def recent_tasks_to_run(
        self,
        limit: Optional[int] = None,
        margin_seconds: int = 0,
    ) -> List[dict]:
        """Retrieve list of recent tasks to run.

        This method fetches recent tasks from the database up to the specified
        limit. The tasks are selected based on the current UTC time.

        Args:
        ----
            limit (Optional[int]): The maximum number of tasks to retrieve.
                If None, all recent tasks are retrieved.
            margin_seconds: int
                A margin (in seconds). Negative values delay processing tasks to
                ensure data availability.


        Returns:
        -------
            list[dict]: A list of dictionaries, each representing a task.

        """
        end_time = Time.now().utc
        end_time_with_margin = end_time + TimeDelta(margin_seconds, format="sec")

        tasks = self.dao.select_recent(end_time_with_margin.to_datetime(timezone.utc), limit)
        return tasks

    def next_task_to_run(
        self,
        start_time: Optional[Time] = None,
        end_time: Optional[Time] = None,
        margin_seconds: int = 0,  # Allow negative margins
    ) -> Optional[dict]:
        """Retrieve the next task to run within a specified time range.

        Args:
        ----
            start_time: Optional[Time]
                The start time from which to begin searching for the next task.
            end_time: Optional[Time]
                The end time up to which to search for the next task.
            margin_seconds: int
                A margin (in seconds). Negative values delay processing tasks to
                ensure data availability.

        Returns:
        -------
            Optional[dict]
                A dictionary representing the next task to run, or None if no suitable task is found.
        """

        # Convert Astropy Time to timezone-aware datetime (UTC)
        start_dt = start_time.to_datetime(timezone=timezone.utc) if start_time else None
        end_dt = end_time.to_datetime(timezone=timezone.utc) if end_time else None

        # Fetch the next task from the database
        task = self.dao.select_next(start_dt, end_dt)

        # Adjust current time with margin
        current_time_with_margin = Time.now().utc + TimeDelta(margin_seconds, format="sec")
        if task is not None and task["end_time"] >= current_time_with_margin:
            self.log.debug(
                f"Task end time {task['end_time']} is not at least "
                f"{abs(margin_seconds)} seconds in the past. Skipping task."
            )
            return None

        return task

    def waiting_tasks(self, butler_repo: str, status: str = "pending") -> Optional[dict]:
        """Retrieves unprocessed tasks.

        Args:
        ----
            butler_repo (str): The bulter repository relative to the task
            status (str, optional): The status of the tasks to query. Defaults to "pending".

        Returns:
        -------
        Optional[dict]: A dictionary representing the next task with the specified status.
            If no task is found, returns `None`.
        """
        task = self.dao.select_queued(butler_repo, status)

        return task

    def failed_tasks(self, butler_repo: str, max_retries: int = 3) -> Optional[dict]:
        """Retrieves failed tasks.

        Args:
        ----
            butler_repo (str): The bulter repository relative to the task
            max_retries (int): Maximum retries failed task has. Defaults to 3.

        Returns:
        -------
        Optional[dict]: A dictionary representing the next task with the specified status.
            If no task is found, returns `None`.
        """

        task = self.dao.select_failed(butler_repo, max_retries=max_retries)

        # add a retry key to act as a verifier to increment retries
        if task:
            task = [d.update({"retry": True}) or d for d in task]

        return task

    def get_task_by_interval(
        self, start_time: Time, end_time: Time, butler_repo: str, status: str
    ) -> Optional[dict]:
        """Get task by interval

        Args:
        ----
            start_time (Time): The start time for the task
            end_time (Time): The end time for the task
            butler_repo (str): The butler repository relative to the task
            status (str): The status of the task to query

        Returns:
        -------
            Optional[dict]: A dictionary representing the task.
            If no task is found, returns `None`.
        """
        start_time = start_time.to_datetime(timezone.utc)
        end_time = end_time.to_datetime(timezone.utc)
        task = self.dao.get_task_by_interval(start_time, end_time, butler_repo, status)
        return task

    def check_existing_task_by_interval(
        self, start_time: Time, end_time: Time, butler_repo: str, status: str
    ) -> bool:
        """Verifiy existing task by interval

        Args:
        ----
            start_time (Time): The start time for the task
            end_time (Time): The end time for the task
            butler_repo (str): The butler repository relative to the task
            status (str): The status of the task to query

        Returns:
        -------
            bool: True if task exists, False otherwise

        """

        task = self.get_task_by_interval(start_time, end_time, butler_repo, status)
        if task:
            return True

        return False
