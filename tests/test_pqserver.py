import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import numpy as np
import pytest
import sqlalchemy as sa
from astropy.table import Table
from astropy.time import Time
from fastapi.testclient import TestClient
from requests import Response


def _assert_http_status(response: Response, status: int):
    assert response.status_code == status, f"{response.status_code} {response.json()}"


@pytest.fixture
def tmpdir(scope="module"):
    tmpdir = Path(tempfile.mkdtemp())
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


@pytest.fixture
def db(tmpdir, scope="module"):
    db_path = tmpdir / "test.db"
    instruments = ["latiss"]
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE schemas (name text, path text)")
        for instrument in instruments:
            schema = f"cdb_{instrument}"
            sql = Path(__file__).parent / f"{schema}.sql"
            if not sql.exists():
                continue
            schema_path = tmpdir / f"{schema}.db"
            conn.execute(f"INSERT INTO schemas VALUES ('{schema}', '{schema_path}')")
            with sqlite3.connect(schema_path) as schema_conn:
                schema_conn.executescript(sql.read_text())
            schema_conn.close()
    conn.close()
    with sqlite3.connect(tmpdir / "cdb_latiss.db") as conn:
        conn.execute(
            "INSERT INTO exposure "
            "(exposure_id, exposure_name, controller, day_obs, seq_num, "
            "physical_filter, band, s_ra, s_dec, sky_rotation) "
            "VALUES "
            "(2024032100002, 'AT_O_20240321_000002', 'O', 20240321, 2, "
            "'empty~empty', 'EMPTY', 0, 0, 3.780205180514687);"
        )
    conn.close()
    return db_path


@pytest.fixture
def astropy_tables(scope="module"):
    t = dict()
    return t


@pytest.fixture
def lsstcomcamsim(tmpdir, astropy_tables, scope="module"):
    schema = "cdb_lsstcomcamsim"
    db_path = tmpdir / "test.db"
    schema_path = tmpdir / f"{schema}.db"

    data_path = Path(__file__).parent / "lsstcomcamsim"
    sql_path = data_path / f"{schema}.sql"

    # Build the main db file to specify where to look for
    # specific schemas.
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE schemas (name text, path text)")
        conn.execute(f"INSERT INTO schemas VALUES ('{schema}', '{schema_path}')")

    # Set up the lsstcomcamsim schema with the schema from the SQL file
    # generated with felis, and with sample data interrogated from consdb,
    # and with fake made up flex data
    with sqlite3.connect(schema_path) as conn:
        conn.executescript(sql_path.read_text())

    engine = sa.create_engine(f"sqlite:///{schema_path}")

    table_dict = {
        "exposure2.ecsv": "exposure",
        "ccdexposure.ecsv": "ccdexposure",
        "ccdvisit1_quicklook.ecsv": "ccdvisit1_quicklook",
        "exposure.ecsv": "exposure",
        "visit1_quicklook.ecsv": "visit1_quicklook",
    }

    for file_name, table_name in table_dict.items():
        astropy_table = Table.read(data_path / file_name)
        astropy_tables[file_name] = astropy_table
        metadata = sa.MetaData()

        sql_table = sa.Table(table_name, metadata, autoload_with=engine)

        # Convert the Astropy table to a list of dictionaries, one per row
        rows = [
            {
                k: (
                    None
                    if v is None or v == "null"
                    else (
                        v.to_datetime()
                        if isinstance(v, Time)
                        else bool(v) if isinstance(v, np.bool_) else str(v)
                    )
                )
                for k, v in dict(row).items()
            }
            for row in astropy_table
        ]

        # Insert rows into the SQL table
        with engine.begin() as connection:
            connection.execute(sql_table.insert(), rows)

    engine.dispose()

    print(f"{db_path=}")
    os.environ["POSTGRES_URL"] = f"sqlite:///{db_path}"
    from lsst.consdb import pqserver, utils

    pqserver.engine = utils.setup_postgres()
    pqserver.instrument_tables = pqserver.InstrumentTables()
    try:
        yield TestClient(pqserver.app)
    finally:
        pqserver.engine.dispose()


@pytest.fixture
def app(db, scope="module"):
    os.environ["POSTGRES_URL"] = f"sqlite:///{db}"
    from lsst.consdb import pqserver, utils

    pqserver.engine = utils.setup_postgres()
    pqserver.instrument_tables = pqserver.InstrumentTables()
    try:
        yield pqserver.app
    finally:
        pqserver.engine.dispose()


@pytest.fixture
def client(app, scope="module"):
    # NOTE: all tests share the same client, app, and database.
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    result = response.json()
    assert "instruments" in result
    assert "obs_types" in result
    assert "dtypes" in result


def test_root2(client):
    response = client.get("/consdb")
    result = response.json()
    assert "instruments" in result
    assert "latiss" in result["instruments"]
    assert "obs_types" in result
    assert "exposure" in result["obs_types"]
    assert "dtypes" in result
    assert set(result["dtypes"]) == {"bool", "int", "float", "str"}


