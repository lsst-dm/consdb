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
    engine: Engine = None
    con = None
    dialect = None
    db_uri: str

    def __init__(self, db_uri: str):
        self.db_uri = db_uri

        sgbd = self.db_uri.split(":")[0]

        if sgbd == "sqlite":
            self.dialect = sqlite
        elif sgbd == "postgresql":
            self.dialect = postgresql
        else:
            raise Exception("The dialect for xxx has not yet been implemented.")

    def get_db_engine(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(self.db_uri, poolclass=NullPool)

        return self.engine

    def get_con(self):
        if self.con is None:
            engine = self.get_db_engine()
            self.con = engine.connect()

        return self.con

    def get_table(self, tablename, schema=None) -> Table:

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
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            engine = self.get_db_engine()
            with engine.connect() as con:
                return con.execute(stm)

    def fetch_all_dict(self, stm) -> List[Dict]:

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
        engine = self.get_db_engine()
        with engine.connect() as con:
            return con.execute(stm).scalar()

    def fetch_scalars(self, stm) -> List[Any]:
        engine = self.get_db_engine()
        with engine.connect() as con:
            return list(con.execute(stm).scalars())

    def execute_count(self, table: Table) -> int:
        engine = self.get_db_engine()
        with engine.connect() as con:
            stm = func.count().select().select_from(table)
            return con.scalar(stm)

    def execute_upsert(self, tbl: Table, df: pandas.DataFrame) -> int:

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

        # Insert Statement using dialect insert
        insert_stm = self.dialect.insert(tbl).values(records)

        # Update Statement using in case of conflict makes an update.
        # IMPORTANT: The dialect must be compatible with on_conflict_do_update.
        upsert_stm = insert_stm.on_conflict_do_update(
            index_elements=tbl.primary_key.columns,
            set_={k: getattr(insert_stm.excluded, k) for k in update_cols},
        )
        # print(self.debug_query(upsert_stm, True))

        engine = self.get_db_engine()
        with engine.connect() as con:
            result = con.execute(upsert_stm)
            con.commit()
            return result.rowcount

    def debug_query(self, stm, with_parameters=False) -> str:
        sql = self.stm_to_str(stm, with_parameters)
        return sql

    def stm_to_str(self, stm, with_parameters=False):
        sql = str(
            stm.compile(
                dialect=self.dialect.dialect(),
                compile_kwargs={"literal_binds": with_parameters},
            )
        )

        # Remove new lines
        sql = sql.replace("\n", " ").replace("\r", "")

        return sql

    # def import_with_copy_expert(self, sql, data):
    #     """
    #         This method is recommended for importing large volumes of data. using the postgresql COPY method.

    #         The method is useful to handle all the parameters that PostgreSQL makes available
    #         in COPY statement: https://www.postgresql.org/docs/current/sql-copy.html

    #         it is necessary that the from clause is reading from STDIN.

    #         example:
    #         sql = COPY <table> (<columns) FROM STDIN with (FORMAT CSV, DELIMITER '|', HEADER);

    #         Parameters:
    #             sql (str): The sql statement should be in the form COPY table '.
    #             data (file-like ): a file-like object to read or write
    #         Returns:
    #             rowcount (int):  the number of rows that the last execute*() produced (for DQL statements like SELECT) or affected (for DML statements like UPDATE or INSERT)

    #     References:
    #         https://www.psycopg.org/docs/cursor.html#cursor.copy_from
    #         https://stackoverflow.com/questions/30050097/copy-data-from-csv-to-postgresql-using-python
    #         https://stackoverflow.com/questions/13125236/sqlalchemy-psycopg2-and-postgresql-copy
    #     """

    #     with warnings.catch_warnings():
    #         warnings.simplefilter("ignore", category=sa_exc.SAWarning)

    #         connection = self.get_db_engine().raw_connection()
    #         try:
    #             cursor = connection.cursor()
    #             cursor.copy_expert(sql, data)
    #             connection.commit()

    #             cursor.close()
    #             return cursor.rowcount
    #         except Exception as e:
    #             connection.rollback()
    #             raise (e)
    #         finally:
    #             connection.close()
