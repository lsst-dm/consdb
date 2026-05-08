"""End-to-end coverage for the /insert/ endpoint family against the
``cdb_lsstcam`` schema.

The tests walk every non-flexdata table in topological FK order and POST a
synthetic row through each of the three endpoint shapes (``by_seq_num``,
``/obs/{obs_id}``, bulk), checking that the API accepts the insert and the
follow-up upsert (``u=1``). Synthetic rows are generated deterministically
from a seed so different test functions can run against the same module-
scoped database without colliding.
"""

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
    """Assert an HTTP response code, surfacing the JSON body on mismatch."""
    assert response.status_code == status, f"{response.status_code} {response.json()}"


@pytest.fixture(scope="module")
def lsstcam_client():
    """FastAPI TestClient wired to a fresh temporary Postgres instance.

    The instance is loaded with the ``cdb_lsstcam`` schema as-built from
    Felis (no Alembic migrations); ``client.engine`` is exposed so tests
    can reach the DB directly when they need to bypass the API.
    """
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
    """Return ``(MetaData, topo-sorted table names)`` for the schema.

    Reflects the live DB (so SQL views are included), drops flexdata tables
    — those have their own endpoint family and aren't covered here — and
    sorts the remaining tables so every parent precedes its children. The
    sorted order is what the per-test loops iterate over.
    """
    md = sa.MetaData(schema=lsstcam_client.schema_name)
    md.reflect(lsstcam_client.engine, views=True)
    table_names = sorted(md.tables.keys())
    table_names = [name for name in table_names if "flexdata" not in name]
    return md, _topo_sort_tables(md, table_names)


@pytest.fixture
def row_builder(lsstcam_tables):
    """Per-test row factory that resolves FK columns to previously-built rows.

    Each call records the produced row so later calls within the same test
    can pull matching FK values out of it. Function-scoped on purpose: the
    cache should not leak across tests, even though the underlying DB
    state does (the ``lsstcam_client`` fixture is module-scoped).
    """
    md, _ = lsstcam_tables
    rows_by_table: dict[str, dict[str, object]] = {}

    def _builder(table_name: str, seed: int) -> dict[str, object]:
        table = md.tables[table_name]
        row = _build_row(table, seed, rows_by_table)
        rows_by_table[table_name] = row
        return row

    return _builder


def _topo_sort_tables(md: sa.MetaData, table_names: list[str]) -> list[str]:
    """Order tables so each appears after every table it FKs to.

    Implemented as Kahn's algorithm over the FK graph restricted to
    ``table_names`` (foreign keys to outside-the-set tables are ignored).
    If a cycle leaves some tables un-ordered they're appended at the end,
    in case the suite still wants to attempt them rather than fail to start.
    """
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
    """Map natural-id column names to seeded values.

    ``exposure_id``, ``visit_id``, and ``obs_id`` share one synthetic id
    because the schema treats visits as views of exposures with the column
    renamed; ``ccdexposure_id`` and ``ccdvisit_id`` similarly share a
    second one derived from the first.
    """
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
    """Build a deterministic, length-clipped string for a column."""
    value = f"{table_name}_{column_name}_{seed}"
    if length is not None:
        value = value[: max(1, length)]
    return value


def _default_value(column: sa.Column, table_name: str, seed: int) -> object:
    """Choose a synthetic value for a single column based on the seed.

    Composite-key columns (``day_obs``, ``seq_num``, ``detector``) and
    natural-id columns (``exposure_id``, ``visit_id``, ...) get
    seed-derived integers so multiple rows generated from the same seed
    line up across parent/child tables. Other columns fall back to a
    minimal-but-valid value for their SQL type.
    """
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
    """Construct a single row dict for ``table``, FK-aligned to known parents.

    Starts from ``_default_value`` for every column, then walks the table's
    foreign keys and overwrites each FK column with the corresponding value
    from the already-built parent row in ``rows_by_table``. Parents missing
    from the cache are left at their default — which is fine when the parent
    table isn't being inserted in this test.
    """
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
    """Return the natural-id column name for a table.

    Iterates the ``ObsIdColname`` enum and returns the first member whose
    value names an existing column; raises if none match. Mirrors the
    server-side ``InstrumentTable.obs_id_column`` mapping.
    """
    for col_name in ObsIdColname:
        if col_name.value in table.columns:
            return col_name.value
    raise AssertionError(f"No obs_id column found for {table.schema}.{table.name}")


