import logging
import math
from datetime import datetime, timezone
from typing import Optional

from astropy.time import Time, TimeDelta
from lsst.consdb.efd_transform.dao.transformd import TransformdDao


class QueueManager:
    """
    Manages the creation, retrieval, and execution of tasks in a queue.
    Attributes:
        db_uri (str): The database URI.
        log (logging.Logger): Logger for logging messages.
        dao (TransformdDao): Data Access Object for interacting with the
            database.
    """

    def __init__(
        self,
        db_uri: str,
        schema: str,
        logger: logging.Logger,
    ):
        self.dao = TransformdDao(db_uri, schema=schema)
        self.db_uri = db_uri
        self.log = logger

        # All task fields
        # task = {
        #     'start_time': datetime,
        #     'end_time': datetime,
        #     'status': 'pending',
        #     'process_start_time': None,
        #     'process_end_time': None,
        #     'process_exec_time': 0,
        #     'exposures': 0,
        #     'visits1': 0,
        #     'retries': 0,
        #     'error': None,
        #     'created_at': datetime.now(timezone.utc),
        # }

    def create_tasks(
        self,
        start_time: Optional[Time] = None,
        end_time: Optional[Time] = None,
        process_interval: int = 5,
        time_window: int = 1,
        status: str = "pending",
    ) -> list[dict]:
        """
        Create tasks based on the given time range and process interval.
        This method generates tasks within the specified time range, divided by
        the process interval. If the start time is not provided, it will use
        the end time of the last task from the database, or the current time
        minus the process interval if no previous tasks exist. If the end time
        is not provided, it will use the current time minus the time window.
        Args:
            start_time (Optional[Time]): The start time for the tasks.
                Defaults to None.
            end_time (Optional[Time]): The end time for the tasks.
                Defaults to None.
            process_interval (int): The interval in minutes between each task.
                Defaults to 5.
            time_window (int): The time window in minutes to look back from
                the end time. Defaults to 1.
        Returns:
            list[dict]: A list of dictionaries, each containing the
                'start_time' and 'end_time' for a task.
        """

        proccess_interval_seconds = TimeDelta(process_interval * 60, format="sec")

        time_window_seconds = TimeDelta(time_window * 60, format="sec")

        # If start time is None, get last task end time.
        if start_time is None:
            last_task = self.dao.select_last()
            # If there is no previous task, then start is now minus the
            # process interval.
            if last_task is None:
                start_time = (
                    datetime.now(tz=timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None)
                )
                start_time = (
                    Time(start_time.isoformat(), format="isot", scale="utc") - proccess_interval_seconds
                )
            # Otherwise, start is the last task end time - time window.
            else:
                start_time = last_task["end_time"]
                start_time = Time(start_time.isoformat(), format="isot", scale="utc") - time_window_seconds

        if end_time is None:
            # Considering that in real-time execution, the final time must be
            # at most now. It is necessary to subtract the time window to
            # ensure that the last task is less than now.
            end_time = datetime.now(tz=timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None)
            end_time = Time(end_time.isoformat(), format="isot", scale="utc")
            end_time = end_time - time_window_seconds
            # allows creating tasks for the future.
            # the responsibility for not executing future tasks is the
            # next_task_to_run function.
            if start_time > end_time:
                end_time = start_time + proccess_interval_seconds

        # start and end times computed before generating the interval list
        # self.log.debug(f"Current time: {now}")
        # self.log.debug(f"Start time: {start_time}")
        # self.log.debug(f"End time: {end_time}")
        # self.log.debug(f"Process interval: {process_interval} minutes")
        # self.log.debug(f"Time window: {time_window} minutes")

        # If diference between start and end is less than process interval,
        # create_time_intervals return an empty list.
        intervals = self.create_time_intervals(
            start_time=start_time,
            end_time=end_time,
            process_interval=process_interval,
            time_window=time_window,
        )

        rows = []
        for t in intervals:
            task = {
                "start_time": t[0].datetime.replace(tzinfo=timezone.utc),
                "end_time": t[1].datetime.replace(tzinfo=timezone.utc),
                "timewindow": time_window,
                "status": status,
            }
            rows.append(task)

        # TODO: Order tasks by start_time
        # Usar um dataframe, ordenar e depois converter para lista de
        # dicionários

        self.log.debug("Insert tasks into database")
        affected_rows = 0
        tasks = []
        for row in rows:
            task = self.dao.insert(row)
            tasks.append(task)
            affected_rows += 1

        self.log.info(f"Created {affected_rows} new tasks.")

        return tasks

    def create_time_intervals(
        self, start_time: Time, end_time: Time, process_interval: int, time_window: int
    ):
        """
        Create a list of time intervals between a start and end time,
        with each interval expanded by a specified time window.
        Parameters:
        -----------
        start_time : Time
            The starting time for the intervals.
        end_time : Time
            The ending time for the intervals.
        process_interval : int
            The length of each processing interval in minutes.
        time_window : int
            The length of the time window to expand each interval by,
            in minutes.
        Returns:
        --------
        intervals : list of list of Time
            A list of intervals, where each interval is represented as a list
            containing the start and end times, expanded by the time window.
        """

        proccess_interval_seconds = TimeDelta(process_interval * 60, format="sec")
        time_window_seconds = TimeDelta(time_window * 60, format="sec")

        time_span = (end_time - start_time).sec
        n_intervals = math.ceil(time_span / proccess_interval_seconds.sec)

        intervals = []
        for n in range(n_intervals):
            # calculate proccess interval start and end
            start = start_time + (n * proccess_interval_seconds)
            end = start + proccess_interval_seconds
            # calculate time window start and end
            start = start - time_window_seconds
            end = end + time_window_seconds

            intervals.append([start, end])

        return intervals

    def recent_tasks_to_run(self, limit: Optional[int] = None) -> list[dict]:
        """
        Retrieve a list of recent tasks to run.

        This method fetches recent tasks from the database up to the specified
        limit.
        The tasks are selected based on the current UTC time.

        Args:
            limit (Optional[int]): The maximum number of tasks to retrieve.
            If None, all recent tasks are retrieved.

        Returns:
            list[dict]: A list of dictionaries, each representing a task.
        """

        end_time = datetime.now(timezone.utc)

        tasks = self.dao.select_recent(end_time, limit)
        return tasks

    def next_task_to_run(
        self, start_time: Optional[Time] = None, end_time: Optional[Time] = None, time_window: int = 1
    ) -> Optional[dict]:
        """
        Retrieve the next task to run within a specified time window.

        Parameters:
        -----------
        start_time : Optional[Time]
            The start time from which to begin searching for the next task.
            If provided, the search will start from this time minus
            the time window.
        end_time : Optional[Time]
            The end time up to which to search for the next task.
            If provided, the search will end at this time plus the time window.
        time_window : int, optional
            The time window in minutes to adjust the start and end times.
            Default is 1 minute.

        Returns:
        --------
        Optional[dict]
            A dictionary representing the next task to run,
            or None if no suitable task is found or if the task's end time
            is in the future.
        """

        time_window_seconds = TimeDelta(time_window * 60, format="sec")

        if start_time is not None:
            start_time = start_time - time_window_seconds
        if end_time is not None:
            end_time = end_time + time_window_seconds

        if start_time is not None and end_time is not None:
            task = self.dao.select_next(start_time.datetime, end_time.datetime)
        else:
            task = self.dao.select_next()

        # Ensure that the task's end time is not greater than the current time.
        if task is not None and task["end_time"] > datetime.now(timezone.utc):
            self.log.debug(f"Task end time {task['end_time']} is in the future. Skipping task.")
            return None

        return task
