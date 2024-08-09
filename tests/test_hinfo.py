import os
import shutil
import sqlite3
import tempfile
from pathlib import Path

import pytest
import yaml
from lsst.consdb import hinfo, utils
from lsst.resources import ResourcePath
from sqlalchemy import MetaData, Table, select


@pytest.fixture
def tmpdir(scope="module"):
    os.environ["INSTRUMENT"] = "LATISS"
    tmpdir = Path(tempfile.mkdtemp())
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


@pytest.fixture
def engine(tmpdir, scope="module"):
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

    os.environ["POSTGRES_URL"] = f"sqlite:///{db_path}"
    hinfo.engine = utils.setup_postgres()
    hinfo.instrument = "LATISS"

    try:
        yield hinfo.engine
    finally:
        hinfo.engine.dispose()


def _header_lookup(header, key):
    for line in header:
        if line["keyword"] == key:
            return line["value"]
    return None


def test_process_resource(engine):
    yaml_path = Path(__file__).parent / "ATHeaderService_header_AT_O_20240801_000302.yaml"
    rp = ResourcePath(yaml_path)

    with open(yaml_path, "r") as f:
        header = yaml.safe_load(f)["PRIMARY"]

    instrument_dict = hinfo.get_instrument_dict("LATISS")
    hinfo.process_resource(rp, instrument_dict)

    metadata_obj = MetaData(schema="cdb_latiss")
    exposure_table = Table("exposure", metadata_obj, autoload_with=engine)
    with engine.begin() as conn:
        row = conn.execute(select(exposure_table)).first()
        print(f"{row=}")
        print(f"{row.exposure_name=}")

    assert _header_lookup(header, "OBSID") == row.exposure_name
    assert _header_lookup(header, "VIGN_MIN") == row.vignette_min
    assert _header_lookup(header, "DOMEAZ") == row.dome_azimuth

    elstart = _header_lookup(header, "ELSTART")
    elend = _header_lookup(header, "ELEND")
    assert 0.5 * (elstart + elend) == row.zenith_distance
