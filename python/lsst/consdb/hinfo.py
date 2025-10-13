import asyncio
import os
import random
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Union

import aiokafka  # type: ignore
import astropy.time  # type: ignore
import astropy.units as u  # type: ignore
import httpx  # type: ignore
import kafkit.registry
import kafkit.registry.httpx  # type: ignore
import lsst.geom  # type: ignore
import lsst.obs.lsst  # type: ignore
import numpy as np  # type: ignore
import yaml
from astro_metadata_translator import ObservationInfo
from astropy.coordinates import AltAz, CartesianRepresentation, EarthLocation, SkyCoord  # type: ignore
from lsst.obs.lsst.rawFormatter import LsstCamRawFormatter  # type: ignore
from lsst.resources import ResourcePath
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert

from .utils import setup_logging, setup_postgres

if TYPE_CHECKING:
    import lsst.afw.cameraGeom  # type: ignore

###############################
# Header Processing Functions #
###############################


def logical_or(*bools: int | str | None) -> bool:
    return any([b == 1 or b == "1" for b in bools])


def region(
    camera: lsst.afw.cameraGeom.Camera,
    ra: float,
    dec: float,
    rotpa: float,
    points: list[tuple[str, int, int]],
) -> str:
    region = "Polygon ICRS"
    for detector, offset_x, offset_y in points:
        skywcs = LsstCamRawFormatter.makeRawSkyWcsFromBoresight(
            lsst.geom.SpherePoint(ra, dec, lsst.geom.degrees),
            rotpa * lsst.geom.degrees,
            camera[detector],
        )
        bbox = camera[detector].getBBox()
        x = bbox.getMinX() + bbox.getWidth() * offset_x
        y = bbox.getMinY() + bbox.getHeight() * offset_y
        point = skywcs.pixelToSky(x, y)
        region += f" {point.getLongitude().asDegrees():.6f} {point.getLatitude().asDegrees():.6f}"
    return region


def ccdexposure_id(
    translator: lsst.obs.lsst.translators.lsst.LsstBaseTranslator, exposure_id: int, detector: int
) -> int:
    # global logger
    det_exp_id = translator.compute_detector_exposure_id(exposure_id, detector)
    logger.debug(f"t={translator}, eid={exposure_id}, d={detector}, cid={det_exp_id}")
    return det_exp_id


def ccd_region(
    camera: lsst.afw.cameraGeom.Camera, imgtype: str, ra: float, dec: float, rotpa: float, ccdname: str
) -> str | None:
    if imgtype != "OBJECT":
        return None
    return region(
        camera,
        ra,
        dec,
        rotpa,
        [
            (ccdname, 0, 0),
            (ccdname, 1, 0),
            (ccdname, 1, 1),
            (ccdname, 0, 1),
        ],
    )


def fp_region(
    camera: lsst.afw.cameraGeom.Camera, imgtype: str, ra: float, dec: float, rotpa: float
) -> str | None:
    # global instrument
    if imgtype != "OBJECT":
        return None
    if instrument == "LATISS":
        corners = [
            ("RXX_S00", 0, 0),
            ("RXX_S00", 1, 0),
            ("RXX_S00", 1, 1),
            ("RXX_S00", 0, 1),
        ]
    elif instrument == "LSSTComCam" or instrument == "LSSTComCamSim":
        corners = [
            ("R22_S00", 0, 0),
            ("R22_S02", 1, 0),
            ("R22_S20", 0, 1),
            ("R22_S22", 1, 1),
        ]
    elif instrument == "LSSTCam":
        corners = [
            ("R01_S00", 0, 0),
            ("R03_S02", 1, 0),
            ("R03_S02", 1, 1),
            ("R04_SG1", 1, 0),
            ("R04_SG1", 1, 1),
            ("R04_SG0", 1, 0),
            ("R04_SG0", 1, 1),
            ("R14_S02", 1, 0),
            ("R34_S22", 1, 1),
            ("R34_S22", 0, 1),
            ("R44_SG1", 1, 1),
            ("R44_SG1", 0, 1),
            ("R44_SG0", 1, 1),
            ("R44_SG0", 0, 1),
            ("R43_S22", 1, 1),
            ("R41_S20", 0, 1),
            ("R41_S20", 0, 0),
            ("R40_SG1", 0, 1),
            ("R40_SG1", 0, 0),
            ("R40_SG0", 0, 1),
            ("R40_SG0", 0, 0),
            ("R30_S20", 0, 1),
            ("R10_S00", 0, 0),
            ("R10_S00", 1, 0),
            ("R00_SG1", 0, 0),
            ("R00_SG1", 1, 0),
            ("R00_SG0", 0, 0),
            ("R00_SG0", 1, 0),
        ]
    else:
        return None
    return region(camera, ra, dec, rotpa, corners)


