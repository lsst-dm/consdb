import os
from pathlib import Path

import pytest
import sqlalchemy as sa
import yaml
from fastapi.testclient import TestClient
from felis.datamodel import Schema
from felis.db.utils import DatabaseContext
from felis.metadata import MetaDataBuilder
from felis.tests.postgresql import setup_postgres_test_db
from lsst.consdb import pqserver
from lsst.consdb.cdb_schema import ObsIdColname
from lsst.consdb.config import config
from lsst.consdb.dependencies import reset_dependencies


def _assert_http_status(response, status: int) -> None:
    assert response.status_code == status, f"{response.status_code} {response.json()}"


@pytest.fixture(scope="module")
def lsstcam_client():
    reset_dependencies()
    schema_name = "cdb_lsstcam"
    schema_file = Path(os.environ["SDM_SCHEMAS_DIR"]) / "yml" / f"{schema_name}.yaml"

    with schema_file.open() as f:
        yaml_data = yaml.safe_load(f)
    schema = Schema.model_validate(yaml_data)
    md = MetaDataBuilder(schema).build()

    with setup_postgres_test_db() as instance:
        os.environ["POSTGRES_URL"] = instance.url
        config.postgres_url = instance.url

        context = DatabaseContext(md, instance.engine)
        context.initialize()
        context.create_all()

        client = TestClient(pqserver.app)
        client.engine = instance.engine
        client.schema_name = schema_name
        yield client


@pytest.fixture(scope="module")
def lsstcam_tables(lsstcam_client):
    md = sa.MetaData(schema=lsstcam_client.schema_name)
    md.reflect(lsstcam_client.engine, views=True)
    table_names = sorted(md.tables.keys())
    table_names = [name for name in table_names if "flexdata" not in name]
    return md, _topo_sort_tables(md, table_names)


@pytest.fixture
def row_builder(lsstcam_tables):
    md, _ = lsstcam_tables
    rows_by_table: dict[str, dict[str, object]] = {}

    def _builder(table_name: str, seed: int) -> dict[str, object]:
        table = md.tables[table_name]
        row = _build_row(table, seed, rows_by_table)
        rows_by_table[table_name] = row
        return row

    return _builder


def _topo_sort_tables(md: sa.MetaData, table_names: list[str]) -> list[str]:
    deps = {name: set() for name in table_names}
    for name in table_names:
        table = md.tables[name]
        for fk in table.foreign_keys:
            ref_table = fk.column.table
            ref_name = f"{ref_table.schema}.{ref_table.name}"
            if ref_name in deps:
                deps[name].add(ref_name)

    ordered = []
    ready = [name for name, refs in deps.items() if not refs]
    while ready:
        name = ready.pop()
        ordered.append(name)
        for other, refs in deps.items():
            if name in refs:
                refs.remove(name)
                if not refs and other not in ordered and other not in ready:
                    ready.append(other)

    if len(ordered) != len(table_names):
        remaining = [name for name in table_names if name not in ordered]
        ordered.extend(remaining)

    return ordered


def _ids_for_seed(seed: int) -> dict[str, int]:
    exposure_id = 7000000000000 + seed * 1000
    ccdexposure_id = exposure_id * 100 + (seed + 1)
    return {
        "exposure_id": exposure_id,
        "visit_id": exposure_id,
        "obs_id": exposure_id,
        "ccdexposure_id": ccdexposure_id,
        "ccdvisit_id": ccdexposure_id,
    }


def _string_value(table_name: str, column_name: str, length: int | None, seed: int) -> str:
    value = f"{table_name}_{column_name}_{seed}"
    if length is not None:
        value = value[: max(1, length)]
    return value


