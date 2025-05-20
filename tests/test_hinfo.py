import os
from pathlib import Path

import lsst.utils
import pytest
import sqlalchemy as sa
import yaml
from felis.datamodel import Schema
from felis.db.utils import DatabaseContext
from felis.metadata import MetaDataBuilder
from felis.tests.postgresql import setup_postgres_test_db
from lsst.consdb import hinfo
from lsst.resources import ResourcePath
from sqlalchemy import MetaData, select


@pytest.fixture
def pg_engine(request, scope="module"):
    schema_name = request.param if hasattr(request, "param") else "cdb_latiss"

    schema_file = os.path.join(lsst.utils.getPackageDir("sdm_schemas"), "yml", schema_name + ".yaml")

    with open(schema_file) as f:
        yaml_data = yaml.safe_load(f)
    schema = Schema.model_validate(yaml_data)
    md = MetaDataBuilder(schema).build()

    with setup_postgres_test_db() as instance:
        context = DatabaseContext(md, instance.engine)
        context.initialize()
        context.create_all()

        hinfo.engine = instance.engine
        hinfo.instrument = "LATISS"

        yield hinfo.engine


def _header_lookup(header, key):
    for line in header:
        if line["keyword"] == key:
            return line["value"]
    return None


def test_process_resource(pg_engine):
    yaml_path = Path(__file__).parent / "ATHeaderService_header_AT_O_20240801_000302.yaml"
    rp = ResourcePath(yaml_path)

    with open(yaml_path, "r") as f:
        header = yaml.safe_load(f)["PRIMARY"]

    instrument_dict = hinfo.get_instrument_dict("LATISS")
    hinfo.process_resource(rp, instrument_dict)

    metadata_obj = MetaData(schema="cdb_latiss")
    exposure_table = sa.Table("exposure", metadata_obj, autoload_with=pg_engine)
    with pg_engine.begin() as conn:
        row = conn.execute(select(exposure_table)).first()

    assert _header_lookup(header, "OBSID") == row.exposure_name
    assert _header_lookup(header, "VIGN_MIN") == row.vignette_min
    assert _header_lookup(header, "DOMEAZ") == row.dome_azimuth
    assert _header_lookup(header, "OBSANNOT") == row.scheduler_note