def _by_seq_path(instrument: str, table_name: str, row: dict[str, object], has_detector: bool) -> str:
    """URL for the ``by_seq_num`` endpoint family, with optional detector."""
    path = f"/consdb/insert/{instrument}/{table_name}/by_seq_num/{row['day_obs']}/{row['seq_num']}"
    if has_detector:
        path += f"/{row['detector']}"
    return path


def _insert_path(instrument: str, table_name: str, obs_id: int) -> str:
    """URL for the ``/obs/{obs_id}`` per-row endpoint."""
    return f"/consdb/insert/{instrument}/{table_name}/obs/{obs_id}"


def _insert_multiple_path(instrument: str, table_name: str) -> str:
    """URL for the bulk ``/insert/{instrument}/{table}`` endpoint."""
    return f"/consdb/insert/{instrument}/{table_name}"


def _call_insert_by_seq(client: TestClient, table_name: str, table: sa.Table, row: dict[str, object], u: int):
    """POST one row via ``by_seq_num``, picking the 2- or 3-segment variant."""
    path = _by_seq_path("lsstcam", table_name, row, "detector" in table.columns)
    response = client.post(path, params={"u": u}, json={"values": row})
    _assert_http_status(response, 200)


def _call_insert(client: TestClient, table_name: str, table: sa.Table, row: dict[str, object], u: int):
    """POST one row via ``/obs/{obs_id}``."""
    obs_id_col = _obs_id_column(table)
    path = _insert_path("lsstcam", table_name, int(row[obs_id_col]))
    response = client.post(path, params={"u": u}, json={"values": row})
    _assert_http_status(response, 200)


def _call_insert_multiple(
    client: TestClient, table_name: str, table: sa.Table, row: dict[str, object], u: int
):
    """POST one row as a single-entry ``obs_dict`` via the bulk endpoint."""
    obs_id_col = _obs_id_column(table)
    obs_id = int(row[obs_id_col])
    path = _insert_multiple_path("lsstcam", table_name)
    response = client.post(path, params={"u": u}, json={"obs_dict": {obs_id: row}})
    _assert_http_status(response, 200)


def test_insert_by_seq_num(lsstcam_client, lsstcam_tables, row_builder):
    """Exercise the ``by_seq_num`` endpoint family across every table.

    Walks the topo-sorted table list; for each table inserts a row with
    ``u=0`` and re-inserts with ``u=1`` to verify both insert and upsert.
    """
    md, table_names = lsstcam_tables
    for table_name in table_names:
        table = md.tables[table_name]
        row = row_builder(table_name, seed=0)
        _call_insert_by_seq(lsstcam_client, table_name, table, row, u=0)
        _call_insert_by_seq(lsstcam_client, table_name, table, row, u=1)


def test_insert_single(lsstcam_client, lsstcam_tables, row_builder):
    """Exercise the ``/obs/{obs_id}`` endpoint across every table.

    Same insert+upsert pattern as ``test_insert_by_seq_num`` but goes
    through the per-row natural-id endpoint instead.
    """
    md, table_names = lsstcam_tables
    for table_name in table_names:
        table = md.tables[table_name]
        row = row_builder(table_name, seed=1)
        _call_insert(lsstcam_client, table_name, table, row, u=0)
        _call_insert(lsstcam_client, table_name, table, row, u=1)


def test_insert_multiple(lsstcam_client, lsstcam_tables, row_builder):
    """Exercise the bulk ``/insert/{instrument}/{table}`` endpoint."""
    md, table_names = lsstcam_tables
    for table_name in table_names:
        table = md.tables[table_name]
        row = row_builder(table_name, seed=2)
        _call_insert_multiple(lsstcam_client, table_name, table, row, u=0)
        _call_insert_multiple(lsstcam_client, table_name, table, row, u=1)
