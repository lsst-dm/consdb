import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import pytest
from requests import Response


def _assert_http_status(response: Response, status: int):
    assert response.status_code == status, f"{response.status_code} {response.json}"


@pytest.fixture
def tmpdir(scope="module"):
    tmpdir = Path(tempfile.mkdtemp())
    return tmpdir
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
def app(db, scope="module"):
    os.environ["POSTGRES_URL"] = f"sqlite:///{db}"
    import pqserver

    return pqserver.app


@pytest.fixture
def client(app, scope="module"):
    # NOTE: all tests share the same client, app, and database.
    return app.test_client()


def test_root(client):
    response = client.get("/")
    result = response.json
    assert "instruments" in result
    assert "obs_types" in result
    assert "dtypes" in result


def test_root2(client):
    response = client.get("/consdb")
    result = response.json
    assert "instruments" in result
    assert "latiss" in result["instruments"]
    assert "obs_types" in result
    assert "exposure" in result["obs_types"]
    assert "dtypes" in result
    assert set(result["dtypes"]) == {"bool", "int", "float", "str"}


def test_flexible_metadata(client):
    response = client.post(
        "/consdb/flex/latiss/exposure/addkey",
        json={"key": "foo", "dtype": "bool", "doc": "bool key"},
    )
    _assert_http_status(response, 200)
    result = response.json
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
    result = response.json
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
    result = response.json
    assert result["obs_type"] == "Exposure"

    response = client.post(
        "/consdb/flex/bad_instrument/exposure/addkey",
        json={"key": "quux", "dtype": "str", "doc": "str key"},
    )
    _assert_http_status(response, 404)
    result = response.json
    assert result == {
        "message": "Unknown instrument",
        "value": "bad_instrument",
        "valid": ["latiss"],
    }

    response = client.get("/consdb/flex/latiss/exposure/schema")
    _assert_http_status(response, 200)
    result = response.json
    assert "foo" in result
    assert "bar" in result
    assert "baz" in result
    assert result["baz"] == ["float", "float key", None, None]

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/2024032100002",
        json={"values": {"foo": True, "bar": 42, "baz": 3.14159}},
    )
    _assert_http_status(response, 200)
    result = response.json
    assert result["message"] == "Flexible metadata inserted"
    assert result["obs_id"] == 2024032100002

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/2024032100002",
        json={"values": {"foo": True, "bar": 42, "baz": 3.14159}},
    )
    _assert_http_status(response, 500)
    result = response.json
    assert "UNIQUE" in result["message"]

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002")
    _assert_http_status(response, 200)
    result = response.json
    assert result == {"foo": True, "bar": 42, "baz": 3.14159}

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002?k=bar&k=baz")
    _assert_http_status(response, 200)
    result = response.json
    assert result == {"bar": 42, "baz": 3.14159}

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/2024032100002?u=1",
        json={"values": {"foo": False, "bar": 34, "baz": 2.71828}},
    )
    _assert_http_status(response, 200)
    result = response.json
    assert result["message"] == "Flexible metadata inserted"

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002")
    _assert_http_status(response, 200)
    result = response.json
    assert result == {"foo": False, "bar": 34, "baz": 2.71828}

    response = client.get("/consdb/flex/latiss/exposure/obs/2024032100002?k=baz")
    _assert_http_status(response, 200)
    result = response.json
    assert result == {"baz": 2.71828}

    response = client.post("/consdb/flex/latiss/exposure/obs/2024032100002", json={})
    _assert_http_status(response, 404)
    result = response.json
    assert "Invalid JSON" in result["message"]
    assert result["required_keys"] == ["values"]

    response = client.post(
        "/consdb/insert/latiss",
        json={
            "table": "exposure",
            "values": {
                "exposure_name": "AT_O_20240327_000002",
                "controller": "O",
                "day_obs": 20240327,
                "seq_num": 2,
            },
            "obs_id": 2024032700002,
        },
    )
    _assert_http_status(response, 200)
    result = response.json
    assert result == {
        "message": "Data inserted",
        "table": "cdb_latiss.exposure",
        "instrument": "latiss",
    }

    response = client.post("/consdb/query", json={"query": "SELECT * FROM exposure ORDER BY day_obs;"})
    _assert_http_status(response, 200)
    result = response.json
    assert len(result) == 2
    assert "exposure_id" in result["columns"]
    assert 20240321 in result["data"][0]
    assert "AT_O_20240327_000002" in result["data"][1]
