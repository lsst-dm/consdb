import argparse
import asyncio
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

import astropy.time

# import lsst_efd_client
import yaml
from config_model import ConfigModel
from dao.influxdb import InfluxDbDao
from lsst.daf.butler import Butler
from pydantic import ValidationError
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
    parser = build_argparser()

    args = parser.parse_args()

    log = get_logger(args.logfile)

    # defining the start and end time
    # TODO: Should I use UTC???
    # now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    now = datetime.now().replace(second=0, microsecond=0)

    if args.start_time is None:
        start_time = now - timedelta(minutes=int(args.timedelta))
    else:
        start_time = datetime.fromisoformat(args.start_time)

    if args.end_time is None:
        end_time = now
    else:
        end_time = datetime.fromisoformat(args.end_time)

    start_time = astropy.time.Time(start_time.isoformat(), format="isot")
    end_time = astropy.time.Time(end_time.isoformat(), format="isot")

    # Instantiate the butler
    butler = Butler(args.repo)

    # Instantiate the EFD
    db_uri = args.db_conn_str
    efd = InfluxDbDao(args.efd_conn_str)

    config = read_config(args.config_name)

    # TODO: Commit every can be a enviroment variable
    commit_every = 100

    # Instantiate the main class transform
    tm = Transform(
        butler=butler, db_uri=db_uri, efd=efd, config=config, logger=log, commit_every=commit_every
    )
    tm.process_interval(
        args.instrument,
        start_time,
        end_time,
    )


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
