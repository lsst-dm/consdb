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

"""Handles the transformation of EFD data using configurable models.

Includes functionalities for managing data queues, retrieving configurations,
and transforming data.
"""

import argparse
import asyncio
import logging
import os
import signal
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from astropy.time import Time, TimeDelta
from lsst.consdb.transformed_efd.config_model import ConfigModel
from lsst.consdb.transformed_efd.dao.influxdb import InfluxDbDao
from lsst.consdb.transformed_efd.queue_manager import QueueManager
from lsst.consdb.transformed_efd.transform import Transform
from lsst.daf.butler import Butler


def parse_utc_naive(isostr: str) -> datetime:
    """Parse ISO string to UTC-naive datetime."""
    dt = datetime.fromisoformat(isostr)
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt


def get_logger(path: str | Path | None = None) -> logging.Logger:

    log = logging.getLogger("transformed_efd")
    log.handlers.clear()
    log.propagate = False

    # Get log level from environment variable, default to "INFO"
    env_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, env_level, logging.INFO)  # Default to INFO if invalid level
    log.setLevel(level)

    # Console formatter with UTC time
    console_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ")
    console_fmt.converter = time.gmtime
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_fmt)
    log.addHandler(console_handler)

    if path:
        try:
            path = Path(path) if isinstance(path, str) else path
            path.parent.mkdir(parents=True, exist_ok=True)
            file_fmt = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ"
            )
            file_fmt.converter = time.gmtime
            file_handler = logging.FileHandler(path)
            file_handler.setFormatter(file_fmt)
            log.addHandler(file_handler)
        except (IOError, PermissionError, OSError) as e:
            log.warning(f"Failed to initialize file logging: error={str(e)}")

    return log


