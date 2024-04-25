import argparse
from typing import TYPE_CHECKING, Any, Callable

import astropy.time
import lsst_efd_client
import pandas
import yaml
from lsst.daf.butler import Butler, DimensionRecord
from sqlalchemy import create_engine, Engine


class Summary:
    # TODO define summary
    pass


# TODO add all summarizing functions
def gen_mean(
    config: dict[str, Any]
) -> Callable[[pandas.DataFrame, astropy.time.Time, astropy.time.Time], Summary]:
    def do(
        series: pandas.DataFrame, start: astropy.time.Time, end: astropy.time.Time
    ) -> Summary:
        return Summary()

    return do


FUNCTION_GENERATORS = dict(mean=gen_mean)


class EfdValues:
    def __init__(
        self,
        config: dict[str, Any],
        window: astropy.time.TimeDelta,
        series: pandas.DataFrame,
    ):
        self._entries = series
        self._sum_function = FUNCTION_GENERATORS[config["function"]](config)
        self._window = window

    def summarize(self, start: astropy.time.Time, end: astropy.time.Time) -> Any:
        return self._sum_function(
            self._entries, start - self._window, end + self._window
        )


class Records:
    def __init__(self, db: Engine):
        self._db = db

    def add(
        self, dim: DimensionRecord, topic: dict[str, Any], summary: Any
    ) -> None:
        pass

    def write(self, table: str) -> None:
        pass


def read_config(config_name: str) -> dict[str, Any]:
    with open(config_name, "r") as f:
        return yaml.safe_load(f)


def get_efd_values(
    efd: lsst_efd_client.EfdClient,
    topic: dict[str, Any],
    start: astropy.time.Time,
    end: astropy.time.Time,
) -> pandas.DataFrame:
    window = astropy.time.TimeDelta(topic.get("window", 0.0), format="sec")
    series = efd.select_time_series(
        topic["name"],
        topic["fields"],
        start - window,
        end + window,
        topic.get("index", None),
    )
    return EfdValues(topic, window, series)


def process_interval(
    butler: Butler,
    db: Engine,
    efd: lsst_efd_client.EfdClient,
    config: dict[str, Any],
    instrument: str,
    start_time: str,
    end_time: str,
) -> None:
    start = astropy.time.Time(start_time, format="isot")
    end = astropy.time.Time(end_time, format="isot")

    exposure_list = []
    visit_list = []
    min_topic_time = end
    max_topic_time = start

    where_clause = "instrument=instr and timespan OVERLAPS (start, end)"

    for e in butler.queryDimensionRecords(
        "exposure",
        where=where_clause,
        bind=dict(instr=instrument, start=start, end=end),
    ):
        if e.timespan.end < end:
            exposure_list.append(e)
            min_topic_time = min(e.timespan.begin, min_topic_time)
            max_topic_time = max(e.timespan.begin, max_topic_time)

    for v in butler.queryDimensionRecords(
        "visit", where=where_clause, bind=dict(instr=instrument, start=start, end=end)
    ):
        if v.timespan.end < end:
            visit_list.append(v)
            min_topic_time = min(v.timespan.begin, min_topic_time)
            max_topic_time = max(v.timespan.begin, max_topic_time)

    exposure_records = Records(db)
    visit_records = Records(db)
    for topic in config["topics"]:
        efd_values = get_efd_values(efd, topic, min_topic_time, max_topic_time)
        for e in exposure_list:
            summary = efd_values.summarize(e.timespan.begin, e.timespan.end)
            exposure_records.add(e, topic, summary)
        for v in visit_list:
            summary = efd_values.summarize(v.timespan.begin, v.timespan.end)
            visit_records.add(v, topic, summary)

    exposure_records.write(config["exposure_table"])
    visit_records.write(config["visit_table"])


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize EFD topics in a time range")
    parser.add_argument(
        "-c", "--config", dest="config_name", required=True, help="config YAML"
    )
    parser.add_argument(
        "-i", "--instrument", dest="instrument", required=True, help="instrument name"
    )
    parser.add_argument(
        "-s",
        "--start",
        dest="start_time",
        required=True,
        help="start time (ISO, YYYY-MM-DDTHH:MM:SS)",
    )
    parser.add_argument(
        "-e",
        "--end",
        dest="end_time",
        required=True,
        help="end time (ISO, YYYY-MM-DDTHH:MM:SS)",
    )
    parser.add_argument("-r", "--repo", dest="repo", default="/repo/embargo", required=True, help="Butler repo")
    parser.add_argument(
        "-d",
        "--db",
        dest="db_conn_str",
        default="sqlite://test.db",
        required=True,
        help="Consolidated Database connection string",
    )
    parser.add_argument(
        "-E", "--efd", dest="efd_conn_str", default="usdf_efd", required=True, help="EFD connection string"
    )
    return parser


def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    butler = Butler(args.repo)
    db = create_engine(args.db_conn_str)
    efd = lsst_efd_client.EfdClient(args.efd_conn_str)
    config = read_config(args.config_name)
    process_interval(
        butler, db, efd, config, args.instrument, args.start_time, args.end_time
    )
