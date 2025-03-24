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

from datetime import datetime, timezone
from typing import Dict, List, Optional, TypedDict

import pandas
from lsst.consdb.transformed_efd.dao.base import DBBase
from sqlalchemy import desc
from sqlalchemy.sql import and_, select


class Task(TypedDict):
    """Typed dictionary representing a task record."""

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
    """Data Access Object (DAO) for managing the "transformed_efd_scheduler" table.

    This class facilitates querying records, bulk inserts, and task management
    operations, such as updating statuses and execution counts.
    """

    def __init__(self, db_uri: str, schema: str):
        """Initialize the TransformdDao instance.

        Args:
        ----
        db_uri (str): The database URI for connecting to the database.
        schema (str): The schema name in the database.
        """
        super().__init__(db_uri, schema)
        self.tbl = self.get_table("transformed_efd_scheduler", schema=schema)

    def _update_task_status(self, id: int, status: str, **kwargs) -> None:
        """Helper method to update task status and related fields.

        Args:
        ----
            id (int): The ID of the task to update.
            status (str): The new status of the task.
            **kwargs: Additional fields to update.

        Raises:
        ------
            Exception: If there is an error updating the task.
        """
        try:
            self.update(id, {"status": status, **kwargs})
        except Exception as e:
            raise Exception(f"Error updating task to {status} status: {e}")

    def select_by_id(self, id: int) -> Task:
        """Select record from the table by its ID.

        Args:
        ----
            id (int): The ID of the record to select.

        Returns:
        -------
            Task: A dictionary representing the selected record.
        """
        stm = select(self.tbl.c).where(and_(self.tbl.c.id == id))
        return self.fetch_one_dict(stm)

    def count(self) -> int:
        """Return count of rows in the "transformd" table.

        Returns
        -------
            int: The count of rows in the table.
        """
        return self.execute_count(self.tbl)

    def bulk_insert(self, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """Insert data from a pandas DataFrame into the database table in bulk.

        Args:
        ----
        df (pandas.DataFrame): The DataFrame containing the data to be inserted.
        commit_every (int, optional): The number of rows to insert before
            committing the transaction. Defaults to 100.

        Returns:
        -------
            int: The number of affected rows.
        """
        return self.execute_bulk_insert(tbl=self.tbl, df=df, commit_every=commit_every)

    def insert(self, data: Dict) -> Task:
        """Insert row into the "transformd" table.

        Args:
        ----
            data (dict): The data to insert.

        Returns:
        -------
            Task: The inserted row.
        """
        stm = self.tbl.insert().values(**data)
        engine = self.get_db_engine()
        with engine.connect() as con:
            result = con.execute(stm)
            con.commit()
            id = result.inserted_primary_key[0]
            return self.select_by_id(id)

    def update(self, id: int, data: Dict) -> int:
        """Update row in the "transformd" table based on the ID.

        Args:
        ----
            id (int): The ID of the row to update.
            data (dict): The data to update.

        Returns:
        -------
            int: The number of affected rows.
        """
        stm = self.tbl.update().where(self.tbl.c.id == id).values(**data)
        engine = self.get_db_engine()
        with engine.connect() as con:
            result = con.execute(stm)
            con.commit()
            return result.rowcount

    def task_started(self, id: int) -> None:
        """Update status of a task to 'running' and sets the process start time."""
        self._update_task_status(
            id,
            "running",
            process_start_time=datetime.now(timezone.utc).replace(tzinfo=timezone.utc),
            process_end_time=None,
            process_exec_time=0,
            exposures=0,
            visits1=0,
            error=None,
        )

    def task_update_counts(self, id: int, exposures: int, visits1: int) -> None:
        """Update task counts for a given task ID, exposures, and visits.

        Args:
        ----
            id (int): The ID of the task to update.
            exposures (int): The number of exposures to set for the task.
            visits1 (int): The number of visits to set for the task.
        """
        self._update_task_status(id, "failed", exposures=exposures, visits1=visits1)

    def task_completed(self, id: int) -> None:
        """Mark task as completed by updating its status and execution time."""
        row = self.select_by_id(id)
        process_start_time = row["process_start_time"].replace(tzinfo=timezone.utc)
        process_end_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        exec_time = process_end_time - process_start_time

        self._update_task_status(
            id,
            "completed",
            process_end_time=process_end_time,
            process_exec_time=exec_time.total_seconds(),
            error=None,
        )

    def task_failed(self, id: int, error: str) -> None:
        """Mark task as failed in the database and updates relevant fields."""
        row = self.select_by_id(id)
        process_start_time = row["process_start_time"].replace(tzinfo=timezone.utc)
        process_end_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        exec_time = process_end_time - process_start_time

        self._update_task_status(
            id,
            "failed",
            process_end_time=process_end_time,
            process_exec_time=exec_time.total_seconds(),
            error=error,
        )

    def task_retries_increment(self, id: int) -> None:
        """Increment the retry count for a task identified by its ID.

        Args:
        ----
            id (int): The ID of the task to increment the retry count for.

        Raises:
        ------
            Exception: If there is an error updating the task retries.
        """
        row = self.select_by_id(id)
        retries = row["retries"] + 1
        self.update(id, {"retries": retries})

    def select_next(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> Task:
        """Select the next pending record within the specified time range.

        Args:
        ----
            start_time (Optional[datetime]): The start time to filter records.
                Defaults to None.
            end_time (Optional[datetime]): The end time to filter records.
                Defaults to None.

        Returns:
        -------
            Task: A dictionary representing the next pending record that
                matches the criteria.
        """
        query = select(self.tbl.c).where(self.tbl.c.status == "pending")
        if start_time is not None:
            query = query.where(self.tbl.c.start_time >= start_time)
        if end_time is not None:
            query = query.where(self.tbl.c.end_time <= end_time)
        query = query.order_by(self.tbl.c.start_time).limit(1)
        return self.fetch_one_dict(query)

    def select_last(self) -> Task:
        """Select last record from the table based on the 'end_time' column.

        Returns
        -------
            Task: A dictionary representing the last record in the table.
        """
        stm = select(self.tbl.c).order_by(desc(self.tbl.c.end_time)).limit(1)
        return self.fetch_one_dict(stm)

    def select_recent(self, end_time: datetime, limit: Optional[int] = None) -> List[Task]:
        """Select recent records.

        Args:
        ----
            end_time (datetime): The end time threshold for selecting records.
            limit (Optional[int], optional): The maximum number of records to
                return. Defaults to None.

        Returns:
        -------
            List[Task]: A list of dictionaries representing the selected
                records.
        """
        query = (
            select(self.tbl.c)
            .where(and_(self.tbl.c.status == "pending", self.tbl.c.end_time <= end_time))
            .order_by(desc(self.tbl.c.end_time))
        )
        if limit is not None:
            query = query.limit(limit)
        return self.fetch_all_dict(query)

    def select_queued(self, butler_repo: str, status: str) -> List[Task]:
        """Select task created but queued.

        Args:
        ----
            butler_repo (str): The bulter repository relative to the task
            status (str): The status (pending/idle).


        Returns:
        -------
            Task: A dictionary representing the next pending record that
                matches the criteria.
        """
        query = select(self.tbl.c).where(
            and_(self.tbl.c.status == status, self.tbl.c.butler_repo == butler_repo)
        )
        return self.fetch_all_dict(query)

    def select_failed(self, butler_repo: str, max_retries: Optional[int] = None) -> List[Task]:
        """Select failed tasks

        Args:
        ----
            butler_repo (str): The bulter repository relative to the task
            max_retries (Optional[int]): Maximum retries of failed task

        Returns:
        -------
            Task: A dictionary representing the next pending record that
                matches the criteria.
        """
        if max_retries:
            query = select(self.tbl.c).where(
                and_(
                    self.tbl.c.status == "failed",
                    self.tbl.c.retries <= max_retries,
                    self.tbl.c.butler_repo == butler_repo,
                )
            )
        else:
            query = select(self.tbl.c).where(self.tbl.c.status == "failed")

        return self.fetch_all_dict(query)

    def get_task_by_interval(
        self, start_time: datetime, end_time: datetime, butler_repo: str, status: str
    ) -> Task:
        """Check if there is an existing task within the specified time range.

        Args:
        ----
            start_time (datetime): The start time to filter records.
            end_time (datetime): The end time to filter records.
            butler_repo (str): The butler repository to filter records.
            status (str): The status to filter records.

        Returns:
        -------
            Task: A dictionary representing the existing task that matches the criteria.
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
