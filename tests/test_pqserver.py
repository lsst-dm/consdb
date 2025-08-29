import os
from pathlib import Path

import lsst.utils
import numpy as np
import pytest
import sqlalchemy as sa
import yaml
from astropy.table import Table
from astropy.time import Time
from fastapi.testclient import TestClient
from felis.datamodel import Schema
from felis.db.utils import DatabaseContext
from felis.metadata import MetaDataBuilder
from felis.tests.postgresql import setup_postgres_test_db
from lsst.consdb import pqserver
from lsst.consdb.config import config
from lsst.consdb.dependencies import reset_dependencies
from requests import Response


def _assert_http_status(response: Response, status: int):
    assert response.status_code == status, f"{response.status_code} {response.json()}"


@pytest.fixture
def astropy_tables(scope="module"):
    t = dict()
    return t


@pytest.fixture
def lsstcomcamsim(request, astropy_tables, scope="module"):
    reset_dependencies()
    schema_name = request.param if hasattr(request, "param") else "cdb_lsstcomcamsim"
    data_path = Path(__file__).parent / "lsstcomcamsim"

    schema_file = os.path.join(lsst.utils.getPackageDir("sdm_schemas"), "yml", schema_name + ".yaml")

    with open(schema_file) as f:
        yaml_data = yaml.safe_load(f)
    schema = Schema.model_validate(yaml_data)
    md = MetaDataBuilder(schema).build()

    with setup_postgres_test_db() as instance:
        os.environ["POSTGRES_URL"] = instance.url
        config.postgres_url = instance.url

        context = DatabaseContext(md, instance.engine)
        context.initialize()
        context.create_all()

        table_dict = {
            "exposure.ecsv": "exposure",
            "exposure2.ecsv": "exposure",
            "ccdexposure.ecsv": "ccdexposure",
            "ccdvisit1_quicklook.ecsv": "ccdvisit1_quicklook",
            "visit1_quicklook.ecsv": "visit1_quicklook",
            "exposure_flexdata_schema.ecsv": "exposure_flexdata_schema",
            "ccdexposure_flexdata_schema.ecsv": "ccdexposure_flexdata_schema",
            "exposure_flexdata.ecsv": "exposure_flexdata",
            "ccdexposure_flexdata.ecsv": "ccdexposure_flexdata",
        }

        for file_name, table_name in table_dict.items():
            astropy_table = Table.read(data_path / file_name)
            astropy_tables[file_name] = astropy_table
            metadata = sa.MetaData()

            sql_table = sa.Table(table_name, metadata, schema=schema_name, autoload_with=instance.engine)

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

            fk_column = {
                "ccdexposure": "exposure_id",
                "visit1_quicklook": "visit_id",
                "exposure_flexdata": "obs_id",
            }
            with instance.engine.begin() as connection:
                if table_name in fk_column.keys() and "day_obs" in sql_table.columns:
                    # Adjust for multi-column primary keys
                    exposure_table = sa.Table(
                        "exposure", metadata, schema=schema_name, autoload_with=instance.engine
                    )
                    for row in rows:
                        stmt = sa.select(exposure_table.c["day_obs", "seq_num"]).where(
                            exposure_table.c.exposure_id == row[fk_column[table_name]]
                        )
                        query_result = connection.execute(stmt).first()

                        row["day_obs"] = query_result.day_obs
                        row["seq_num"] = query_result.seq_num

                # Insert rows into the SQL table
                connection.execute(sql_table.insert(), rows)

        with instance.engine.begin() as connection:
            connection.exec_driver_sql(
                f"DROP TABLE IF EXISTS {schema_name}.visit1;"
                f" CREATE VIEW {schema_name}.visit1 AS SELECT * FROM {schema_name}.exposure;"
            )

            client = TestClient(pqserver.app)
            client.connection = connection
            yield client


@pytest.fixture
def app(db, scope="module"):
    os.environ["POSTGRES_URL"] = f"sqlite:///{db}"
    from lsst.consdb import pqserver, utils

    pqserver.engine = utils.setup_postgres()
    pqserver.instrument_tables = pqserver.InstrumentTables()

    yield pqserver.app


def test_root(lsstcomcamsim):
    response = lsstcomcamsim.get("/")
    result = response.json()
    assert "instruments" in result
    assert "obs_types" in result
    assert "dtypes" in result