def test_insert_multiple(lsstcomcamsim):
    data = {
        7024052800012: {
            "exposure_name": "CC_S_20240528_000012",
            "controller": "S",
            "day_obs": 20240528,
            "seq_num": 12,
            "physical_filter": "i_06",
            "exp_midpt": "2024-05-28T22:19:04.847500",
            "exp_midpt_mjd": 60458.92991721521,
            "obs_start": "2024-05-28T22:19:04.300000",
            "obs_start_mjd": 60458.92991088214,
            "obs_end": "2024-05-28T22:19:05.395000",
            "obs_end_mjd": 60458.929923548276,
            "emulated": False,
        },
        7024052800011: {
            "exposure_name": "CC_S_20240528_000011",
            "controller": "S",
            "day_obs": 20240528,
            "seq_num": 11,
            "physical_filter": "i_06",
            "exp_midpt": "2024-05-28T22:19:00.632500",
            "exp_midpt_mjd": 60458.929868432606,
            "obs_start": "2024-05-28T22:19:00.086000",
            "obs_start_mjd": 60458.929862109704,
            "obs_end": "2024-05-28T22:19:01.179000",
            "obs_end_mjd": 60458.92987475551,
            "emulated": False,
        },
    }
    response = lsstcomcamsim.post(
        "/consdb/insert/lsstcomcamsim/exposure",
        json={"obs_dict": data},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert "Data inserted" in result["message"]
    assert result["table"] == "exposure"
    assert result["instrument"] == "lsstcomcamsim"
    assert result["obs_id"] == list(data.keys())


def test_insert_multiple_update(lsstcomcamsim):
    data = {
        7024052800012: {
            "exposure_name": "CC_S_20240528_000012",
            "controller": "S",
            "day_obs": 20240528,
            "seq_num": 12,
            "physical_filter": "i_06",
            "exp_midpt": "2024-05-28T22:19:04.847500",
            "exp_midpt_mjd": 60458.92991721521,
            "obs_start": "2024-05-28T22:19:04.300000",
            "obs_start_mjd": 60458.92991088214,
            "obs_end": "2024-05-28T22:19:05.395000",
            "obs_end_mjd": 60458.929923548276,
            "emulated": False,
        },
        7024052800011: {
            "exposure_name": "CC_S_20240528_000011",
            "controller": "S",
            "day_obs": 20240528,
            "seq_num": 11,
            "physical_filter": "i_06",
            "exp_midpt": "2024-05-28T22:19:00.632500",
            "exp_midpt_mjd": 60458.929868432606,
            "obs_start": "2024-05-28T22:19:00.086000",
            "obs_start_mjd": 60458.929862109704,
            "obs_end": "2024-05-28T22:19:01.179000",
            "obs_end_mjd": 60458.92987475551,
            "emulated": False,
        },
    }
    response = lsstcomcamsim.post(
        "/consdb/insert/lsstcomcamsim/exposure",
        json={"obs_dict": data},
    )
    _assert_http_status(response, 200)

    data[7024052800012]["exposure_name"] = "fred"
    data[7024052800011]["exposure_name"] = "sally"
    response = lsstcomcamsim.post(
        "/consdb/insert/lsstcomcamsim/exposure",
        json={"obs_dict": data},
    )
    _assert_http_status(response, 500)

    response = lsstcomcamsim.post(
        "/consdb/insert/lsstcomcamsim/exposure?u=1",
        json={"obs_dict": data},
    )
    _assert_http_status(response, 200)
    assert response.json()["obs_id"] == list(data.keys())


def test_schema(lsstcomcamsim):
    response = lsstcomcamsim.get("/consdb/schema/lsstcomcamsim")
    _assert_http_status(response, 200)


def test_schema_non_instrument(lsstcomcamsim):
    response = lsstcomcamsim.get("/consdb/schema/asdf")
    _assert_http_status(response, 404)
    result = response.json()
    assert "Unknown instrument" in result["message"]


def test_schema_instrument(lsstcomcamsim):
    response = lsstcomcamsim.get("/consdb/schema/lsstcomcamsim")
    _assert_http_status(response, 200)
    result = response.json()
    assert isinstance(result, list)
    tables = [
        "exposure",
        "ccdexposure",
        "ccdexposure_camera",
        "ccdvisit1_quicklook",
        "visit1_quicklook",
        "exposure_flexdata",
        "exposure_flexdata_schema",
        "ccdexposure_flexdata",
        "ccdexposure_flexdata_schema",
    ]
    tables = [f"cdb_lsstcomcamsim.{t}" for t in tables]
    for t in tables:
        assert t in result


def test_schema_non_table(lsstcomcamsim):
    response = lsstcomcamsim.get("/consdb/schema/lsstcomcamsim/asdf")
    _assert_http_status(response, 404)
    assert "Unknown table" in response.json()["message"]


def test_schema_table(lsstcomcamsim, astropy_tables):
    astropy_table = astropy_tables["exposure.ecsv"]
    response = lsstcomcamsim.get("/consdb/schema/lsstcomcamsim/exposure")
    _assert_http_status(response, 200)
    result = response.json()
    for column in astropy_table.columns:
        assert column in result.keys()


def test_validate_unit():
    os.environ["POSTGRES_URL"] = "sqlite://"
    from lsst.consdb import pqserver

    assert pqserver.AddKeyRequestModel.validate_unit("s") == "s"
    assert pqserver.AddKeyRequestModel.validate_unit("km/s") == "km/s"
    assert pqserver.AddKeyRequestModel.validate_unit("km s-1") == "km s-1"

    with pytest.raises(ValueError):
        pqserver.AddKeyRequestModel.validate_unit("tacos / s")


def test_validate_ucd():
    os.environ["POSTGRES_URL"] = "sqlite://"
    from lsst.consdb import pqserver

    assert pqserver.AddKeyRequestModel.validate_ucd("this.is.a.valid.ucd")
    assert pqserver.AddKeyRequestModel.validate_ucd("THIS-ONE.IS.TOO")

    with pytest.raises(ValueError):
        pqserver.AddKeyRequestModel.validate_ucd("but this is not")

    with pytest.raises(ValueError):
        pqserver.AddKeyRequestModel.validate_ucd("neither#is@this[one]!")


def test_flexible_metadata(client):
    response = client.post(
        "/consdb/flex/latiss/exposure/addkey",
        json={"key": "foo", "dtype": "bool", "doc": "bool key"},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Key added to flexible metadata",
        "key": "foo",
        "instrument": "latiss",
        "obs_type": "exposure",
    }

    response = client.post(
        "/consdb/flex/LATISS/exposure/addkey",
        json={"key": "bar", "dtype": "int", "doc": "int key"},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Key added to flexible metadata",
        "key": "bar",
        "instrument": "LATISS",
        "obs_type": "exposure",
    }

    response = client.post(
        "/consdb/flex/latiss/Exposure/addkey",
        json={"key": "baz", "dtype": "float", "doc": "float key"},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result["obs_type"] == "exposure"

    response = client.post(
        "/consdb/flex/bad_instrument/exposure/addkey",
        json={"key": "quux", "dtype": "str", "doc": "str key"},
    )
    _assert_http_status(response, 404)
    result = response.json()
    assert "Unknown instrument" in result["message"]

    response = client.get("/consdb/flex/latiss/exposure/schema")
    _assert_http_status(response, 200)
    result = response.json()
    assert "foo" in result
    assert "bar" in result
    assert "baz" in result
    assert result["baz"] == ["float", "float key", None, None]

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/2024032100002",
        json={"values": {"foo": True, "bar": 42, "baz": 3.14159}},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result["message"] == "Flexible metadata inserted"
    assert result["obs_id"] == 2024032100002

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/2024032100002",
        json={"values": {"foo": True, "bar": 42, "baz": 3.14159}},
    )
    _assert_http_status(response, 500)
    result = response.json()
    assert "UNIQUE" in result["message"]

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/2024032100002",
        json={"values": {"bad_key": 2.71828}},
    )
    _assert_http_status(response, 404)
    result = response.json()
    assert result["message"] == "Unknown key"
    assert result["value"] == "bad_key"

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {"foo": True, "bar": 42, "baz": 3.14159}

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002?k=bar&k=baz")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {"bar": 42, "baz": 3.14159}

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/2024032100002?u=1",
        json={"values": {"foo": False, "bar": 34, "baz": 2.71828}},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result["message"] == "Flexible metadata inserted"

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {"foo": False, "bar": 34, "baz": 2.71828}

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002?k=baz")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {"baz": 2.71828}

    response = client.post("/consdb/flex/latiss/exposure/obs/2024032100002", json={})
    _assert_http_status(response, 404)
    result = response.json()
    assert "Validation error" in result["message"]
    assert result["detail"][0]["type"] == "missing"
    assert "values" in result["detail"][0]["loc"]

    response = client.post(
        "/consdb/insert/latiss/exposure/obs/2024032100003",
        json={
            "values": {
                "exposure_name": "AT_O_20240327_000002",
                "controller": "O",
                "day_obs": 20240327,
                "seq_num": 2,
            },
        },
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Data inserted",
        "table": "cdb_latiss.exposure",
        "instrument": "latiss",
        "obs_id": 2024032100003,
    }

    response = client.post("/consdb/query", json={"query": "SELECT * FROM exposure ORDER BY day_obs;"})
    _assert_http_status(response, 200)
    result = response.json()
    assert len(result) == 2
    assert "exposure_id" in result["columns"]
    assert 20240321 in result["data"][0]
    assert "AT_O_20240327_000002" in result["data"][1]