#################################
# Header Mapping Configurations #
#################################

ColumnMapping = Union[str, tuple[Callable[..., Any], *tuple[str, ...]]]

# Non-instrument-specific mapping to column name from Header Service keyword
KW_MAPPING: dict[str, ColumnMapping] = {
    "controller": "CONTRLLR",
    "band": "FILTBAND",
    "wind_speed": "WINDSPD",
    "wind_dir": "WINDDIR",
    "dimm_seeing": "SEEING",
    "vignette": "VIGNETTE",
    "vignette_min": "VIGN_MIN",
    "scheduler_note": "OBSANNOT",
    "s_region": (fp_region, "camera", "IMGTYPE", "RA", "DEC", "ROTPA"),
}

# Instrument-specific mapping to column name from Header Service keyword
LATISS_MAPPING: dict[str, ColumnMapping] = {
    "dome_azimuth": "DOMEAZ",
    "shut_lower": "SHUTLOWR",
    "shut_upper": "SHUTUPPR",
    "simulated": (
        logical_or,
        "SIMULATE ATMCS",
        "SIMULATE ATHEXAPOD",
        "SIMULATE ATPNEUMATICS",
        "SIMULATE ATDOME",
        "SIMULATE ATSPECTROGRAPH",
    ),
}

LSSTCOMCAMSIM_MAPPING: dict[str, ColumnMapping] = {
    "simulated": (
        logical_or,
        "SIMULATE MTMOUNT",
        "SIMULATE MTM1M3",
        "SIMULATE MTM2",
        "SIMULATE CAMHEXAPOD",
        "SIMULATE M2HEXAPOD",
        "SIMULATE MTROTATOR",
        "SIMULATE MTDOME",
        "SIMULATE MTDOMETRAJECTORY",
    ),
}

LSSTCOMCAM_MAPPING: dict[str, ColumnMapping] = {
    "simulated": (
        logical_or,
        "SIMULATE MTMOUNT",
        "SIMULATE MTM1M3",
        "SIMULATE MTM2",
        "SIMULATE CAMHEXAPOD",
        "SIMULATE M2HEXAPOD",
        "SIMULATE MTROTATOR",
        "SIMULATE MTDOME",
        "SIMULATE MTDOMETRAJECTORY",
    ),
}

LSSTCAM_MAPPING: dict[str, ColumnMapping] = {
    "simulated": (
        logical_or,
        "SIMULATE MTMOUNT",
        "SIMULATE MTM1M3",
        "SIMULATE MTM2",
        "SIMULATE CAMHEXAPOD",
        "SIMULATE M2HEXAPOD",
        "SIMULATE MTROTATOR",
        "SIMULATE MTDOME",
        "SIMULATE MTDOMETRAJECTORY",
    ),
}

DETECTOR_MAPPING: dict[str, ColumnMapping] = {
    "ccdexposure_id": (ccdexposure_id, "translator", "exposure_id", "detector"),
    "exposure_id": "exposure_id",
    "detector": "detector",
    "s_region": (ccd_region, "camera", "IMGTYPE", "RA", "DEC", "ROTPA", "ccdname"),
}


def time_midpoint(t1: astropy.time.Time, t2: astropy.time.Time) -> astropy.time.Time:
    return t1 + (t2 - t1) / 2


