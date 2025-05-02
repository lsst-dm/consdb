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

"""Provides the `DBBase` class for managing database access."""

import logging
import warnings
from datetime import datetime, timezone
from typing import Any, Dict, List

import numpy
import pandas
from sqlalchemy import Engine, MetaData, Table, create_engine
from sqlalchemy import exc as sa_exc
from sqlalchemy import func
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.pool import NullPool


class DBBase:
    """The base class for database access objects.

    Attributes
    ----------
        engine (Engine): The database engine.
        connexion: The database connection.
        dialect: The database dialect.
        db_uri (str): The URI of the database.
        logger (logging.Logger): The logger for the class.

    """

    engine: Engine = None
    connexion = None
    dialect = None
    db_uri: str

    def __init__(self, db_uri: str, schema: str = None, logger: logging.Logger = None):
        """Initialize a BaseDAO object.

        Args:
        ----
            db_uri (str): The URI of the database.
            schema (str, optional): The schema to use. Defaults to None.
            logger (logging.Logger, optional): The logger to use.
                Defaults to None.

        Raises:
        ------
            Exception: If the dialect has not been implemented.

        """
        self.db_uri = db_uri
        self.log = logger

        sgbd = self.db_uri.split(":")[0]

        if sgbd == "sqlite":
            self.dialect = sqlite
        elif sgbd == "postgresql":
            self.dialect = postgresql
        else:
            raise Exception(f"The dialect for {sgbd} has not yet been implemented.")

    def get_db_engine(self) -> Engine:
        """Return the database engine.

        If the engine is not already created, it creates a new engine
        using the provided database URI and returns it.

        Returns
        -------
            The database engine.

        """
        if self.engine is None:
            self.engine = create_engine(self.db_uri, poolclass=NullPool)

        return self.engine

    def get_con(self):
        """Return the database connection.

        If the connection is not already established, it creates a new
        connection using the database engine obtained
        from `get_db_engine` method.

        Returns
        -------
            The database connection.

        """
        if self.connexion is None:
            engine = self.get_db_engine()
            self.connexion = engine.connect()

        return self.connexion

    def get_table(self, tablename, schema=None) -> Table:
        """Retrieve a table object from the database.

        Args:
        ----
            tablename (str): The name of the table to retrieve.
            schema (str, optional): The name of the schema where the table
                resides. Defaults to None.

        Returns:
        -------
            Table: The table object representing the requested table.

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)

            engine = self.get_db_engine()
            metadata = MetaData()
            metadata.reflect(engine)

            if schema is not None and self.dialect == postgresql:
                tbl = Table(tablename, metadata, autoload_with=self.get_con(), schema=schema)
            else:
                tbl = Table(tablename, metadata, autoload_with=self.get_con())
            return tbl

    def execute(self, stm):
        """Execute SQL statement on the database.

        Args:
        ----
            stm (str): The SQL statement to execute.

        Returns:
        -------
            ResultProxy: The result of the executed statement.

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            engine = self.get_db_engine()
            with engine.connect() as con:
                return con.execute(stm)

    def fetch_all_dict(self, stm) -> List[Dict]:
        """Fetch all rows from the database using the provided SQL statement.

        Args:
        ----
            stm (str): The SQL statement to execute.

        Returns:
        -------
            List[Dict]: A list of dictionaries representing the fetched rows.

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)

            engine = self.get_db_engine()
            with engine.connect() as con:

                queryset = con.execute(stm)

                rows = []
                for row in queryset:
                    d = row._asdict()
                    rows.append(d)

                return rows

    def fetch_one_dict(self, stm) -> Dict:
        """Fetch single row from the database and returns it as a dictionary.

        Args:
        ----
            stm (str): The SQL statement to execute.

        Returns:
        -------
            dict: A dictionary representing the fetched row, or None if no
                row is found.

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)

            engine = self.get_db_engine()
            with engine.connect() as con:

                queryset = con.execute(stm).fetchone()

                if queryset is not None:
                    d = queryset._asdict()
                    return d
                else:
                    return None

    def fetch_scalar(self, stm) -> Any:
        """Execute SQL statement and returns the first column of the first row.

        Args:
        ----
            stm (str): The SQL statement to execute.

        Returns:
        -------
            Any: The scalar value returned by the SQL statement.

        """
        engine = self.get_db_engine()
        with engine.connect() as con:
            return con.execute(stm).scalar()

    def fetch_scalars(self, stm) -> List[Any]:
        """Fetch and return list of scalar values from the database.

        Args:
        ----
            stm (str): The SQL statement to execute.

        Returns:
        -------
            List[Any]: A list of scalar values fetched from the database.

        """
        engine = self.get_db_engine()
        with engine.connect() as con:
            return list(con.execute(stm).scalars())

    def execute_count(self, table: Table) -> int:
        """Count total rows in the given table.

        Args:
        ----
            table (Table): The table to query.

        Returns:
        -------
            int: Total row count.

        """
        engine = self.get_db_engine()
        with engine.connect() as con:
            stm = func.count().select().select_from(table)
            return con.scalar(stm)

    def execute_upsert(self, tbl: Table, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """Executes an upsert on the table using the provided DataFrame.

        Args:
        ----
            tbl (Table): The table object representing the database table.
            df (pandas.DataFrame): The DataFrame to be upserted.
            commit_every (int, optional): The number of records to commit at
                once. Defaults to 100.

        Returns:
        -------
            int: The number of affected rows.

        Raises:
        ------
            ValueError: If the DataFrame is missing primary key columns or if
                there are no columns to update.
        """
        # Replace NaN with None for SQL compatibility
        df = df.replace(numpy.nan, None)

        # Validate that the DataFrame includes all primary key columns
        pk_columns = {c.name for c in tbl.primary_key.columns}
        if not pk_columns.issubset(df.columns):
            missing_cols = pk_columns - set(df.columns)
            raise ValueError(f"DataFrame is missing primary key columns: {missing_cols}")

        # List of all columns that will be used in the insert
        insert_cols = df.columns.to_list()

        # List of columns without primary keys.
        # These columns will be updated in case of conflict.
        update_cols = [
            c.name for c in tbl.c if c not in list(tbl.primary_key.columns) and c.name in insert_cols
        ]

        # Warn when update_cols is not empty
        if not update_cols:
            self.log.debug(
                f"event=row_upserted schema={tbl.schema} table={tbl.name} "
                f"warning='No data from the EFD to upsert'"
            )

        # Convert the dataframe to a list of dicts
        records = df.to_dict("records")
        affected_rows = 0

        for i in range(0, len(records), commit_every):
            chunk = records[i : i + commit_every]

            # Insert Statement using dialect insert
            insert_stm = self.dialect.insert(tbl).values(chunk)

            # Update statement
            if update_cols:
                upsert_stm = insert_stm.on_conflict_do_update(
                    index_elements=tbl.primary_key.columns,
                    set_={k: getattr(insert_stm.excluded, k) for k in update_cols},
                )
            else:
                upsert_stm = insert_stm.on_conflict_do_nothing()

            # Log each row being committed, only primary key values
            pk_names = [col.name for col in tbl.primary_key.columns]
            for record in chunk:
                pk_values = {name: record[name] for name in pk_names}
                self.log.info(
                    f"event=row_upserted schema={tbl.schema} table={tbl.name} pk_values={pk_values}"
                )

            # Execute the upsert statement
            engine = self.get_db_engine()
            with engine.connect() as con:
                result = con.execute(upsert_stm)
                con.commit()
                # account affected rows for two states on_conflict_do_nothing
                # and on_conflict_do_update
                affected_rows += (
                    len(result.inserted_primary_key) if result.inserted_primary_key else result.rowcount
                )

        return affected_rows

    def execute_bulk_insert(self, tbl: Table, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """Inserts data in bulk into the table using the provided DataFrame.

        Args:
        ----
            tbl (Table): The table object representing the database table.
            df (pandas.DataFrame): The DataFrame containing the data to insert.
            commit_every (int, optional): The number of rows to commit at once.
                Defaults to 100.

        Returns:
        -------
            int: The number of rows inserted.

        """
        # replace NaN for None
        df = df.replace(numpy.nan, None)

        # Convert the dataframe to a list of dicts
        records = df.to_dict("records")

        affected_rows = 0

        for i in range(0, len(records), commit_every):
            chunk = records[i : i + commit_every]

            # Insert Statement using dialect insert
            insert_stm = self.dialect.insert(tbl).values(chunk)

            # Log each row being committed, only primary key values
            pk_names = [col.name for col in tbl.primary_key.columns]
            for record in chunk:
                pk_values = {name: record[name] for name in pk_names}
                self.log.info(f"event=insert schema={tbl.schema} table={tbl.name} pk_values={pk_values}")

            engine = self.get_db_engine()
            with engine.connect() as con:
                result = con.execute(insert_stm)
                con.commit()
                affected_rows += result.rowcount

        return affected_rows

    def debug_query(self, stm, with_parameters=False) -> str:
        """Returns SQL representation of the statement for debugging.

        Args:
        ----
            stm: The statement to be converted to SQL.
            with_parameters: Whether to include parameter values in the SQL.

        Returns:
        -------
            str: The SQL representation of the statement.

        """
        sql = self.stm_to_str(stm, with_parameters)
        return sql

    def stm_to_str(self, stm, with_parameters=False):
        """Convert SQLAlchemy statement object to a string representation.

        Args:
        ----
            stm (sqlalchemy.sql.expression.Selectable): The SQLAlchemy
                statement object to convert.
            with_parameters (bool, optional): Whether to include parameter
                values in the resulting SQL string. Defaults to False.

        Returns:
        -------
            str: The string representation of the SQL query.

        """
        sql = str(
            stm.compile(
                dialect=self.dialect.dialect(),
                compile_kwargs={"literal_binds": with_parameters},
            )
        )

        # Remove new lines
        sql = sql.replace("\n", " ").replace("\r", "")

        return sql

    @staticmethod
    def _ensure_utc(dt: datetime) -> datetime:
        """Ensure datetime is in UTC (naive or aware).
        Args:
            dt: Input datetime
        Returns:
            UTC-naive datetime
        """
        if dt.tzinfo is not None:
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
