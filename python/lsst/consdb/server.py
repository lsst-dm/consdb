from flask import Flask, request
from sqlalchemy import create_engine, MetaData
import sqlalchemy.exc


app = Flask(__name__)
engine = create_engine("postgresql://usdf-butler.slac.stanford.edu:5432/lsstdb1")
metadata_obj = MetaData(schema="cdb_latiss")
metadata_obj.reflect(engine)


@app.post("/insert")
def insert():
    info = request.json
    table = info["table"]
    valdict = info["values"]
    keylist = list(valdict.keys())
    valuelist = list(valdict.values())
    placeholders = ",".join(["?"] * len(valdict))
    # check schema

    with engine.begin() as conn:
        conn.exec_driver_sql(
            f"INSERT OR UPDATE INTO ? ({placeholders}) VALUES ({placeholders})",
            [table] + keylist + valuelist,
        )
    return ("OK", 200)


@app.post("/query")
def query():
    info = request.json
    tables = ",".join(info["tables"])
    columns = ",".join(info["columns"])
    if "where" in info:
        where = "WHERE " + info["where"]
        if ";" in where:
            return ("Cannot create query containing more than one statement", 403)
    with engine.begin() as conn:
        try:
            cursor = conn.exec_driver_sql(f"SELECT {columns} FROM {tables} {where}")
            first = True
            result = []
            for row in cursor:
                if first:
                    result.append(row._fields)
                    first = False
                result.append(list(row))
            return result
        except sqlalchemy.exc.DBAPIError as e:
            return (str(e), 500)


@app.get("/schema/<table>")
def schema(table: str):
    return [(c.name, str(c.type), c.doc) for c in metadata_obj.tables[table.lower()].columns]
