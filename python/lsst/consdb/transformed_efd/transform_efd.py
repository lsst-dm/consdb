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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml
from astropy.time import Time, TimeDelta
from lsst.consdb.transformed_efd.config_model import ConfigModel
from lsst.consdb.transformed_efd.dao.influxdb import InfluxDbDao
from lsst.consdb.transformed_efd.failure_monitor import FailureMonitor
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
            log.warning("event=logging_file_init_failed error=%s", e)

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
    req.add_argument(
        "-d",
        "--db",
        dest="db_conn_str",
        nargs="+",
        required=True,
        help=(
            "Database connection string(s). First URI is primary (production), "
            "additional URIs are secondary replicas."
        ),
    )
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
        help="Resume pending tasks in job mode",
    )
    opt.add_argument(
        "--failure-monitor",
        dest="failure_monitor",
        action="store_const",
        const=True,
        default=False,
        help="Run failure monitor checks (cronjob mode only)",
    )
    opt.add_argument(
        "--monitor-window-days",
        dest="monitor_window_days",
        type=int,
        default=7,
        help="Day_obs window size for Butler reconciliation checks",
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
    log.debug(
        "event=task_processing_start id=%s start_time=%s end_time=%s timewindow=%s retry=%s",
        task["id"],
        task["start_time"],
        task["end_time"],
        task["timewindow"],
        retry,
    )

    qm.dao.task_started(task["id"])
    if retry:
        qm.dao.task_retries_increment(task["id"])
    try:
        counts = tm.process_interval(
            instrument,
            _to_astropy_time(task["start_time"]) - TimeDelta(timewindow * 60, format="sec"),
            _to_astropy_time(task["end_time"]) + TimeDelta(timewindow * 60, format="sec"),
            task_context=task,
        )
        qm.dao.task_update_counts(task["id"], exposures=counts["exposures"], visits1=counts["visits1"])
        qm.dao.task_completed(task["id"])
        return counts
    except Exception as e:
        log.error("event=task_processing_failed id=%s error=%s", task["id"], e, exc_info=True)
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
    if args.resume:
        log.info("event=job_resume_idle_tasks")
        tasks = qm.waiting_tasks(args.repo, "idle", start_time, end_time)
    else:
        log.debug("event=job_create_tasks start_time=%s end_time=%s", start_time, end_time)
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


async def handle_cronjob(
    qm: QueueManager, tm: Transform, log: logging.Logger, args: argparse.Namespace
) -> list[dict]:
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
    if args.failure_monitor:
        log.debug("event=failure_monitor_run_start")
        monitor = FailureMonitor(
            qm,
            db_uri=args.db_conn_str,
            instrument=args.instrument,
            butler_dao=tm.butler_dao,
            log=log,
        )
        return monitor.run(args)

    else:
        log.debug("event=cronjob_check_pending_tasks")
        tasks = qm.recent_tasks_to_run(margin_seconds=-300)
        waiting_tasks = qm.waiting_tasks(args.repo, "pending")

        if not tasks and not waiting_tasks:
            log.debug("event=cronjob_create_periodic_tasks")
            qm.create_tasks(
                start_time=None,
                end_time=None,
                process_interval=int(args.timedelta),
                time_window=int(args.timewindow),
                butler_repo=args.repo,
            )
            tasks = qm.recent_tasks_to_run(margin_seconds=-300)

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
            log.warning("event=graceful_shutdown_between_batches")
            break

        batch = tasks[i : i + batch_size]
        log.debug(
            "event=task_batch_processing batch=%s total_batches=%s batch_size=%s",
            i // batch_size + 1,
            (len(tasks) - 1) // batch_size + 1,
            len(batch),
        )

        for task in batch:
            await asyncio.sleep(0)  # Yield control to event loop
            counts = await _process_task(task, qm, tm, log, instrument, timewindow, task.get("retry", False))
            totals["tasks"] += 1
            totals["exposures"] += counts["exposures"]
            totals["visits1"] += counts["visits1"]

            # Check between tasks
            if shutdown_event and shutdown_event.is_set():
                log.warning("event=graceful_shutdown_between_tasks")
                break  # Exit task loop

        if shutdown_event.is_set():
            break  # Exit batch loop

    log.info(
        "event=task_processing_summary tasks=%s exposures=%s visits=%s",
        totals["tasks"],
        totals["exposures"],
        totals["visits1"],
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
        log.warning("event=shutdown_signal_received action=finish_current_task_or_batch")

    # Set up signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _signal_handler)

    try:
        log.info(
            "event=execution_config mode=%s instrument=%s repo=%s timedelta_min=%s timewindow_min=%s "
            "resume=%s failure_monitor=%s monitor_window_days=%s",
            args.mode,
            args.instrument,
            args.repo,
            args.timedelta,
            args.timewindow,
            args.resume,
            args.failure_monitor,
            args.monitor_window_days,
        )

        if args.mode == "cronjob" and args.resume:
            raise ValueError("--resume is only supported with --mode job")
        if args.mode == "job" and args.failure_monitor:
            raise ValueError("--failure-monitor is only supported with --mode cronjob")

        # Initialize core components
        butler = Butler(args.repo)
        efd = InfluxDbDao(args.efd_conn_str, logger=log, max_fields_per_query=100)

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
            db_uri=args.db_conn_str, instrument=args.instrument, schema="efd_scheduler", logger=log
        )

        log.debug("event=components_initialized")

        safe_uris = [uri.split("@")[-1] if "@" in uri else uri for uri in args.db_conn_str]
        safe_primary = safe_uris[0]
        safe_secondaries = safe_uris[1:]
        log.info(
            "event=db_targets_configured db_count=%s primary=...@%s secondaries=%s",
            len(args.db_conn_str),
            safe_primary,
            safe_secondaries,
        )

        # Cleanup orphaned tasks
        fixed = qm.dao.fail_orphaned_tasks()
        if fixed:
            log.info("event=orphaned_tasks_marked_failed count=%s", fixed)

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
        if args.mode == "job":
            tasks = await handle_job(qm, log, args, **time_params)
        else:
            tasks = await handle_cronjob(qm, tm, log, args)

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
        log.warning("event=shutdown_completed")
    except ValueError as e:
        log.error("event=configuration_error error=%s", e)
        exit_code = 1
    except Exception as e:
        log.error("event=processing_failed error=%s", e, exc_info=True)
        exit_code = 1
    finally:
        log.info("event=runtime duration=%s", datetime.now(timezone.utc).replace(tzinfo=None) - exec_start)
        sys.exit(exit_code)


if __name__ == "__main__":
    """Execute main coroutine."""
    asyncio.run(main())
