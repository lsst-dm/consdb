import argparse
import asyncio
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import astropy.time

# import lsst_efd_client
import yaml
from config_model import ConfigModel
from dao.influxdb import InfluxDbDao
from lsst.daf.butler import Butler
from pydantic import ValidationError
from queue_manager import QueueManager
from transform import Transform

# from sqlalchemy import create_engine


def get_logger(path: str, debug: bool = True) -> logging.Logger:
    """
    Create and configure a logger object.

    Args:
        path (str): The path to the log file.
        debug (bool, optional): Flag indicating whether to enable debug mode.
        Defaults to True.

    Returns:
        logging.Logger: The configured logger object.
    """
    # File Handler
    logfile = Path(path)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)

    # Stdout handler
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
    """
    Build the argument parser for the script.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="Summarize EFD topics in a time range")
    parser.add_argument("-c", "--config", dest="config_name", required=True, help="config YAML")
    parser.add_argument(
        "-i",
        "--instrument",
        dest="instrument",
        required=True,
        help="instrument name",
    )
    parser.add_argument(
        "-s",
        "--start",
        dest="start_time",
        required=False,
        help="start time (ISO, YYYY-MM-DDTHH:MM:SS)",
    )
    parser.add_argument(
        "-e",
        "--end",
        dest="end_time",
        required=False,
        help="end time (ISO, YYYY-MM-DDTHH:MM:SS)",
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
        "-d",
        "--db",
        dest="db_conn_str",
        # default="sqlite://test.db",
        required=True,
        help="Consolidated Database connection string",
    )
    parser.add_argument(
        "-E",
        "--efd",
        dest="efd_conn_str",
        # default="usdf_efd",
        required=True,
        help="EFD connection string",
    )
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
        help="Processing overlaping time window in minutes",
    )
    parser.add_argument(
        "-l",
        "--logfile",
        dest="logfile",
        default="transform.log",
        help="Log file",
    )

    return parser


def read_config(config_name: str) -> Dict[str, Any]:
    """
    Reads a configuration file and returns the configuration as a dictionary.

    Args:
        config_name (str): The name of the configuration file.

    Returns:
        dict: The configuration as a dictionary.

    Raises:
        ValidationError: If the configuration file is invalid.

    """
    try:
        with open(config_name, "r") as file:
            data = yaml.safe_load(file)
            config = ConfigModel(**data)

            return config.model_dump()

    except ValidationError as e:
        raise e


async def main() -> None:
    """
    Entry point of the program.

    This function performs the main logic of the program, including parsing
    command line arguments, setting up logging, creating necessary objects,
    and processing the specified time interval.
    """
    t0 = datetime.now()
    parser = build_argparser()

    args = parser.parse_args()

    log = get_logger(args.logfile)

    # TODO: Remove this or make it optional
    log.debug("==============================================================")
    log.debug("Testing postgres connection")
    # ConsDB DB URI
    consdb_url = args.db_conn_str
    try:
        from dao.base import DBBase
        from dao.exposure_efd import ExposureEfdDao
        from dao.visit_efd import VisitEfdDao

        consdb = DBBase(consdb_url)
        log.debug(f"ConsDB engine: {consdb.get_db_engine()}")
        log.debug(f"ConsDB connection: {consdb.get_con()}")
        log.debug("Postgres connection successful")

        log.debug("Testing table exposure_efd")
        expdao = ExposureEfdDao(consdb_url, "cdb_latiss")
        log.debug(f"exposure_efd table: {expdao.tbl}")

        log.debug("Testing table visit1_efd")
        visdao = VisitEfdDao(consdb_url, "cdb_latiss")
        log.debug(f"visit1_efd table: {visdao.tbl}")
    except Exception as e:
        log.error(f"Postgres connection failed: {e}")
        sys.exit(1)
    log.debug("==============================================================")

    # Instantiate the butler
    butler = Butler(args.repo)
    log.debug(f"Butler: {butler}")

    # Instantiate the EFD
    efd = InfluxDbDao(args.efd_conn_str)
    log.debug(f"EFD: {efd}")

    config = read_config(args.config_name)
    log.debug(f"Configs Columns: {len(config['columns'])}")

    # TODO: Commit every can be a enviroment variable
    commit_every = 100

    # Instantiate the main class transform
    tm = Transform(
        butler=butler, db_uri=consdb_url, efd=efd, config=config, logger=log, commit_every=commit_every
    )

    # Instantiate the queue manager
    qm = QueueManager(db_uri=consdb_url, logger=log)

    start_time = None
    if args.start_time is not None:
        start_time = datetime.fromisoformat(args.start_time)
        start_time = astropy.time.Time(start_time.isoformat(), format="isot", scale="utc")

    end_time = None
    if args.end_time is not None:
        end_time = datetime.fromisoformat(args.end_time)
        end_time = astropy.time.Time(end_time.isoformat(), format="isot", scale="utc")

    # Run the transform script with fixed interval
    # TODO: Translate this
    # Execution for a specific period or reprocessing.
    # creates new tasks and executes only the created tasks.
    # Does not consider existing tasks as pending.
    if start_time is not None and end_time is not None:
        log.info("Running the transform script with fixed interval")
        tasks = qm.create_tasks(
            start_time=start_time,
            end_time=end_time,
            process_interval=int(args.timedelta),
            time_window=int(args.timewindow),
        )

    else:
        log.info("Running the transform script with periodic interval")
        # Periodic cronjob execution.
        # Check the most recent pending tasks (end_time desc)
        # If it does not find any, it will create new tasks using the
        # last execution.
        tasks = qm.recent_tasks_to_run()

        if len(tasks) == 0:
            log.debug("No tasks found.")
            # The created tasks cannot be executed now because the end_time is
            # greater than the current time (now + time window).
            # In the next iteration they will be executed
            qm.create_tasks(
                process_interval=int(args.timedelta),
                time_window=int(args.timewindow),
            )

            # All tasks with pending status ordered by end time desc
            # As long as end_time is less than the current time
            tasks = qm.recent_tasks_to_run()

    count_task = 0
    # Count exposures and visits1 includind overlaps between tasks
    count_exposures = 0
    count_visits1 = 0

    # TODO: Perhaps it would be interesting to test the end_time of each task
    # and if it is less than now, create a new task until it reaches
    # the current time.
    for task in tasks:
        log.info("----------------------------------------------------------")
        log.info(f"Next Task: ID: {task['id']}")
        log.info(
            f"Current Time: {datetime.now(tz=timezone.utc).replace(tzinfo=None).isoformat(timespec='seconds')}"
        )
        log.info(
            f"Task Start: {task['start_time']} End: {task['end_time']} = {task['end_time'] - task['start_time']}"
        )

        qm.dao.task_started(task["id"])
        try:
            process_count = tm.process_interval(
                args.instrument,
                start_time=astropy.time.Time(task["start_time"].isoformat(), format="isot", scale="utc"),
                end_time=astropy.time.Time(task["end_time"].isoformat(), format="isot", scale="utc"),
            )

            count_exposures += process_count["exposures"]
            count_visits1 += process_count["visits1"]

            qm.dao.task_update_counts(
                task["id"], exposures=process_count["exposures"], visits1=process_count["visits1"]
            )

            qm.dao.task_completed(task["id"])

        except Exception as e:
            log.error(f"Error processing task: {e}")
            qm.dao.task_failed(task["id"], error=str(e))
        count_task += 1

    log.info("======================================")
    log.info(f"Total Tasks: {count_task}")
    log.info(f"Processed Exposures: {count_exposures} (including overlaps)")
    log.info(f"Processed Visits1: {count_visits1} (including overlaps)")
    t1 = datetime.now()
    dt = t1 - t0
    log.info(f"Total time: {dt}")
    log.info("End of processing")
    sys.exit(0)


if __name__ == "__main__":

    # Execution example
    # python python/lsst/consdb/transform_efd.py \
    #     -i LATISS \
    #     -s 2024-04-25T00:00:00  \
    #     -e 2024-04-30T23:59:59 \
    #     -r /repo/embargo \
    #     -d sqlite:///$PWD/.tmp/test.db \
    #     -E usdf_efd \
    #     -c $PWD/.tmp/config.yaml \
    #     -l $PWD/.tmp/transform.log
    asyncio.run(main())
