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

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, TypedDict

import numpy
import pandas
from lsst.consdb.transformed_efd.dao.base import DBBase
from sqlalchemy import desc
from sqlalchemy.sql import and_, or_, select


class Task(TypedDict):
    """Task record dictionary."""

    id: int
    status: str
    start_time: datetime
    end_time: datetime
    process_start_time: Optional[datetime]
    process_end_time: Optional[datetime]
    process_exec_time: float
    exposures: int
    visits1: int
    retries: int
    error: Optional[str]
    butler_repo: Optional[str]


class TransformdDao(DBBase):
    """DAO for transformed_efd_scheduler table operations."""

    def __init__(self, db_uri: str, instrument: str, schema: str, logger: logging.Logger = None) -> None:
        """Initialize DAO.

        Parameters
        ----------
        db_uri : str
            Database connection URI
        instrument : str
            Instrument name
        schema : str
            Database schema name
        logger : logging.Logger, optional
            Logger instance for logging (default: None)
        """
        super().__init__(db_uri, schema, logger)
        self.tbl = self.get_table(instrument, schema=schema)

    def _update_task_status(self, id: int, status: str, **kwargs) -> None:
        """Update task status and fields.

        Parameters
        ----------
        id : int
            Task ID to update
        status : str
            New status value
        **kwargs
            Additional fields to update
        """
        try:
            self.update(id, {"status": status, **kwargs})
        except Exception as e:
            self.log.error(f"Task update failed: id={id} status={status} error={e}", exc_info=True)
            raise Exception(f"Error updating task: error={e}") from e

    @staticmethod
    def _ensure_utc_naive(dt: Optional[datetime]) -> Optional[datetime]:
        """Convert datetime to UTC-naive format.

        Args:
            dt: Input datetime (naive or aware)

        Returns:
            UTC-naive datetime, or None if input was None
        """
        if dt is None:
            return None
        if dt.tzinfo is not None:
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt  # Assume naive datetimes are UTC

    def select_by_id(self, id: int) -> Task:
        """Get task by ID.

        Parameters
        ----------
        id : int
            Task ID to retrieve

        Returns
        -------
        Task
            Task record dictionary
        """
        stm = select(self.tbl.c).where(self.tbl.c.id == id)
        return self.fetch_one_dict(stm)

    def count(self) -> int:
        """Count rows in table.

        Returns
        -------
        int
            Number of rows
        """
        return self.execute_count(self.tbl)

    def bulk_insert(self, df: pandas.DataFrame, commit_every: int = 100) -> List[Dict]:
        """Bulk insert DataFrame and return the inserted task records.

        Parameters
        ----------
        df : pandas.DataFrame
            Data to insert
        commit_every : int, optional
            Commit interval (default: 100)

        Returns
        -------
        List[Dict]
            A list of dicts representing the inserted tasks.
        """
        df = df.replace(numpy.nan, None)
        records = df.to_dict("records")

        inserted_tasks = []
        engine = self.get_db_engine()

        for i in range(0, len(records), commit_every):
            chunk = records[i : i + commit_every]
            insert_stm = self.dialect.insert(self.tbl).values(chunk).returning(self.tbl)

            with engine.connect() as con:
                result = con.execute(insert_stm)
                rows = result.fetchall()  # ✅ Must be BEFORE commit
                con.commit()

            pk_names = [col.name for col in self.tbl.primary_key.columns]

            for row in rows:
                task_dict = dict(row._mapping)
                inserted_tasks.append(task_dict)
                pk_values = {k: task_dict[k] for k in pk_names}
                self.log.info(
                    f"event=row_inserted schema={self.tbl.schema} table={self.tbl.name} pk_values={pk_values}"
                )

        return inserted_tasks

    def insert(self, data: Dict) -> Task:
        """Insert new task.

        Parameters
        ----------
        data : Dict
            Task data to insert

        Returns
        -------
        Task
            Inserted task record
        """
        stm = self.tbl.insert().values(**data)
        with self.get_db_engine().connect() as con:
            result = con.execute(stm)
            con.commit()
            return self.select_by_id(result.inserted_primary_key[0])

    def update(self, id: int, data: Dict) -> int:
        """Update task by ID.

        Parameters
        ----------
        id : int
            Task ID to update
        data : Dict
            Fields to update

        Returns
        -------
        int
            Number of rows affected
        """
        stm = self.tbl.update().where(self.tbl.c.id == id).values(**data)
        with self.get_db_engine().connect() as con:
            result = con.execute(stm)
            con.commit()
            return result.rowcount

    def task_started(self, id: int) -> None:
        """Mark task as running.

        Parameters
        ----------
        id : int
            Task ID to update
        """
        self._update_task_status(
            id,
            "running",
            process_start_time=self._ensure_utc(datetime.now(timezone.utc)),
            process_end_time=None,
            process_exec_time=0,
            exposures=0,
            visits1=0,
            error=None,
        )

    def task_update_counts(self, id: int, exposures: int, visits1: int) -> None:
        """Update task counts.

        Parameters
        ----------
        id : int
            Task ID to update
        exposures : int
            Exposure count
        visits1 : int
            Visit count
        """
        self._update_task_status(id, "failed", exposures=exposures, visits1=visits1)

    def task_completed(self, id: int) -> None:
        """Mark task as completed.

        Parameters
        ----------
        id : int
            Task ID to update
        """
        row = self.select_by_id(id)
        end_time = self._ensure_utc(datetime.now(timezone.utc))
        exec_time = (end_time - row["process_start_time"]).total_seconds()
        self._update_task_status(
            id,
            "completed",
            process_end_time=end_time,
            process_exec_time=exec_time,
            error=None,
        )

    def task_failed(self, id: int, error: str) -> None:
        """Mark task as failed.

        Parameters
        ----------
        id : int
            Task ID to update
        error : str
            Error message
        """
        row = self.select_by_id(id)
        end_time = self._ensure_utc(datetime.now(timezone.utc))
        exec_time = (end_time - row["process_start_time"]).total_seconds()
        self._update_task_status(
            id,
            "failed",
            process_end_time=end_time,
            process_exec_time=exec_time,
            error=error,
        )

    def task_retries_increment(self, id: int) -> None:
        """Increment task retries.

        Parameters
        ----------
        id : int
            Task ID to update
        """
        row = self.select_by_id(id)
        self.update(id, {"retries": row["retries"] + 1})

    def select_next(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> Task:
        """Get next pending task in time range.

        Parameters
        ----------
        start_time : datetime, optional
            Minimum start time filter
        end_time : datetime, optional
            Maximum end time filter

        Returns
        -------
        Task
            Next pending task record
        """
        query = select(self.tbl.c).where(self.tbl.c.status == "pending")
        if start_time:
            query = query.where(self.tbl.c.start_time >= start_time)
        if end_time:
            query = query.where(self.tbl.c.end_time <= end_time)
        return self.fetch_one_dict(query.order_by(self.tbl.c.start_time).limit(1))

    def select_last(self) -> Task:
        """Get last task by end_time.

        Returns
        -------
        Task
            Most recent task record
        """
        stm = select(self.tbl.c).order_by(desc(self.tbl.c.end_time)).limit(1)
        return self.fetch_one_dict(stm)

    def select_recent(self, end_time: datetime, limit: Optional[int] = None) -> List[Task]:
        """Get recent pending tasks.

        Parameters
        ----------
        end_time : datetime
            Maximum end time filter
        limit : int, optional
            Maximum records to return

        Returns
        -------
        List[Task]
            List of task records
        """
        query = (
            select(self.tbl.c)
            .where(and_(self.tbl.c.status == "pending", self.tbl.c.end_time <= end_time))
            .order_by(desc(self.tbl.c.end_time))
        )
        if limit:
            query = query.limit(limit)
        return self.fetch_all_dict(query)

    def select_queued(self, butler_repo: str, status: str) -> List[Task]:
        """Get queued tasks by repo and status.

        Parameters
        ----------
        butler_repo : str
            Butler repository filter
        status : str
            Status filter ('pending' or 'idle')

        Returns
        -------
        List[Task]
            List of task records
        """
        query = select(self.tbl.c).where(
            and_(self.tbl.c.status == status, self.tbl.c.butler_repo == butler_repo)
        )
        return self.fetch_all_dict(query)

    def select_failed(self, butler_repo: str, max_retries: Optional[int] = None) -> List[Task]:
        """Get failed tasks with optional retry limit.

        Parameters
        ----------
        butler_repo : str
            Butler repository filter
        max_retries : int, optional
            Maximum retries filter

        Returns
        -------
        List[Task]
            List of task records
        """
        query = select(self.tbl.c).where(self.tbl.c.status == "failed")
        if max_retries:
            query = query.where(
                and_(self.tbl.c.retries <= max_retries, self.tbl.c.butler_repo == butler_repo)
            )
        return self.fetch_all_dict(query)

    def get_task_by_interval(
        self, start_time: datetime, end_time: datetime, butler_repo: str, status: str
    ) -> Task:
        """Get task by time interval, repo and status.

        Parameters
        ----------
        start_time : datetime
            Exact start time filter
        end_time : datetime
            Exact end time filter
        butler_repo : str
            Butler repository filter
        status : str
            Status filter

        Returns
        -------
        Task
            Matching task record
        """
        query = select(self.tbl.c).where(
            and_(
                self.tbl.c.start_time == start_time,
                self.tbl.c.end_time == end_time,
                self.tbl.c.butler_repo == butler_repo,
                self.tbl.c.status == status,
            )
        )
        return self.fetch_one_dict(query)

    def fail_orphaned_tasks(self) -> int:
        """Mark orphaned running tasks as failed.

        Returns
        -------
        int
            Number of tasks updated
        """
        query = (
            self.tbl.update()
            .where(
                and_(
                    self.tbl.c.status == "running",
                    or_(self.tbl.c.process_start_time.is_(None), self.tbl.c.process_end_time.is_(None)),
                )
            )
            .values(
                status="failed",
                error="Task interrupted",
                process_end_time=self._ensure_utc(datetime.now(timezone.utc)),
            )
        )
        with self.get_db_engine().connect() as con:
            result = con.execute(query)
            con.commit()
            return result.rowcount
