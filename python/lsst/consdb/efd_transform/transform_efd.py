"""Handles the transformation of EFD data using configurable models.

Includes functionalities for managing data queues, retrieving configurations, and
transforming data.
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from astropy.time import Time, TimeDelta
from lsst.consdb.efd_transform.config_model import ConfigModel
from lsst.consdb.efd_transform.dao.influxdb import InfluxDbDao
from lsst.consdb.efd_transform.queue_manager import QueueManager
from lsst.consdb.efd_transform.transform import Transform
from lsst.daf.butler import Butler
from pydantic import ValidationError


def get_logger(path: str, debug: bool = True) -> logging.Logger:
    """Create and configure a logger object.

    Args:
    ----
        path (str): The path to the log file.
        debug (bool, optional): Flag indicating whether to enable debug mode.
        Defaults to True.

    Returns:
    -------
        logging.Logger: The configured logger object.
    """
    logfile = Path(path)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)

    consoleFormatter = logging.Formatter("[%(levelname)s] %(message)s")
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(consoleFormatter)

    log = logging.getLogger("transform")
    log.addHandler(file_handler)
    log.addHandler(consoleHandler)

    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    return log


def build_argparser() -> argparse.ArgumentParser:
    """Build the argument parser for the script.

    Returns
    -------
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="Summarize EFD topics in a time range")
    parser.add_argument("-c", "--config", dest="config_name", required=True, help="config YAML")
    parser.add_argument("-i", "--instrument", dest="instrument", required=True, help="instrument name")
    parser.add_argument(
        "-s", "--start", dest="start_time", required=False, help="start time (ISO, YYYY-MM-DDTHH:MM:SS)"
    )
    parser.add_argument(
        "-e", "--end", dest="end_time", required=False, help="end time (ISO, YYYY-MM-DDTHH:MM:SS)"
    )
    parser.add_argument(
        "-r",
        "--repo",
        dest="repo",
        default="s3://rubin-summit-users/butler.yaml",
        required=True,
        help="Butler repo",
    )
    parser.add_argument(
        "-d", "--db", dest="db_conn_str", required=True, help="Consolidated Database connection string"
    )
    parser.add_argument("-E", "--efd", dest="efd_conn_str", required=True, help="EFD connection string")
    parser.add_argument(
        "-t",
        "--timedelta",
        dest="timedelta",
        default=5,
        required=False,
        help="Processing time interval in minutes",
    )
    parser.add_argument(
        "-w",
        "--timewindow",
        dest="timewindow",
        default=1,
        required=False,
        help="Processing overlapping time window in minutes",
    )
    parser.add_argument("-l", "--logfile", dest="logfile", default="transform.log", help="Log file")
    parser.add_argument(
        "-m",
        "--mode",
        dest="mode",
        choices=["job", "cronjob"],
        required=True,
        help="Execution mode: 'job' for Kubernetes Job or 'cronjob' for periodic tasks",
    )
    parser.add_argument(
        "-R",
        "--resume",
        dest="resume",
        action="store_true",
        default=False,
        required=False,
        help="Resume idle tasks processing",
    )
    return parser


def read_config(config_name: str) -> Dict[str, Any]:
    """Read configuration file and returns the configuration as a dictionary.

    Args:
    ----
        config_name (str): The name of the configuration file.

    Returns:
    -------
        dict: The configuration as a dictionary.

    Raises:
    ------
        ValidationError: If the configuration file is invalid.
    """
    try:
        with open(config_name, "r") as file:
            data = yaml.safe_load(file)
            config = ConfigModel(**data)
            return config.model_dump()
    except ValidationError as e:
        raise e


def _to_astropy_time(dt: Optional[datetime]) -> Optional[Time]:
    """Convert a datetime object to an Astropy Time object.

    Args:
    ----
        dt (Optional[datetime]): The datetime object to convert.

    Returns:
    -------
        Optional[Time]: The converted Astropy Time object, or None if dt is None.
    """
    if dt is None:
        return None
    return Time(dt.isoformat(), format="isot", scale="utc")


def _process_task(
    task: Dict,
    qm: QueueManager,
    tm: Transform,
    log: logging.Logger,
    instrument: str,
    timewindow: int,
    retry: bool = False,
) -> Dict[str, int]:
    """Process a single task and update its status.

    Args:
        task (Dict): The task to process.
        qm (QueueManager): The queue manager instance.
        tm (Transform): The transform instance.
        log (logging.Logger): The logger instance.
        instrument (str): The instrument name.
        timewindow (int): The time window value.

    Returns:
        Dict[str, int]: A dictionary containing the counts of exposures and visits.
    """
    log.info("----------------------------------------------------------")
    log.info(f"Task ID: {task['id']}")
    log.info(f"Start Time: {task['start_time']} End Time: {task['end_time']}")
    log.info(f"Duration: {task['end_time'] - task['start_time']}")

    qm.dao.task_started(task["id"])
    try:
        process_count = tm.process_interval(
            instrument,
            start_time=_to_astropy_time(task["start_time"]) - TimeDelta(timewindow * 60, format="sec"),
            end_time=_to_astropy_time(task["end_time"]) + TimeDelta(timewindow * 60, format="sec"),
        )

        qm.dao.task_update_counts(
            task["id"],
            exposures=process_count["exposures"],
            visits1=process_count["visits1"],
        )

        qm.dao.task_completed(task["id"])
        if retry:
            qm.dao.task_retries_increment(task["id"])
        return process_count

    except Exception as e:
        log.error(f"Error processing task {task['id']}: {e}")
        qm.dao.task_failed(task["id"], error=str(e))
        return {"exposures": 0, "visits1": 0}