@pytest.mark.parametrize("lsstcomcamsim", ["cdb_latiss"], indirect=True)
def test_root2(lsstcomcamsim, request):
    response = lsstcomcamsim.get("/consdb")
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
    response = lsstcomcamsim.get("/consdb")
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
        "visit1",
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


@pytest.mark.parametrize("lsstcomcamsim", ["cdb_latiss"], indirect=True)
def test_query_endpoint(lsstcomcamsim):
    client = lsstcomcamsim

    # A simple test of the query endpoint.
    response = client.post(
        "/consdb/query",
        json={"query": "SELECT 1;"},
    )
    _assert_http_status(response, 200)
    assert response.json() == {
        "columns": ["?column?"],
        "data": [[1]],
    }

    # Modify the database, but with commit=0. The
    # actual content of the database should not be
    # changed.
    response = client.post(
        "/consdb/query?commit=0",
        json={"query": "DELETE FROM cdb_latiss.ccdexposure_flexdata;"},
    )
    _assert_http_status(response, 200)
    assert response.json() == {
        "columns": ["commit"],
        "data": [[0]],
    }

    # Check that the rows are still present in the database
    response = client.post(
        "/consdb/query?commit=0",
        json={"query": "SELECT count(*) FROM cdb_latiss.ccdexposure_flexdata;"},
    )
    _assert_http_status(response, 200)
    response_json = response.json()
    assert response_json["data"][0][0] != 0

    # Run the query again with commit=1.
    response = client.post(
        "/consdb/query?commit=1",
        json={"query": "DELETE FROM cdb_latiss.ccdexposure_flexdata;"},
    )
    _assert_http_status(response, 200)
    assert response.json() == {
        "columns": ["commit"],
        "data": [[1]],
    }

    # This time, the rows were deleted, because commit=1.
    response = client.post(
        "/consdb/query?commit=0",
        json={"query": "SELECT count(*) FROM cdb_latiss.ccdexposure_flexdata;"},
    )
    _assert_http_status(response, 200)
    response_json = response.json()
    assert response_json["data"][0][0] == 0


@pytest.mark.parametrize("lsstcomcamsim", ["cdb_latiss"], indirect=True)
def test_missing_primary_key(lsstcomcamsim):
    client = lsstcomcamsim

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

    # Add n_inputs to the visit1_quicklook table
    response = client.post(
        "/consdb/insert/latiss/visit1_quicklook/by_seq_num/20240327/2",
        json={
            "values": {
                "visit_id": 2024032100003,
                "n_inputs": 12345,
            },
        },
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Data inserted",
        "table": "cdb_latiss.visit1_quicklook",
        "instrument": "latiss",
        "obs_id": [20240327, 2],
    }

    # Verify the result in the database
    query_result = client.connection.execute(
        sa.text("SELECT n_inputs FROM cdb_latiss.visit1_quicklook WHERE day_obs = 20240327 AND seq_num = 2")
    ).scalar_one_or_none()
    assert query_result == 12345

    # Modify n_inputs
    response = client.post(
        "/consdb/insert/latiss/visit1_quicklook/by_seq_num/20240327/2?u=1",
        json={
            "values": {
                "visit_id": 2024032100003,
                "n_inputs": 54321,
            },
        },
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Data inserted",
        "table": "cdb_latiss.visit1_quicklook",
        "instrument": "latiss",
        "obs_id": [20240327, 2],
    }

    # Verify that the database was modified
    query_result = client.connection.execute(
        sa.text("SELECT n_inputs FROM cdb_latiss.visit1_quicklook WHERE day_obs = 20240327 AND seq_num = 2")
    ).scalar_one_or_none()
    assert query_result == 54321

    response = client.post(
        "/consdb/insert/latiss/ccdexposure/obs/8675309",
        json={
            "values": {
                "s_region": "testregion",
                "exposure_id": 2024032100003,
                "detector": 0,
            },
        },
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Data inserted",
        "table": "cdb_latiss.ccdexposure",
        "instrument": "latiss",
        "obs_id": 8675309,
    }


def test_validate_unit():
    from lsst.consdb import models

    model = models.AddKeyRequestModel(key="foo", dtype="float", unit="s")
    assert model.unit == "s"

    model = models.AddKeyRequestModel(key="foo", dtype="float", unit="km/s")
    assert model.unit == "km/s"

    model = models.AddKeyRequestModel(key="foo", dtype="float", unit="km s-1")
    assert model.unit == "km s-1"

    with pytest.raises(ValueError) as exc_info:
        models.AddKeyRequestModel(key="foo", dtype="float", unit="tacos / s")
    assert "unit" in str(exc_info.value)