cerro_pachon = EarthLocation(lat=-30.24074167 * u.deg, lon=-70.7366833 * u.deg, height=2750 * u.m)


def altaz_midpoint_from_radec(
    tracking_radec: SkyCoord, t1: astropy.time.Time, t2: astropy.time.Time
) -> AltAz:
    """Return the AltAz of *tracking_radec* at the midpoint of *t1* and *t2*.

    Parameters
    ----------
    tracking_radec : `~astropy.coordinates.SkyCoord`
        Target position in an ICRS-like frame (e.g., RA/Dec).
    t1, t2 : `~astropy.time.Time`
        Start and end times.

    Returns
    -------
    `~astropy.coordinates.AltAz`
        Altitude–azimuth coordinates at the midpoint, using the global
        *cerro_pachon* (Cerro Pachón).
    """
    global cerro_pachon
    altaz_frame = AltAz(obstime=time_midpoint(t1, t2), location=cerro_pachon)
    return tracking_radec.transform_to(altaz_frame)


def altaz_midpoint_from_altaz(altaz_begin: AltAz, altaz_end: AltAz) -> AltAz:
    """Return the AltAz midway between `altaz_begin` and `altaz_end`.

    Parameters
    ----------
    altaz_begin : `~astropy.coordinates.AltAz`
        The starting AltAz coordinate.
    altaz_end : `~astropy.coordinates.AltAz`
        The ending AltAz coordinate.

    Returns
    -------
    `~astropy.coordinates.AltAz`
        Altitude–azimuth coordinates at the midpoint.
    """
    cartesian_begin = altaz_begin.represent_as(CartesianRepresentation)
    cartesian_end = altaz_end.represent_as(CartesianRepresentation)

    midpoint = cartesian_begin + cartesian_end
    midpoint = midpoint / midpoint.norm()

    return AltAz(midpoint)


def altaz_midpoint(
    tracking_radec: SkyCoord,
    datetime_begin: astropy.time.Time,
    datetime_end: astropy.time.Time,
    altaz_begin: AltAz,
    altaz_end: AltAz,
) -> AltAz:
    """Return the AltAz using tracking_radec falling back on the endpoints.

    Parameters
    ----------
    tracking_radec : `~astropy.coordinates.SkyCoord`
        Target position in an ICRS-like frame (e.g., RA/Dec).
    t1, t2 : `~astropy.time.Time`
        Start and end times.
    altaz_begin : `~astropy.coordinates.AltAz`
        The starting AltAz coordinate.
    altaz_end : `~astropy.coordinates.AltAz`
        The ending AltAz coordinate.

    Returns
    -------
    `~astropy.coordinates.AltAz`
        Altitude–azimuth coordinates at the midpoint.
    """
    if tracking_radec is not None:
        return altaz_midpoint_from_radec(tracking_radec, datetime_begin, datetime_end)
    else:
        return altaz_midpoint_from_altaz(altaz_begin, altaz_end)


