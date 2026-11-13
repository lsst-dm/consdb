import os
from pathlib import Path

import astropy.units as u
import lsst.utils
import pytest
import sqlalchemy as sa
import yaml
from felis.datamodel import Schema
from felis.db.database_context import create_database_context
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

    # Manually add the shadow column, since it is not listed in the schema.
    tables_to_modify = [t for t in md.tables.values() if t.name == "exposure" or t.name == "ccdexposure"]
    for table in tables_to_modify:
        table.append_column(sa.Column("pgs_region", sa.String(1024)))

    with setup_postgres_test_db() as instance:
        context = create_database_context(instance.engine.url, md)
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


def test_altaz_midpoint_uses_location():
    from astropy.coordinates import AltAz, EarthLocation, SkyCoord
    from astropy.time import Time
    from lsst.obs.lsst.translators.lsst import SIMONYI_LOCATION

    radec = SkyCoord(ra=150.0 * u.deg, dec=-30.0 * u.deg)
    t1 = Time("2026-05-11T03:00:00", scale="tai")
    t2 = Time("2026-05-11T03:00:30", scale="tai")
    begin = AltAz(az=10.0 * u.deg, alt=60.0 * u.deg)
    end = AltAz(az=12.0 * u.deg, alt=62.0 * u.deg)

    altaz = hinfo.altaz_midpoint(radec, t1, t2, begin, end, SIMONYI_LOCATION)
    expected = radec.transform_to(
        AltAz(obstime=Time("2026-05-11T03:00:15", scale="tai"), location=SIMONYI_LOCATION)
    )
    assert abs(altaz.alt - expected.alt).to_value(u.arcsec) < 1e-6
    assert abs(altaz.az - expected.az).to_value(u.arcsec) < 1e-6

    # A site 1.3 km away gives a measurably different result.
    other = EarthLocation(lat=-30.24074167 * u.deg, lon=-70.7366833 * u.deg, height=2750 * u.m)
    altaz_other = hinfo.altaz_midpoint(radec, t1, t2, begin, end, other)
    assert abs(altaz.alt - altaz_other.alt).to_value(u.arcsec) > 10

    # Without a location, fall back on the endpoints.
    fallback = hinfo.altaz_midpoint(radec, t1, t2, begin, end, None)
    assert fallback.alt.deg == pytest.approx(61.0, abs=0.01)