def test_validate_ucd():
    from lsst.consdb import models

    model = models.AddKeyRequestModel(key="foo", dtype="float", ucd="this.is.a.valid.ucd")
    assert model.ucd == "this.is.a.valid.ucd"
    model = models.AddKeyRequestModel(key="foo", dtype="float", ucd="THIS-ONE.IS.TOO")
    assert model.ucd == "THIS-ONE.IS.TOO"

    with pytest.raises(ValueError) as exc_info:
        models.AddKeyRequestModel(key="foo", dtype="float", ucd="but this is not")
    assert "ucd" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        models.AddKeyRequestModel(key="foo", dtype="float", ucd="neither#is@this[one]!")
    assert "ucd" in str(exc_info.value)


@pytest.mark.parametrize("lsstcomcamsim", ["cdb_latiss"], indirect=True)
def test_flexible_metadata(lsstcomcamsim):
    client = lsstcomcamsim

    response = client.post(
        "/consdb/flex/latiss/exposure/addkey",
        json={"key": "foo2", "dtype": "bool", "doc": "new bool key"},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Key added to flexible metadata",
        "key": "foo2",
        "instrument": "latiss",
        "obs_type": "exposure",
    }

    response = client.post(
        "/consdb/flex/LATISS/exposure/addkey",
        json={"key": "bar2", "dtype": "int", "doc": "int key"},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "message": "Key added to flexible metadata",
        "key": "bar2",
        "instrument": "latiss",
        "obs_type": "exposure",
    }

    response = client.post(
        "/consdb/flex/latiss/Exposure/addkey",
        json={"key": "baz2", "dtype": "float", "doc": "float key 2"},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result["obs_type"] == "exposure"

    response = client.post(
        "/consdb/flex/bad_instrument/exposure/addkey",
        json={"key": "quux2", "dtype": "str", "doc": "str key"},
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
    assert result["baz2"] == ["float", "float key 2", None, None]
    assert "foo2" in result
    assert "bar2" in result
    assert "baz2" in result

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/7024040300451",
        json={"values": {"foo2": True, "bar2": 42, "baz2": 3.14159}},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result["message"] == "Flexible metadata inserted"
    assert result["obs_id"] == 7024040300451

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/7024040300451",
        json={"values": {"foo2": True, "bar2": 42, "baz2": 3.14159}},
    )
    _assert_http_status(response, 500)
    result = response.json()
    assert "already exists" in result["message"]

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/7024040300451",
        json={"values": {"bad_key": 2.71828}},
    )
    _assert_http_status(response, 404)
    result = response.json()
    assert result["message"] == "Unknown key"
    assert result["value"] == "bad_key"

    response = client.get("/consdb/flex/latiss/exposure/obs/7024040300451")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {
        "bar": 1234,
        "bar2": 42,
        "baz": 3.14,
        "baz2": 3.14159,
        "foo": True,
        "foo2": True,
        "qux": "nachos",
    }

    response = client.get("/consdb/flex/latiss/exposure/obs/7024040300451?k=bar2&k=baz2")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {"bar2": 42, "baz2": 3.14159}

    response = client.post(
        "/consdb/flex/latiss/exposure/obs/7024052800003?u=1",
        json={"values": {"foo": False, "bar": 34, "baz": 2.71828}},
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert result["message"] == "Flexible metadata inserted"

    response = client.get("/consdb/flex/latiss/exposure/obs/7024052800003")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {"foo": False, "bar": 34, "baz": 2.71828, "qux": "burritos"}  # Qux loaded by fixture

    response = client.get("/consdb/flex/latiss/exposure/obs/7024052800003?k=baz")
    _assert_http_status(response, 200)
    result = response.json()
    assert result == {"baz": 2.71828}

    response = client.post("/consdb/flex/latiss/exposure/obs/7024052800003", json={})
    _assert_http_status(response, 422)
    result = response.json()["detail"][0]
    assert "Field required" in result["msg"]
    assert result["type"] == "missing"
    assert "values" in result["loc"]
    assert "body" in result["loc"]

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

    response = client.post(
        "/consdb/query", json={"query": "SELECT * FROM cdb_latiss.exposure ORDER BY day_obs;"}
    )
    _assert_http_status(response, 200)
    result = response.json()
    assert len(result) == 2
    assert "exposure_id" in result["columns"]
    assert 2024032100003 in result["data"][0]
    assert "CC_S_20240403_000451" in result["data"][1]