# Mapping to column name from ObservationInfo keyword
OI_MAPPING: dict[str, ColumnMapping] = {
    "exposure_name": "observation_id",
    "exposure_id": "exposure_id",
    "exp_time": "exposure_time_requested",
    "can_see_sky": "can_see_sky",
    "day_obs": "observing_day",
    "seq_num": "observation_counter",
    "physical_filter": "physical_filter",
    "s_ra": (lambda coord: coord.ra.deg, "tracking_radec"),
    "s_dec": (lambda coord: coord.dec.deg, "tracking_radec"),
    "sky_rotation": "boresight_rotation_angle",
    "azimuth_start": (lambda altaz: altaz.az.deg, "altaz_begin"),
    "azimuth_end": (lambda altaz: altaz.az.deg, "altaz_end"),
    "azimuth": (
        lambda coord, t1, t2, altaz1, altaz2: altaz_midpoint(coord, t1, t2, altaz1, altaz2).az.deg,
        "ACCEPTS_NULL",
        "tracking_radec",
        "datetime_begin",
        "datetime_end",
        "altaz_begin",
        "altaz_end",
    ),
    "altitude_start": (lambda altaz: altaz.alt.deg, "altaz_begin"),
    "altitude_end": (lambda altaz: altaz.alt.deg, "altaz_end"),
    "altitude": (
        lambda coord, t1, t2, altaz1, altaz2: altaz_midpoint(coord, t1, t2, altaz1, altaz2).alt.deg,
        "ACCEPTS_NULL",
        "tracking_radec",
        "datetime_begin",
        "datetime_end",
        "altaz_begin",
        "altaz_end",
    ),
    "zenith_distance_start": (lambda altaz: altaz.zen.deg, "altaz_begin"),
    "zenith_distance_end": (lambda altaz: altaz.zen.deg, "altaz_end"),
    "zenith_distance": (
        lambda coord, t1, t2, altaz1, altaz2: altaz_midpoint(coord, t1, t2, altaz1, altaz2).zen.deg,
        "ACCEPTS_NULL",
        "tracking_radec",
        "datetime_begin",
        "datetime_end",
        "altaz_begin",
        "altaz_end",
    ),
    "airmass": "boresight_airmass",
    "exp_midpt": (lambda t1, t2: time_midpoint(t1, t2).tai.isot, "datetime_begin", "datetime_end"),
    "exp_midpt_mjd": (lambda t1, t2: time_midpoint(t1, t2).tai.mjd, "datetime_begin", "datetime_end"),
    "obs_start": (lambda t: t.tai.isot, "datetime_begin"),
    "obs_start_mjd": (lambda t: t.tai.mjd, "datetime_begin"),
    "obs_end": (lambda t: t.tai.isot, "datetime_end"),
    "obs_end_mjd": (lambda t: t.tai.mjd, "datetime_end"),
    "shut_time": "exposure_time",
    "dark_time": "dark_time",
    "group_id": "exposure_group",
    "cur_index": (lambda seq_num, start: seq_num - start + 1, "observation_counter", "group_counter_start"),
    "max_index": (lambda end, start: end - start + 1, "group_counter_end", "group_counter_start"),
    "img_type": "observation_type",
    "emulated": "has_simulated_content",
    "science_program": "science_program",
    "observation_reason": "observation_reason",
    "target_name": "object",
    "air_temp": "temperature",
    "pressure": "pressure",
    "humidity": "relative_humidity",
    "focus_z": "focus_z",
}

# Mapping from instrument name to Header Service topic name
TOPIC_MAPPING: dict[str, ColumnMapping] = {
    "LATISS": "ATHeaderService",
    "LSSTComCam": "CCHeaderService",
    "LSSTCam": "MTHeaderService",
}


########################
# Processing Functions #
########################


def process_column(column_def: ColumnMapping, info: dict) -> Any:
    """Generate a column value from one or more keyword values in a dict.

    The dict may contain FITS headers or ObservationInfo.

    Parameters
    ----------
    column_def : `str`
        Definition of the column.  Either a string specifying the info keyword
        to use as the column value, or a tuple containing a function to apply
        to the values of one or more info keywords or function application
        tuples.
    info : `dict`
        A dictionary containing keyword/value pairs.

    Returns
    -------
    column_value : `Any`
        The value to use for the column.
        None if any input value is missing.
    """
    if isinstance(column_def, str):
        if column_def in info:
            return info[column_def]
    elif isinstance(column_def, tuple):
        fn = column_def[0]
        arg_values = [process_column(a, info) for a in column_def[1:]]
        if all(v is not None for v in arg_values):
            return fn(*arg_values)