def build_argparser() -> argparse.ArgumentParser:
    """Construct CLI argument parser.

    Returns
    -------
    argparse.ArgumentParser
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Process EFD data")

    # Required arguments
    req = parser.add_argument_group("required arguments")
    req.add_argument("-c", "--config", dest="config_name", required=True, help="Config YAML file")
    req.add_argument(
        "-i", "--instrument", dest="instrument", type=str.lower, required=True, help="Instrument name"
    )
    req.add_argument(
        "-r",
        "--repo",
        dest="repo",
        required=True,
        default="s3://rubin-summit-users/butler.yaml",
        help="Butler repository path",
    )
    req.add_argument("-d", "--db", dest="db_conn_str", required=True, help="Database connection string")
    req.add_argument("-E", "--efd", dest="efd_conn_str", required=True, help="EFD connection string")
    req.add_argument(
        "-m", "--mode", dest="mode", required=True, choices=["job", "cronjob"], help="Execution mode"
    )

    # Optional arguments
    opt = parser.add_argument_group("optional arguments")
    opt.add_argument("-s", "--start", dest="start_time", help="Start time (ISO format)")
    opt.add_argument("-e", "--end", dest="end_time", help="End time (ISO format)")
    opt.add_argument(
        "-t", "--timedelta", dest="timedelta", type=int, default=5, help="Processing interval in minutes"
    )
    opt.add_argument(
        "-w", "--timewindow", dest="timewindow", type=int, default=1, help="Overlap window in minutes"
    )
    opt.add_argument("-l", "--logfile", dest="logfile", help="Log file path")
    opt.add_argument(
        "-R",
        "--resume",
        dest="resume",
        action="store_const",
        const=True,
        default=False,
        help="Resume pending tasks",
    )

    return parser


def read_config(config_name: str) -> dict[str, Any]:
    """Load and validate YAML config file.

    Parameters
    ----------
    config_name : str
        Path to YAML configuration file

    Returns
    -------
    dict
        Validated configuration data

    Raises
    ------
    ValidationError
        If config fails schema validation
    FileNotFoundError
        If config file doesn't exist
    """
    with open(config_name) as f:
        config = ConfigModel(**yaml.safe_load(f))
        return config.model_dump()


def _to_astropy_time(dt: datetime | None) -> Time | None:
    """Convert datetime to UTC Astropy Time.

    Parameters
    ----------
    dt : datetime or None
        Input datetime (naive or timezone-aware). If None, returns None.

    Returns
    -------
    Time or None
        Astropy Time object in UTC scale. Returns None if input is None.

    Notes
    -----
    - Converts timezone-aware datetimes to UTC-naive before conversion
    - Naive datetimes are assumed to be in UTC
    """
    if dt is None:
        return None
    dt = dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt
    return Time(dt.isoformat(), format="isot", scale="utc")


async def _process_task(
    task: dict,
    qm: QueueManager,
    tm: Transform,
    log: logging.Logger,
    instrument: str,
    timewindow: int,
    retry: bool = False,
) -> dict[str, int]:
    """Process individual task and update database status.

    Parameters
    ----------
    task : dict
        Task metadata with id/start_time/end_time
    qm : QueueManager
        Queue management interface
    tm : Transform
        Data transformation processor
    log : Logger
        Logging channel
    instrument : str
        Target instrument name
    timewindow : int
        Processing window minutes
    retry : bool
        Flag for retry attempt

    Returns
    -------
    dict
        Processed counts: {'exposures': int, 'visits1': int}
    """
    log.info("-" * 51)
    log.info(
        f"Processing Task: id={task['id']} start_time={task['start_time']} end_time={task['end_time']} "
        f"timewindow={task['timewindow']}"
    )

    qm.dao.task_started(task["id"])
    try:
        counts = tm.process_interval(
            instrument,
            _to_astropy_time(task["start_time"]) - TimeDelta(timewindow * 60, format="sec"),
            _to_astropy_time(task["end_time"]) + TimeDelta(timewindow * 60, format="sec"),
        )
        qm.dao.task_update_counts(task["id"], exposures=counts["exposures"], visits1=counts["visits1"])
        qm.dao.task_completed(task["id"])
        if retry:
            qm.dao.task_retries_increment(task["id"])
        return counts
    except Exception as e:
        log.error(f"Task failure: id={task['id']} error={str(e)}")
        qm.dao.task_failed(task["id"], error=str(e))
        return {"exposures": 0, "visits1": 0}


async def handle_job(
    qm: QueueManager, log: logging.Logger, args: argparse.Namespace, start_time: Time, end_time: Time
) -> list[dict]:
    """Process job-type workflow tasks.

    Parameters
    ----------
    qm : QueueManager
        Task queue interface
    log : Logger
        Logging channel
    args : Namespace
        CLI arguments
    start_time : Time
        Processing window start
    end_time : Time
        Processing window end

    Returns
    -------
    list[dict]
        Tasks to process (queued + failed)
    """
    log.info("-" * 51)
    if args.resume:
        log.info("Resuming idle tasks")
        tasks = qm.waiting_tasks(args.repo, "idle", start_time, end_time)
    else:
        log.debug(f"Creating new tasks: start_time={start_time} end_time={end_time}")
        log.info("Creating new tasks...")
        qm.create_tasks(
            start_time=start_time,
            end_time=end_time,
            process_interval=int(args.timedelta),
            time_window=int(args.timewindow),
            status="idle",
            butler_repo=args.repo,
        )
        tasks = qm.waiting_tasks(args.repo, "idle")

    return tasks + qm.failed_tasks(args.repo, max_retries=3)


def _get_retryable_tasks(
    qm: QueueManager,
    repo: str,
    base_hour: float = 2.82843,
    max_retries: int = 3,
    max_age_hours: float = 72.0,
    log: logging.Logger = None,
) -> List[Dict]:
    """
    Return failed tasks eligible for retry based on exponential backoff.

    Parameters
    ----------
    qm : QueueManager
        Queue management object.
    repo : str
        Repository identifier.
    base_hour : float
        Backoff base in hours. Default is 2.82843.
    max_retries : int
        Maximum retry attempts. Default is 3.
    max_age_hours : float
        Max age in hours before a task is considered stale. Default is 72.

    Returns
    -------
    List[Dict]
        Tasks where (now – created_at) exceeds base_hour**(retries+1)
        but is less than max_age_hours.
    """
    tasks = qm.failed_tasks(repo, max_retries=max_retries)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    max_age = timedelta(hours=max_age_hours)
    selected: List[Dict] = []

    for t in tasks:
        retries = t["retries"]
        created = t["created_at"]
        if created.tzinfo:
            created = created.astimezone(timezone.utc).replace(tzinfo=None)

        since_created = now - created
        next_wait = timedelta(hours=base_hour ** (retries + 1))
        if next_wait < since_created < max_age:
            selected.append(t)
            log.debug(
                f"Task {t['id']} retryable: created_at={t['created_at']} elapsed={since_created}"
                f" required_wait={next_wait}"
            )
        elif since_created >= max_age:
            log.debug(
                f"Task {t['id']} stale: created_at={t['created_at']} elapsed={since_created}"
                f" required_wait={next_wait}"
            )
            qm._mark_task_stale(t["id"])

    return selected


async def handle_cronjob(qm: QueueManager, log: logging.Logger, args: argparse.Namespace) -> list[dict]:
    """Manage periodic cronjob tasks.

    Parameters
    ----------
    qm : QueueManager
        Task queue interface
    log : Logger
        Logging channel
    args : Namespace
        CLI arguments

    Returns
    -------
    list[dict]
        Tasks ready for processing
    """
    if args.resume:
        log.info("-" * 51)
        log.info("Checking for eligible failed tasks")
        return _get_retryable_tasks(
            qm,
            args.repo,
            base_hour=2.82843,
            max_retries=3,
            max_age_hours=72.0,
            log=log,
        )

    else:
        log.info("-" * 51)
        log.debug("Checking for pending tasks")
        tasks = qm.recent_tasks_to_run(margin_seconds=-60)
        waiting_tasks = qm.waiting_tasks(args.repo, "pending")

        if not tasks and not waiting_tasks:
            log.info("Creating new periodic tasks...")
            qm.create_tasks(
                start_time=None,
                end_time=None,
                process_interval=int(args.timedelta),
                time_window=int(args.timewindow),
                butler_repo=args.repo,
            )
            tasks = qm.recent_tasks_to_run(margin_seconds=-60)

        return tasks


async def process_tasks(
    tasks: list[dict],
    qm: QueueManager,
    tm: Transform,
    log: logging.Logger,
    instrument: str,
    timewindow: int,
    batch_size: int = 50,
    shutdown_event: Optional[asyncio.Event] = None,
) -> None:
    """Execute task batches and log results.

    Parameters
    ----------
    tasks : list
        Task dictionaries to process
    qm : QueueManager
        Queue management interface
    tm : Transform
        Data processor
    log : Logger
        Logging handler
    instrument : str
        Target instrument name
    timewindow : int
        Processing window in minutes
    batch_size : int
        Tasks per batch
    """
    totals = {"tasks": 0, "exposures": 0, "visits1": 0}

    for i in range(0, len(tasks), batch_size):
        # Check between batches
        if shutdown_event and shutdown_event.is_set():
            log.warning("Graceful shutdown completed between batches.")
            break

        batch = tasks[i : i + batch_size]
        log.debug("")  # Empty line as separator
        log.debug(f"Processing batch: {i//batch_size + 1}/{(len(tasks)-1)//batch_size + 1}")

        for task in batch:
            await asyncio.sleep(0)  # Yield control to event loop
            counts = await _process_task(task, qm, tm, log, instrument, timewindow, task.get("retry", False))
            totals["tasks"] += 1
            totals["exposures"] += counts["exposures"]
            totals["visits1"] += counts["visits1"]

            # Check between tasks
            if shutdown_event and shutdown_event.is_set():
                log.warning("Graceful shutdown completed between tasks.")
                break  # Exit task loop

        if shutdown_event.is_set():
            break  # Exit batch loop

    log.info("-" * 51)
    log.info(
        f"Summary (inserted/updated): tasks={totals['tasks']} exposures={totals['exposures']}"
        f" visits={totals['visits1']}"
    )


async def main() -> None:
    exec_start = datetime.now(timezone.utc).replace(tzinfo=None)
    args = build_argparser().parse_args()
    log = get_logger(args.logfile)
    exit_code = 0
    shutdown_event = asyncio.Event()

    def _signal_handler() -> None:
        """Handle shutdown signals gracefully."""
        shutdown_event.set()
        log.warning("Received shutdown signal, finishing current task/batch...")

    # Set up signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _signal_handler)

    try:
        # Initialize core components
        butler = Butler(args.repo)
        efd = InfluxDbDao(args.efd_conn_str)

        # Main data transformation processor
        tm = Transform(
            butler=butler,
            db_uri=args.db_conn_str,
            efd=efd,
            config=read_config(args.config_name),
            logger=log,
            commit_every=100,
        )

        # Task queue management system
        qm = QueueManager(
            db_uri=args.db_conn_str, instrument=args.instrument, schema="efd2_scheduler", logger=log
        )

        log.info("All components initialized successfully")

        # Cleanup orphaned tasks
        fixed = qm.dao.fail_orphaned_tasks()
        if fixed:
            log.debug(f"Marked {fixed} orphaned task(s) as failed")

        # Handle time parameters
        time_params = {}
        if args.mode == "job":
            if not (args.start_time and args.end_time):
                raise ValueError("Job mode requires both start and end times")

            time_params = {
                "start_time": _to_astropy_time(parse_utc_naive(args.start_time)),
                "end_time": _to_astropy_time(parse_utc_naive(args.end_time)),
            }

        # Execute workflow
        handler = handle_job if args.mode == "job" else handle_cronjob
        tasks = await handler(qm, log, args, **time_params)

        await process_tasks(
            tasks=tasks,
            qm=qm,
            tm=tm,
            log=log,
            instrument=args.instrument,
            timewindow=int(args.timewindow),
            shutdown_event=shutdown_event,
        )

    except asyncio.CancelledError:
        log.warning("Shutdown completed")
    except ValueError as e:
        log.error(f"Configuration error: error={e}")
        exit_code = 1
    except Exception as e:
        log.error(f"Processing failed: error={e}", exc_info=True)
        exit_code = 1
    finally:
        log.info(f"Runtime: {datetime.now(timezone.utc).replace(tzinfo=None) - exec_start}")
        sys.exit(exit_code)


if __name__ == "__main__":
    """Execute main coroutine."""
    asyncio.run(main())
