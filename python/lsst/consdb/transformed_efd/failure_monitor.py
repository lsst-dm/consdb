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

"""Failure monitor pipeline for transformed EFD cronjobs."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Tuple

from astropy.time import Time
from lsst.consdb.transformed_efd.dao.butler import ButlerDao
from lsst.consdb.transformed_efd.dao.exposure_efd import ExposureEfdDao
from lsst.consdb.transformed_efd.dao.visit_efd import VisitEfdDao
from lsst.consdb.transformed_efd.queue_manager import QueueManager


def _schema_by_instrument(instrument: str) -> str:
    schemas = {
        "latiss": "efd_latiss",
        "lsstcomcam": "efd_lsstcomcam",
        "lsstcomcamsim": "efd_lsstcomcamsim",
        "lsstcam": "efd_lsstcam",
    }
    return schemas[instrument.lower()]


def _butler_instrument(instrument: str) -> str:
    instruments = {
        "latiss": "LATISS",
        "lsstcomcam": "LSSTComCam",
        "lsstcomcamsim": "LSSTComCamSim",
        "lsstcam": "LSSTCam",
    }
    return instruments[instrument.lower()]


def _to_astropy_time(value: Any) -> Time:
    if isinstance(value, Time):
        return value.utc if value.scale != "utc" else value
    if hasattr(value, "utc"):
        return value.utc
    if isinstance(value, datetime):
        dt = value.astimezone(timezone.utc).replace(tzinfo=None) if value.tzinfo else value
        return Time(dt.isoformat(), format="isot", scale="utc")
    return Time(value, scale="utc")


def _merged_intervals(intervals: Iterable[Tuple[int, Time, Time]]) -> List[Tuple[int, Time, Time]]:
    ordered = sorted(intervals, key=lambda item: (item[0], item[1].unix))
    if not ordered:
        return []

    merged: List[Tuple[int, Time, Time]] = [ordered[0]]
    for day_obs, start, end in ordered[1:]:
        last_day_obs, last_start, last_end = merged[-1]
        if day_obs == last_day_obs and start.unix <= last_end.unix:
            merged[-1] = (
                last_day_obs,
                last_start,
                Time(max(last_end.unix, end.unix), format="unix", scale="utc"),
            )
        else:
            merged.append((day_obs, start, end))
    return merged


def _intervals_from_sequential_records(records: List[Dict[str, Any]]) -> List[Tuple[int, Time, Time]]:
    """Build intervals from contiguous records by day_obs/seq_num."""
    ordered = sorted(records, key=lambda rec: (rec.get("day_obs", 0), rec.get("seq_num", 0)))
    intervals: List[Tuple[int, Time, Time]] = []

    current_day_obs: Any = None
    previous_seq: int | None = None
    current_start: Time | None = None
    current_end: Time | None = None

    def _flush() -> None:
        if (
            current_day_obs is not None
            and current_start is not None
            and current_end is not None
            and current_end.unix > current_start.unix
        ):
            intervals.append((int(current_day_obs), current_start, current_end))

    for record in ordered:
        timespan = record.get("timespan")
        begin = getattr(timespan, "begin", None) if timespan is not None else None
        end = getattr(timespan, "end", None) if timespan is not None else None
        day_obs = record.get("day_obs")
        seq_num = record.get("seq_num")
        if begin is None or end is None or day_obs is None or seq_num is None:
            continue

        start_time = _to_astropy_time(begin)
        end_time = _to_astropy_time(end)
        if end_time.unix <= start_time.unix:
            continue

        is_contiguous = (
            current_start is not None
            and current_end is not None
            and day_obs == current_day_obs
            and previous_seq is not None
            and int(seq_num) == previous_seq + 1
        )

        if is_contiguous:
            current_end = Time(max(current_end.unix, end_time.unix), format="unix", scale="utc")
        else:
            _flush()
            current_start = start_time
            current_end = end_time
            current_day_obs = day_obs

        previous_seq = int(seq_num)

    _flush()
    return intervals


def _day_obs_window(window_days: int) -> Tuple[int, int]:
    now = datetime.now(timezone.utc).date()
    start = now - timedelta(days=window_days - 1)
    return int(start.strftime("%Y%m%d")), int(now.strftime("%Y%m%d"))


class FailedTaskRetryCheck:
    """Select failed tasks eligible for retry."""

    def run(
        self,
        qm: QueueManager,
        repo: str,
        log: logging.Logger,
        base_hour: float = 2.82843,
        max_retries: int = 3,
        max_age_hours: float = 72.0,
    ) -> List[Dict[str, Any]]:
        tasks = qm.failed_tasks(repo, max_retries=max_retries)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        max_age = timedelta(hours=max_age_hours)
        selected: List[Dict[str, Any]] = []

        for task in tasks:
            retries = task["retries"]
            created = task["created_at"]
            if created.tzinfo:
                created = created.astimezone(timezone.utc).replace(tzinfo=None)

            since_created = now - created
            next_wait = timedelta(hours=base_hour ** (retries + 1))
            if next_wait < since_created < max_age:
                selected.append(task)
                log.debug(
                    f"Task {task['id']} retryable: created_at={task['created_at']} elapsed={since_created}"
                    f" required_wait={next_wait}"
                )
            elif since_created >= max_age:
                log.debug(
                    f"Task {task['id']} stale: created_at={task['created_at']} elapsed={since_created}"
                    f" required_wait={next_wait}"
                )
                qm._mark_task_stale(task["id"])

        return selected


class ButlerReconciliationCheck:
    """Create scheduler tasks for missing Butler exposures/visits."""

    def __init__(
        self,
        qm: QueueManager,
        db_uri: str | list[str],
        instrument: str,
        butler_dao: ButlerDao,
        log: logging.Logger,
    ):
        self.qm = qm
        self.db_uri = db_uri
        self.instrument = instrument
        self.butler_dao = butler_dao
        self.log = log
        self.schema = _schema_by_instrument(instrument)
        self.butler_instrument = _butler_instrument(instrument)

    def run(self, args: Any) -> List[Dict[str, Any]]:
        window_days = max(1, int(getattr(args, "monitor_window_days", 7)))
        process_interval = max(1, int(getattr(args, "timedelta", 5)))
        # Keep the configured overlap, but cap at 5 for monitor-created tasks.
        time_window = min(5, max(1, int(getattr(args, "timewindow", 1))))
        day_start, day_end = _day_obs_window(window_days)

        exp_records = self.butler_dao.exposures_by_day_obs(self.butler_instrument, day_start, day_end)
        vis_records = self.butler_dao.visits_by_day_obs(self.butler_instrument, day_start, day_end)

        exp_dao = ExposureEfdDao(self.db_uri, self.schema, self.log)
        vis_dao = VisitEfdDao(self.db_uri, self.schema, self.log)

        existing_exp_ids = exp_dao.select_ids_by_day_obs(day_start, day_end)
        existing_vis_ids = vis_dao.select_ids_by_day_obs(day_start, day_end)

        missing_exp = [record for record in exp_records if record["id"] not in existing_exp_ids]
        missing_vis = [record for record in vis_records if record["id"] not in existing_vis_ids]

        self.log.debug(
            "Butler reconciliation window: "
            f"day_obs_start={day_start} day_obs_end={day_end} "
            f"missing_exposures={len(missing_exp)} missing_visits={len(missing_vis)}"
        )

        exp_intervals = _intervals_from_sequential_records(missing_exp)
        vis_intervals = _intervals_from_sequential_records(missing_vis)
        merged = _merged_intervals(exp_intervals + vis_intervals)
        created_tasks: List[Dict[str, Any]] = []
        for _day_obs, start_time, end_time in merged:
            created_tasks.extend(
                self.qm.create_tasks(
                    start_time=start_time,
                    end_time=end_time,
                    process_interval=process_interval,
                    time_window=time_window,
                    status="idle",
                    butler_repo=args.repo,
                )
            )

        self.log.debug(
            "Butler reconciliation result: "
            f"exposure_intervals={len(exp_intervals)} visit_intervals={len(vis_intervals)} "
            f"intervals_merged={len(merged)} tasks_created={len(created_tasks)}"
        )
        return created_tasks


class FailureMonitor:
    """Orchestrate monitor checks and return tasks to execute."""

    def __init__(
        self,
        qm: QueueManager,
        db_uri: str | list[str],
        instrument: str,
        butler_dao: ButlerDao,
        log: logging.Logger,
    ):
        self.qm = qm
        self.db_uri = db_uri
        self.instrument = instrument
        self.butler_dao = butler_dao
        self.log = log
        self.retry_check = FailedTaskRetryCheck()
        self.reconciliation_check = ButlerReconciliationCheck(
            qm=qm,
            db_uri=db_uri,
            instrument=instrument,
            butler_dao=butler_dao,
            log=log,
        )

    def run(self, args: Any) -> List[Dict[str, Any]]:
        retry_tasks = self.retry_check.run(self.qm, args.repo, self.log)
        reconciled_tasks = self.reconciliation_check.run(args)
        tasks = retry_tasks + reconciled_tasks

        dedup: Dict[Any, Dict[str, Any]] = {}
        for task in tasks:
            task_id = task.get("id")
            if task_id is None:
                continue
            dedup[task_id] = task

        ordered = sorted(dedup.values(), key=lambda task: task["id"])
        self.log.debug(
            f"Failure monitor selected tasks: retry={len(retry_tasks)} "
            f"created={len(reconciled_tasks)} total={len(ordered)}"
        )
        return ordered