def process_oi_column(column_def: ColumnMapping, obs_info: ObservationInfo) -> Any:
    """
    Process a column definition from OI_MAPPING and return the processed value.

    Parameters
    ----------
    column_def : str or Sequence
        Either a string key to directly access a value in `info`, or a sequence
        where the first element is a callable and the remaining elements are
        keys in `info` whose values are passed to the callable.
    obs_info : ObservationInfo
        An ObservationInfo object containing exposure metadata

    Returns
    -------
    Any
        The resulting value after processing the column definition.
    """
    if isinstance(column_def, str):
        if hasattr(obs_info, column_def):
            val = getattr(obs_info, column_def)
            if val is not None:
                return val
        logger.warning(f"Value missing in processing of OI: {column_def}")
    elif isinstance(column_def, tuple):
        fn = column_def[0]

        accepts_null = column_def[1] == "ACCEPTS_NULL"
        arg_names = column_def[2:] if accepts_null else column_def[1:]

        arg_values = [process_oi_column(a, obs_info) for a in arg_names]
        if accepts_null or all(v is not None for v in arg_values):
            return fn(*arg_values)
        logger.warning(f"Missing values in processing of OI: {fn} {arg_values=}")


def process_resource(resource: ResourcePath, instrument_dict: dict, update: bool = False) -> None:
    """Process a header resource.

    Uses configured mappings and the ObservationInfo translator to generate
    column values that are inserted into the exposure table.

    Parameters
    ----------
    resource : `ResourcePath`
        Path to the Header Service header resource.
    """
    global KW_MAPPING, OI_MAPPING, logger
    global engine

    assert engine is not None

    exposure_rec = dict()

    info = dict()
    content = yaml.safe_load(resource.read())

    for header in content["PRIMARY"]:
        info[header["keyword"]] = header["value"]

    if info["CONTRLLR"] not in instrument_dict:
        logger.warning(f"Will not process {resource}: no mapping for controller `{info['CONTRLLR']}`")
        return

    instrument_obj = instrument_dict[info["CONTRLLR"]]
    info["camera"] = instrument_obj.camera
    info["translator"] = instrument_obj.translator
    for column, column_def in KW_MAPPING.items():
        exposure_rec[column] = process_column(column_def, info)
    for column, column_def in instrument_obj.instrument_mapping.items():
        exposure_rec[column] = process_column(column_def, info)

    obs_info = ObservationInfo(info, translator_class=instrument_obj.translator)
    for column, column_def in OI_MAPPING.items():
        try:
            exposure_rec[column] = process_oi_column(column_def, obs_info)
            if isinstance(exposure_rec[column], u.Quantity):
                exposure_rec[column] = float(exposure_rec[column].value)
            elif isinstance(exposure_rec[column], np.float64):
                exposure_rec[column] = float(exposure_rec[column])
        except Exception:
            exposure_rec[column] = None
            logger.exception(f"Unable to process column: {column}")

    stmt = insert(instrument_obj.exposure_table).values(exposure_rec)
    if update:
        stmt = stmt.on_conflict_do_update(index_elements=["exposure_id"], set_=exposure_rec)
    else:
        stmt = stmt.on_conflict_do_nothing()
    logger.debug(exposure_rec)
    with engine.begin() as conn:
        conn.execute(stmt)

        detectors = [section for section in content if section.endswith("_PRIMARY")]
        for detector in detectors:
            det_exposure_rec = dict()
            det_info = info.copy()
            det_info["exposure_id"] = obs_info.exposure_id
            ccdname = f"{detector[0:3]}_{detector[3:6]}"
            if ccdname == "R00_S00" and instrument_obj.instrument_name == "latiss":
                ccdname = "RXX_S00"
            det_info["ccdname"] = ccdname
            det_info["detector"] = instrument_obj.camera[ccdname].getId()
            for header in content[detector]:
                det_info[header["keyword"]] = header["value"]
            for field, keyword in instrument_obj.det_mapping.items():
                det_exposure_rec[field] = process_column(keyword, det_info)

            if "day_obs" in instrument_obj.ccdexposure_table.columns:  # schema version >= 3.2.0
                det_exposure_rec["day_obs"] = exposure_rec["day_obs"]
                det_exposure_rec["seq_num"] = exposure_rec["seq_num"]

            det_stmt = insert(instrument_obj.ccdexposure_table).values(det_exposure_rec)
            if update:
                det_stmt = det_stmt.on_conflict_do_update(
                    index_elements=["ccdexposure_id"], set_=det_exposure_rec
                )
            else:
                det_stmt = det_stmt.on_conflict_do_nothing()
            logger.debug(det_exposure_rec)
            conn.execute(det_stmt)

        conn.commit()


