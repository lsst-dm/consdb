from datetime import datetime, timezone
from typing import Dict, Optional

import pandas
from dao.base import DBBase
from sqlalchemy import desc
from sqlalchemy.sql import and_, select


class TransformdDao(DBBase):

    def __init__(self, db_uri: str, schema: str):
        """
        Initialize the TransformdDao instance.

        Parameters:
        db_uri (str): The database URI for connecting to the database.

        Notes:
        - The schema is currently hardcoded as "cdb_latiss".
            This may be changed in the future to be passed as a parameter.
        - Awaiting changes from Rodrigo regarding the schema usage.
        """
        super(TransformdDao, self).__init__(db_uri, schema)

        # TODO utilizar o schema como parametro
        # aguardando alterações do rodrigo
        self.tbl = self.get_table("transformed_efd_scheduler", schema=schema)

    def select_by_id(self, id: int) -> Dict:
        """
        Select a record from the table by its ID.

        Args:
            id (int): The ID of the record to select.

        Returns:
            Dict: A dictionary representing the selected record.
        """

        stm = select(self.tbl.c).where(and_(self.tbl.c.id == id))

        return self.fetch_one_dict(stm)

    def count(self) -> int:
        """
        Returns the count of rows in the "transformd" table.

        Returns:
            int: The count of rows in the table.

        """
        return self.execute_count(self.tbl)

    def bulk_insert(self, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """
        Inserts data from a pandas DataFrame into the database table in bulk.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to be
            inserted.
        commit_every (int, optional): The number of rows to insert before
            committing the transaction. Defaults to 100.

        Returns:
            int: The number of affected rows.
        """

        return self.execute_bulk_insert(tbl=self.tbl, df=df, commit_every=commit_every)

    def insert(self, data: Dict) -> Dict:
        """
        Inserts a row into the "transformd" table.

        Args:
            data (dict): The data to insert.

        Returns:
            dict: The inserted row.

        """
        stm = self.tbl.insert().values(**data)
        engine = self.get_db_engine()
        with engine.connect() as con:
            result = con.execute(stm)
            con.commit()
            id = result.inserted_primary_key[0]
            return self.select_by_id(id)

    def update(self, id: int, data: Dict) -> int:
        """
        Updates a row in the "transformd" table based on the ID.

        Args:
            id (int): The ID of the row to update.
            data (dict): The data to update.

        Returns:
            int: The number of affected rows.

        """
        stm = self.tbl.update().where(self.tbl.c.id == id).values(**data)
        engine = self.get_db_engine()
        with engine.connect() as con:
            result = con.execute(stm)
            con.commit()
            return result.rowcount

    def task_started(self, id: int):
        """
        Updates the status of a task to 'running' and sets the process start
        time.

        Parameters:
        id (int): The unique identifier of the task to be updated.

        Raises:
        Exception: If there is an error updating the task status.
        """
        try:
            self.update(
                id,
                {
                    "status": "running",
                    "process_start_time": datetime.now(timezone.utc).replace(tzinfo=timezone.utc),
                    "process_end_time": None,
                    "process_exec_time": 0,
                    "exposures": 0,
                    "visits1": 0,
                    "error": None,
                },
            )

        except Exception as e:
            raise Exception(f"Error updating task to running status: {e}")

    def task_update_counts(self, id: int, exposures: int, visits1: int):
        """
        Updates the task counts for a given task ID.

        Parameters:
        id (int): The ID of the task to update.
        exposures (int): The number of exposures to set for the task.
        visits1 (int): The number of visits to set for the task.

        Raises:
        Exception: If there is an error updating the task counts.
        """
        try:
            self.update(
                id,
                {
                    "status": "failed",
                    "exposures": exposures,
                    "visits1": visits1,
                },
            )
        except Exception as e:
            raise Exception(f"Error updating task counts: {e}")

    def task_completed(self, id: int):
        """
        Marks a task as completed by updating its status and recording the
            execution time.

        Args:
            id (int): The unique identifier of the task to be marked as
            completed.

        Raises:
            Exception: If there is an error updating the task status.
        """
        try:
            row = self.select_by_id(id)

            process_start_time = row["process_start_time"].replace(tzinfo=timezone.utc)
            process_end_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
            exec_time = process_end_time - process_start_time

            self.update(
                id,
                {
                    "status": "completed",
                    "process_end_time": process_end_time,
                    "process_exec_time": exec_time.total_seconds(),
                    "error": None,
                },
            )
        except Exception as e:
            raise Exception(f"Error updating task to completed status: {e}")

    def task_failed(self, id: int, error: str):
        """
        Marks a task as failed in the database and updates relevant fields.

        This method retrieves a task by its ID, calculates the execution time,
        and updates the task's status to 'failed' along with the process end
        time, execution time, and error message. If an error occurs during this
        process, an exception is raised with a descriptive message.

        Args:
            id (int): The unique identifier of the task.
            error (str): The error message describing why the task failed.

        Raises:
            Exception: If there is an error updating the task status.
        """
        try:
            row = self.select_by_id(id)

            process_start_time = row["process_start_time"].replace(tzinfo=timezone.utc)
            process_end_time = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
            exec_time = process_end_time - process_start_time

            self.update(
                id,
                {
                    "status": "failed",
                    "process_end_time": process_end_time,
                    "process_exec_time": exec_time.total_seconds(),
                    "error": error,
                },
            )
        except Exception as e:
            raise Exception(f"Error updating task to failed status: {e}")

    def task_retries_increment(self, id: int):
        """
        Increment the retry count for a task identified by its ID.

        Args:
            id (int): The ID of the task to increment the retry count for.

        Raises:
            Exception: If there is an error updating the task retries.
        """
        try:
            row = self.select_by_id(id)
            retries = row["retries"] + 1

            self.update(
                id,
                {
                    "retries": retries,
                    # last retry time
                },
            )
        except Exception as e:
            raise Exception(f"Error updating task retries: {e}")

    def select_next(self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> Dict:
        """
        Select the next pending record within the specified time range.

        Args:
            start_time (Optional[datetime]): The start time to filter records.
                Defaults to None.
            end_time (Optional[datetime]): The end time to filter records.
                Defaults to None.

        Returns:
            Dict: A dictionary representing the next pending record that
                matches the criteria.
        """
        clauses = [
            self.tbl.c.status == "pending",
        ]
        if start_time is not None:
            clauses.append(self.tbl.c.start_time >= start_time)
        if end_time is not None:
            clauses.append(self.tbl.c.end_time <= end_time)

        stm = select(self.tbl.c).where(and_(*clauses)).order_by(self.tbl.c.start_time).limit(1)

        # print(self.debug_query(stm, with_parameters=True))
        return self.fetch_one_dict(stm)

    def select_last(self) -> Dict:
        """
        Selects the last record from the table based on the 'end_time' column.

        This method constructs a SQL query to select the last record from the
        table associated with this DAO (Data Access Object).
        The selection is ordered by the 'end_time' column in descending order
        and limited to one record.

        Returns:
            Dict: A dictionary representing the last record in the table.
        """

        stm = select(self.tbl.c).order_by(desc(self.tbl.c.end_time)).limit(1)

        # print(self.debug_query(stm, with_parameters=True))
        return self.fetch_one_dict(stm)

    def select_recent(self, end_time: datetime, limit: Optional[int] = None) -> list[Dict]:
        """
        Selects recent records from the table with a status of 'pending'
        and an end time less than or equal to the specified end time.
        Args:
            end_time (datetime): The end time threshold for selecting records.
            limit (Optional[int], optional): The maximum number of records to
                return. Defaults to None.
        Returns:
            list[Dict]: A list of dictionaries representing the selected
                records.
        """

        stm = (
            select(self.tbl.c)
            .where(and_(self.tbl.c.status == "pending", self.tbl.c.end_time <= end_time))
            .order_by(desc(self.tbl.c.end_time))
        )

        if limit is not None:
            stm = stm.limit(limit)

        # print(self.debug_query(stm, with_parameters=True))
        return self.fetch_all_dict(stm)