def _default_value(column: sa.Column, table_name: str, seed: int) -> object:
    col_name = column.name
    ids = _ids_for_seed(seed)
    day_obs = 20240101 + seed
    seq_num = 1 + seed
    detector = seed

    if col_name in ids:
        return ids[col_name]
    if col_name == "day_obs":
        return day_obs
    if col_name == "seq_num":
        return seq_num
    if col_name == "detector":
        return detector

    col_type = column.type
    if isinstance(col_type, (sa.Integer, sa.BigInteger, sa.SmallInteger)):
        return seed + 1
    if isinstance(col_type, (sa.Float, sa.Numeric)):
        return 0.0
    if isinstance(col_type, sa.Boolean):
        return False
    if isinstance(col_type, sa.DateTime):
        return "2024-01-01T00:00:00"
    if isinstance(col_type, sa.Date):
        return "2024-01-01"
    if isinstance(col_type, sa.Time):
        return "00:00:00"
    if isinstance(col_type, (sa.String, sa.Text)):
        length = getattr(col_type, "length", None)
        return _string_value(table_name, col_name, length, seed)

    return _string_value(table_name, col_name, None, seed)


def _build_row(table: sa.Table, seed: int, rows_by_table: dict[str, dict[str, object]]) -> dict[str, object]:
    table_name = f"{table.schema}.{table.name}"
    row = {col.name: _default_value(col, table_name, seed) for col in table.columns}

    for fk in table.foreign_keys:
        ref_table = fk.column.table
        ref_name = f"{ref_table.schema}.{ref_table.name}"
        if ref_name not in rows_by_table:
            continue
        ref_row = rows_by_table[ref_name]
        row[fk.parent.name] = ref_row[fk.column.name]

    return row


def _obs_id_column(table: sa.Table) -> str:
    for col_name in ObsIdColname:
        if col_name.value in table.columns:
            return col_name.value
    raise AssertionError(f"No obs_id column found for {table.schema}.{table.name}")


def _by_seq_path(instrument: str, table_name: str, row: dict[str, object], has_detector: bool) -> str:
    path = f"/consdb/insert/{instrument}/{table_name}/by_seq_num/{row['day_obs']}/{row['seq_num']}"
    if has_detector:
        path += f"/{row['detector']}"
    return path


def _insert_path(instrument: str, table_name: str, obs_id: int) -> str:
    return f"/consdb/insert/{instrument}/{table_name}/obs/{obs_id}"


def _insert_multiple_path(instrument: str, table_name: str) -> str:
    return f"/consdb/insert/{instrument}/{table_name}"


def _call_insert_by_seq(client: TestClient, table_name: str, table: sa.Table, row: dict[str, object], u: int):
    path = _by_seq_path("lsstcam", table_name, row, "detector" in table.columns)
    response = client.post(path, params={"u": u}, json={"values": row})
    _assert_http_status(response, 200)


def _call_insert(client: TestClient, table_name: str, table: sa.Table, row: dict[str, object], u: int):
    obs_id_col = _obs_id_column(table)
    path = _insert_path("lsstcam", table_name, int(row[obs_id_col]))
    response = client.post(path, params={"u": u}, json={"values": row})
    _assert_http_status(response, 200)


def _call_insert_multiple(
    client: TestClient, table_name: str, table: sa.Table, row: dict[str, object], u: int
):
    obs_id_col = _obs_id_column(table)
    obs_id = int(row[obs_id_col])
    path = _insert_multiple_path("lsstcam", table_name)
    response = client.post(path, params={"u": u}, json={"obs_dict": {obs_id: row}})
    _assert_http_status(response, 200)


def test_insert_by_seq_num(lsstcam_client, lsstcam_tables, row_builder):
    md, table_names = lsstcam_tables
    for table_name in table_names:
        table = md.tables[table_name]
        row = row_builder(table_name, seed=0)
        _call_insert_by_seq(lsstcam_client, table_name, table, row, u=0)
        _call_insert_by_seq(lsstcam_client, table_name, table, row, u=1)


def test_insert_single(lsstcam_client, lsstcam_tables, row_builder):
    md, table_names = lsstcam_tables
    for table_name in table_names:
        table = md.tables[table_name]
        row = row_builder(table_name, seed=1)
        _call_insert(lsstcam_client, table_name, table, row, u=0)
        _call_insert(lsstcam_client, table_name, table, row, u=1)


def test_insert_multiple(lsstcam_client, lsstcam_tables, row_builder):
    md, table_names = lsstcam_tables
    for table_name in table_names:
        table = md.tables[table_name]
        row = row_builder(table_name, seed=2)
        _call_insert_multiple(lsstcam_client, table_name, table, row, u=0)
        _call_insert_multiple(lsstcam_client, table_name, table, row, u=1)