def process_local_path(path: str) -> None:
    """Processes all yaml files in the specified path recursively.

    Parameters
    -----------
    path : `str`
        Path to directory that contains yaml files.
    """
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".yaml"):
                    try:
                        logger.info(f"Processing: {file}...")
                        process_resource(
                            ResourcePath(os.path.join(root, file)), get_instrument_dict(instrument)
                        )
                    except Exception:
                        logger.exception(f"Failed to process resource {file}")
    # If a yaml file is provided on the command line, process it.
    elif os.path.isfile(path) and path.endswith(".yaml"):
        process_resource(ResourcePath(path), get_instrument_dict(instrument))


def process_date(day_obs: str, instrument_dict: dict, update: bool = False) -> None:
    """Process all headers from a given observation day (as YYYY-MM-DD).

    Parameters
    ----------
    day_obs : `str`
        Observation day to process, as YYYY-MM-DD.
    """
    # global insrument
    global TOPIC_MAPPING, bucket_prefix

    date = "/".join(day_obs.split("-"))
    d = ResourcePath(f"s3://{bucket_prefix}rubinobs-lfa-cp/{TOPIC_MAPPING[instrument]}/header/{date}/")
    for dirpath, dirnames, filenames in d.walk():
        for fname in filenames:
            process_resource(d.join(fname), instrument_dict, update)


##################
# Initialization #
##################


@dataclass(frozen=True)
class KafkaConfig:
    """Class for configuring Kafka-related items."""

    bootstrap: str
    group_id: str
    username: str
    password: str
    schema_url: str


def get_kafka_config() -> KafkaConfig:
    return KafkaConfig(
        bootstrap=os.environ["KAFKA_BOOTSTRAP"],
        group_id=os.environ.get("KAFKA_GROUP_ID", "consdb-consumer"),
        username=os.environ.get("KAFKA_USERNAME", "consdb"),
        password=os.environ["KAFKA_PASSWORD"],
        schema_url=os.environ["SCHEMA_URL"],
    )


logger = setup_logging("consdb.hinfo")

instrument = os.environ.get("INSTRUMENT", "")
logger.info(f"{instrument=}")
bucket_prefix = os.environ.get("BUCKET_PREFIX", "")
if bucket_prefix:
    os.environ["LSST_DISABLE_BUCKET_VALIDATION"] = "1"


engine = None


@dataclass
class Instrument:
    instrument_name: str
    translator: lsst.obs.lsst.translators.lsst.LsstBaseTranslator
    instrument_mapping: dict
    det_mapping: dict
    camera: lsst.afw.cameraGeom.Camera
    metadata_obj: MetaData
    exposure_table: Table
    ccdexposure_table: Table

    def __init__(self, instrument_name, translator, instrument_mapping, det_mapping, camera):
        global engine
        self.instrument_name = instrument_name
        self.translator = translator
        self.instrument_mapping = instrument_mapping
        self.det_mapping = det_mapping
        self.camera = camera
        self.metadata_obj = MetaData(schema=f"cdb_{instrument_name}")
        self.exposure_table = Table("exposure", self.metadata_obj, autoload_with=engine)
        self.ccdexposure_table = Table("ccdexposure", self.metadata_obj, autoload_with=engine)


#################
# Main Function #
#################