async def handle_job(qm: QueueManager, log: logging.Logger, args, start_time, end_time):
    """Handle tasks for Kubernetes job workflow.

    Args:
        qm (QueueManager): The queue manager instance.
        log (logging.Logger): The logger instance.
        args: Parsed arguments.
        start_time: Start time as Astropy Time.
        end_time: End time as Astropy Time.
    """
    print(args)
    if args.resume:
        log.info("Resuming queued tasks.")
        tasks = qm.waiting_tasks(args.repo, "idle")
    else:
        log.info("Creating tasks for the fixed interval.")
        tasks = qm.create_tasks(
            start_time=start_time,
            end_time=end_time,
            process_interval=int(args.timedelta),
            time_window=int(args.timewindow),
            status="idle",
            butler_repo=args.repo,
        )

    # check for failed tasks and add them to the processing queue again
    failed_tasks = qm.failed_tasks(args.repo, max_retries=3)

    tasks += failed_tasks
    return tasks


async def handle_cronjob(qm: QueueManager, log: logging.Logger, args):
    """Handle tasks for CronJob workflow.

    Args:
        qm (QueueManager): The queue manager instance.
        log (logging.Logger): The logger instance.
        args: Parsed arguments.
    """
    log.info("Retrieving tasks for periodic interval.")

    # negative margin means the amount of time that must have passed in seconds
    # since end_time, it ensures running tasks with time intervals in the past
    tasks = qm.recent_tasks_to_run(margin_seconds=-60)

    # check if there are queued pending tasks
    waiting_tasks = qm.waiting_tasks(args.repo, "pending")

    if not tasks and not waiting_tasks:
        log.info("No tasks found. Creating new tasks.")
        qm.create_tasks(
            start_time=None,
            end_time=None,
            process_interval=int(args.timedelta),
            time_window=int(args.timewindow),
            butler_repo=args.repo,
        )
        tasks = qm.recent_tasks_to_run(margin_seconds=-60)

    # check for failed tasks and add them to the processing queue again
    failed_tasks = qm.failed_tasks(args.repo, max_retries=3)

    tasks += failed_tasks

    return tasks


async def process_tasks(
    tasks,
    qm: QueueManager,
    tm: Transform,
    log: logging.Logger,
    instrument: str,
    timewindow: int,
    batch_size: int = 50,
):
    """Process all tasks.

    Args:
        tasks: List of tasks to process.
        qm (QueueManager): The queue manager instance.
        tm (Transform): The transform instance.
        log (logging.Logger): The logger instance.
        instrument (str): The instrument name.
        timewindow (int): The time window value.
    """
    total_tasks, total_exposures, total_visits1 = 0, 0, 0
    num_batches = (len(tasks) + batch_size - 1) // batch_size  # Calculate total number of batches

    for batch_idx in range(num_batches):
        batch = tasks[batch_idx * batch_size : (batch_idx + 1) * batch_size]
        log.info(f"Processing batch {batch_idx + 1}/{num_batches} with {len(batch)} tasks.")

        for task in batch:
            counts = _process_task(task, qm, tm, log, instrument, timewindow, retry=task.get("retry") is True)
            total_exposures += counts["exposures"]
            total_visits1 += counts["visits1"]
            total_tasks += 1

    # Log summary
    log.info("======================================")
    log.info(f"Total Tasks Processed: {total_tasks}")
    log.info(f"Total Exposures: {total_exposures}")
    log.info(f"Total Visits1: {total_visits1}")


async def main() -> None:
    """Entry point of the program."""
    t0 = datetime.now()
    parser = build_argparser()
    args = parser.parse_args()

    log = get_logger(args.logfile)

    # Instantiate the butler
    butler = Butler(args.repo)
    log.debug(f"Butler instantiated: {butler}")

    # Instantiate the EFD
    efd = InfluxDbDao(args.efd_conn_str)
    log.debug(f"EFD connection initialized: {efd}")

    # Read configuration
    config = read_config(args.config_name)
    log.debug(f"Configuration loaded with {len(config['columns'])} columns.")

    # Instantiate the main transform class
    tm = Transform(
        butler=butler,
        db_uri=args.db_conn_str,
        efd=efd,
        config=config,
        logger=log,
        commit_every=100,
    )

    # Instantiate the queue manager
    qm = QueueManager(
        db_uri=args.db_conn_str,
        schema=tm.get_schema_by_instrument(args.instrument),
        logger=log,
    )

    # Convert start_time and end_time to Astropy Time objects
    start_time = _to_astropy_time(datetime.fromisoformat(args.start_time)) if args.start_time else None
    end_time = _to_astropy_time(datetime.fromisoformat(args.end_time)) if args.end_time else None

    # Handle workflows based on mode
    if args.mode == "job":
        if not start_time or not end_time:
            log.error("Start time and end time are required in 'job' mode.")
            sys.exit(1)
        tasks = await handle_job(qm, log, args, start_time, end_time)
    elif args.mode == "cronjob":
        tasks = await handle_cronjob(qm, log, args)

    # Process tasks
    await process_tasks(tasks, qm, tm, log, args.instrument, int(args.timewindow), batch_size=50)

    log.info(f"Elapsed Time: {datetime.now() - t0}")
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
