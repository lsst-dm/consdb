#!/usr/bin/env python3
"""Run daily ConsDB table consistency checks.

This script uses ``DB_HOST``, ``DB_PORT`` (optional), ``DB_PASS``, ``DB_USER``,
and ``DB_NAME`` to connect to PostgreSQL. Loki alerts should be configured from
the structured ``event=consdb_table_consistency_alert`` error logs emitted by
this script.
"""

import argparse
import datetime
import logging
import os
from collections import defaultdict
from collections.abc import Mapping

import sqlalchemy
from lsst.consdb.consistency_queries import CONSISTENCY_QUERIES
from sqlalchemy.engine import URL

LOG = logging.getLogger("lsst.consdb.daily_consistency_check")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run per-instrument ConsDB table consistency checks.")
    parser.add_argument(
        "day_obs",
        nargs="?",
        type=int,
        help=(
            "Observation day in YYYYMMDD format; defaults to the DAY_OBS "
            "environment variable, or yesterday's UTC date if DAY_OBS is not set."
        ),
    )
    args = parser.parse_args()
    if args.day_obs is None:
        args.day_obs = default_day_obs()
    return args


def default_day_obs() -> int:
    day_obs = os.environ.get("DAY_OBS")
    if day_obs is not None:
        return int(day_obs)
    yesterday = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    return int(yesterday.strftime("%Y%m%d"))


def selected_instruments() -> list[str]:
    instruments = os.environ.get("INSTRUMENTS")
    if instruments is None:
        return list(CONSISTENCY_QUERIES.keys())

    selected = [instrument.strip().lower() for instrument in instruments.split(";") if instrument.strip()]
    invalid = [instrument for instrument in selected if instrument not in CONSISTENCY_QUERIES]
    if invalid:
        valid = ", ".join(CONSISTENCY_QUERIES.keys())
        raise RuntimeError(f"Invalid INSTRUMENTS entries: {', '.join(invalid)}. Valid instruments: {valid}")

    return selected


def make_database_url() -> URL:
    missing = [name for name in ("DB_HOST", "DB_PASS", "DB_USER", "DB_NAME") if os.environ.get(name) is None]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return URL.create(
        "postgresql",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]) if os.environ.get("DB_PORT") else None,
        database=os.environ["DB_NAME"],
    )


def compress_seq_nums(seq_nums: list[int]) -> str:
    if not seq_nums:
        return ""

    ranges = []
    start = previous = seq_nums[0]
    for seq_num in seq_nums[1:]:
        if seq_num == previous:
            continue
        if seq_num == previous + 1:
            previous = seq_num
            continue
        ranges.append(format_seq_num_range(start, previous))
        start = previous = seq_num
    ranges.append(format_seq_num_range(start, previous))
    return ",".join(ranges)


def format_seq_num_range(start: int, end: int) -> str:
    if start == end:
        return str(start)
    return f"{start}-{end}"


def log_alert(instrument: str, day_obs: int, rows: list[Mapping[str, object]]) -> None:
    rule_seq_nums = defaultdict(list)
    for row in rows:
        rule_seq_nums[row["rule"]].append(int(row["seq_num"]))

    rule_messages = [
        f"{rule} failed for seq_num {compress_seq_nums(sorted(seq_nums))}"
        for rule, seq_nums in sorted(rule_seq_nums.items())
    ]
    LOG.error(
        "event=consdb_table_consistency_alert instrument=%s day_obs=%s num_inconsistencies=%s message=%r",
        instrument,
        day_obs,
        len(rows),
        "; ".join(rule_messages),
    )


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    args = parse_args()
    engine = sqlalchemy.create_engine(make_database_url())

    with engine.connect() as connection:
        for instrument in selected_instruments():
            query = CONSISTENCY_QUERIES[instrument]
            rows = list(
                connection.execute(
                    sqlalchemy.text(query),
                    {"day_obs": args.day_obs},
                ).mappings()
            )
            if not rows:
                LOG.info(
                    "event=consdb_table_consistency_ok instrument=%s day_obs=%s",
                    instrument,
                    args.day_obs,
                )
                continue

            log_alert(instrument, args.day_obs, rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