def get_instrument_dict(instrument: str) -> dict:
    if instrument == "LATISS":
        instrument_dict = {
            "O": Instrument(
                "latiss",
                lsst.obs.lsst.translators.LatissTranslator,
                LATISS_MAPPING,
                DETECTOR_MAPPING,
                lsst.obs.lsst.Latiss.getCamera(),
            ),
        }
    elif instrument == "LSSTComCam":
        instrument_dict = {
            "O": Instrument(
                "lsstcomcam",
                lsst.obs.lsst.translators.LsstComCamTranslator,
                LSSTCOMCAM_MAPPING,
                DETECTOR_MAPPING,
                lsst.obs.lsst.LsstComCam.getCamera(),
            ),
            "S": Instrument(
                "lsstcomcamsim",
                lsst.obs.lsst.translators.LsstComCamSimTranslator,
                LSSTCOMCAMSIM_MAPPING,
                DETECTOR_MAPPING,
                lsst.obs.lsst.LsstComCamSim.getCamera(),
            ),
        }
    elif instrument == "LSSTCam":
        instrument_dict = {
            "O": Instrument(
                "lsstcam",
                lsst.obs.lsst.translators.LsstCamTranslator,
                LSSTCAM_MAPPING,
                DETECTOR_MAPPING,
                lsst.obs.lsst.LsstCam.getCamera(),
            ),
        }
    else:
        raise ValueError(f"Unrecognized instrument: {instrument}")

    return instrument_dict


async def wait_for_resource(resource):
    """Wait for a resource to become available.

    Returns if and when `resource.exists()`.

    Parameters
    ----------
    resource : Resource
        The resource to wait for.
    """
    while not resource.exists():
        await asyncio.sleep(random.uniform(0.1, 2.0))


async def handle_message(message, instrument_dict):
    """Handles the received Kafka message.

    This function processes a Kafka message by transforming
    the attached URL to a location on s3, waits for a file
    to appear at that location, and then processes the
    file so by committing it to the database.

    Parameters
    ----------
    message : dict[str, Any]
        The received Kafka message.

    instrument_dict : dict[str, Instrument]
        A dictionary mapping a controller type to its metadata.
    """
    url = message["url"]
    # Replace local HTTP access URL with generic S3 access URL.
    url = re.sub(r"https://s3\.\w+\.lsst\.org/", "s3://", url)
    if bucket_prefix:
        url = re.sub(r"s3://", "s3://" + bucket_prefix, url)
    resource = ResourcePath(url)

    try:
        await asyncio.wait_for(wait_for_resource(resource), timeout=60)
        process_resource(resource, instrument_dict)
    except asyncio.TimeoutError:
        logger.warning(f"Timeout reached while waiting for {url}. Skipping.")


async def main() -> None:
    """Handle Header Service largeFileObjectAvailable messages."""
    # global logger
    # global instrument
    global bucket_prefix, TOPIC_MAPPING

    handler_task_set = set()
    instrument_dict = get_instrument_dict(instrument)

    topic = f"lsst.sal.{TOPIC_MAPPING[instrument]}.logevent_largeFileObjectAvailable"
    kafka_config = get_kafka_config()
    async with httpx.AsyncClient() as client:
        schema_registry = kafkit.registry.httpx.RegistryApi(http_client=client, url=kafka_config.schema_url)
        deserializer = kafkit.registry.Deserializer(registry=schema_registry)

        consumer = aiokafka.AIOKafkaConsumer(
            topic,
            bootstrap_servers=kafka_config.bootstrap,
            group_id=kafka_config.group_id,
            auto_offset_reset="earliest",
            isolation_level="read_committed",
            security_protocol="SASL_PLAINTEXT",
            sasl_mechanism="SCRAM-SHA-512",
            sasl_plain_username=kafka_config.username,
            sasl_plain_password=kafka_config.password,
        )

        await consumer.start()
        logger.info("Consumer started")
        try:
            async for msg in consumer:
                message = (await deserializer.deserialize(msg.value))["message"]
                logger.debug(f"Received message {message}")
                task = asyncio.create_task(handle_message(message, instrument_dict))
                handler_task_set.add(task)
                task.add_done_callback(handler_task_set.discard)
        finally:
            await consumer.stop()

    while handler_task_set:
        logger.debug("Waiting for background tasks to finish...")
        await asyncio.sleep(5)


if __name__ == "__main__":
    import sys

    engine = setup_postgres()
    if len(sys.argv) > 1:
        process_local_path(sys.argv[1])
    else:
        asyncio.run(main())
