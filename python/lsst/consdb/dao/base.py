import warnings
from typing import Any, Dict, List

import numpy
import pandas
from sqlalchemy import Engine, MetaData, Table, create_engine
from sqlalchemy import exc as sa_exc
from sqlalchemy import func
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.pool import NullPool


class DBBase:
    """
    The base class for database access objects.

    Attributes:
        engine (Engine): The database engine.
        con: The database connection.
        dialect: The database dialect.
        db_uri (str): The URI of the database.
    """

    engine: Engine = None
    con = None
    dialect = None
    db_uri: str

    def __init__(self, db_uri: str):
        """
        Initialize a BaseDAO object.

        Args:
            db_uri (str): The URI of the database.

        Raises:
            Exception: If the dialect for the given SGBD has not been
                implemented.
        """
        self.db_uri = db_uri

        sgbd = self.db_uri.split(":")[0]

        if sgbd == "sqlite":
            self.dialect = sqlite
        elif sgbd == "postgresql":
            self.dialect = postgresql
        else:
            raise Exception(f"The dialect for {sgbd} has not yet been implemented.")

    def get_db_engine(self) -> Engine:
        """
        Returns the database engine.

        If the engine is not already created, it creates a new engine
        using the provided database URI and returns it.

        Returns:
            The database engine.

        """
        if self.engine is None:
            self.engine = create_engine(self.db_uri, poolclass=NullPool)

        return self.engine

    def get_con(self):
        """
        Returns the database connection.

        If the connection is not already established, it creates a new
        connection using the database engine obtained
        from `get_db_engine` method.

        Returns:
            The database connection.

        """
        if self.con is None:
            engine = self.get_db_engine()
            self.con = engine.connect()

        return self.con

    def get_table(self, tablename, schema=None) -> Table:
        """
        Retrieve a table object from the database.

        Args:
            tablename (str): The name of the table to retrieve.
            schema (str, optional): The name of the schema where the table
                resides. Defaults to None.

        Returns:
            Table: The table object representing the requested table.
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)

            engine = self.get_db_engine()
            metadata = MetaData()
            metadata.reflect(bind=engine)

            if schema:
                tbl = Table(tablename, metadata, autoload=True, schema=schema)
            else:
                tbl = Table(tablename, metadata, autoload=True)
            return tbl

    def execute(self, stm):
        """
        Executes the given SQL statement on the database.

        Args:
            stm (str): The SQL statement to execute.

        Returns:
            ResultProxy: The result of the executed statement.

        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            engine = self.get_db_engine()
            with engine.connect() as con:
                return con.execute(stm)

    def fetch_all_dict(self, stm) -> List[Dict]:
        """
        Fetches all rows from the database using the provided SQL statement
        and returns them as a list of dictionaries.

        Args:
            stm (str): The SQL statement to execute.

        Returns:
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
        """
        Fetches a single row from the database and returns it as a
        dictionary.

        Args:
            stm (str): The SQL statement to execute.

        Returns:
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
        """
        Executes the given SQL statement and returns the first column of
        the first row as a scalar value.

        Args:
            stm (str): The SQL statement to execute.

        Returns:
            Any: The scalar value returned by the SQL statement.
        """
        engine = self.get_db_engine()
        with engine.connect() as con:
            return con.execute(stm).scalar()

    def fetch_scalars(self, stm) -> List[Any]:
        """
        Fetches and returns a list of scalar values from the database.

        Args:
            stm (str): The SQL statement to execute.

        Returns:
            List[Any]: A list of scalar values fetched from the database.
        """
        engine = self.get_db_engine()
        with engine.connect() as con:
            return list(con.execute(stm).scalars())

    def execute_count(self, table: Table) -> int:
        """
        Executes a count query on the specified table and returns the result.

        Args:
            table (Table): The table to execute the count query on.

        Returns:
            int: The count result.

        """
        engine = self.get_db_engine()
        with engine.connect() as con:
            stm = func.count().select().select_from(table)
            return con.scalar(stm)

    def execute_upsert(self, tbl: Table, df: pandas.DataFrame, commit_every: int = 100) -> int:
        """
        Execute an upsert operation on the given table using the provided
        DataFrame.

        Args:
            tbl (Table): The table object representing the database table.
            df (pandas.DataFrame): The DataFrame containing the data to be
                upserted.
            commit_every (int, optional): The number of records to commit at
                once. Defaults to 100.

        Returns:
            int: The number of affected rows.

        Raises:
            None

        """
        # Based on these solutions
        # https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-upsert-statements
        # https://docs.sqlalchemy.org/en/20/_modules/examples/performance/bulk_inserts.html
        # https://stackoverflow.com/a/55357460/24123418

        # replace NaN for None
        df = df.replace(numpy.nan, None)

        # List of all columns that will be used in the insert
        insert_cols = df.columns.to_list()

        # List of columns without primary keys.
        # These columns will be updated in case of conflict.
        update_cols = [
            c.name for c in tbl.c if c not in list(tbl.primary_key.columns) and c.name in insert_cols
        ]

        # Convert the dataframe to a list of dicts
        records = df.to_dict("records")

        affected_rows = 0

        for i in range(0, len(records), commit_every):
            chunk = records[i: i + commit_every]

            # Insert Statement using dialect insert
            insert_stm = self.dialect.insert(tbl).values(chunk)

            # Update Statement using in case of conflict makes an update.
            # IMPORTANT: The dialect must be compatible with
            # on_conflict_do_update.
            upsert_stm = insert_stm.on_conflict_do_update(
                index_elements=tbl.primary_key.columns,
                set_={k: getattr(insert_stm.excluded, k) for k in update_cols},
            )
            # print(self.debug_query(upsert_stm, True))

            engine = self.get_db_engine()
            with engine.connect() as con:
                result = con.execute(upsert_stm)
                con.commit()
                affected_rows += result.rowcount

        return affected_rows

    def debug_query(self, stm, with_parameters=False) -> str:
        """
        Returns the SQL representation of the given statement for debugging
        purposes.

        Args:
            stm: The statement to be converted to SQL.
            with_parameters: Whether to include parameter values in the SQL.

        Returns:
            str: The SQL representation of the statement.
        """
        sql = self.stm_to_str(stm, with_parameters)
        return sql

    def stm_to_str(self, stm, with_parameters=False):
        """
        Converts a SQLAlchemy statement object to a string representation of
        the corresponding SQL query.

        Args:
            stm (sqlalchemy.sql.expression.Selectable): The SQLAlchemy
                statement object to convert.
            with_parameters (bool, optional): Whether to include parameter
                values in the resulting SQL string. Defaults to False.

        Returns:
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
