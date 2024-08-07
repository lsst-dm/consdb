import asyncio
import os
import random
import re
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any, Sequence

import aiokafka  # type: ignore
import astropy.time  # type: ignore
import httpx  # type: ignore
import kafkit.registry
import kafkit.registry.httpx  # type: ignore
import lsst.geom  # type: ignore
import lsst.obs.lsst  # type: ignore
import yaml
from astro_metadata_translator import ObservationInfo
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


def ninety_minus(angle: float) -> float:
    return 90.0 - angle


def tai_convert(t: str) -> datetime:
    return astropy.time.Time(t, format="isot", scale="tai").datetime


def tai_mean(start: str, end: str) -> datetime:
    s = astropy.time.Time(start, format="isot", scale="tai")
    e = astropy.time.Time(end, format="isot", scale="tai")
    return (s + (e - s) / 2).datetime


def mean(*iterable: float) -> float:
    return sum(iterable) / len(iterable)


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
    global logger
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
    global instrument
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

# Non-instrument-specific mapping to column name from Header Service keyword
KW_MAPPING: dict[str, str | Sequence] = {
    "exposure_name": "OBSID",
    "controller": "CONTRLLR",
    "seq_num": "SEQNUM",
    "band": "FILTBAND",
    "s_ra": "RA",
    "s_dec": "DEC",
    "sky_rotation": "ROTPA",
    "azimuth_start": "AZSTART",
    "azimuth_end": "AZEND",
    "azimuth": (mean, "AZSTART", "AZEND"),
    "altitude_start": (ninety_minus, "ELSTART"),
    "altitude_end": (ninety_minus, "ELEND"),
    "altitude": (mean, (ninety_minus, "ELSTART"), (ninety_minus, "ELEND")),
    "zenith_distance_start": "ELSTART",
    "zenith_distance_end": "ELEND",
    "zenith_distance": (mean, "ELSTART", "ELEND"),
    "exp_midpt": (tai_mean, "DATE-BEG", "DATE-END"),
    "exp_midpt_mjd": (mean, "MJD-BEG", "MJD-END"),
    "obs_start": (tai_convert, "DATE-BEG"),
    "obs_start_mjd": "MJD-BEG",
    "obs_end": (tai_convert, "DATE-END"),
    "obs_end_mjd": "MJD-END",
    "exp_time": "EXPTIME",
    "shut_time": "SHUTTIME",
    "dark_time": "DARKTIME",
    "group_id": "GROUPID",
    "cur_index": "CURINDEX",
    "max_index": "MAXINDEX",
    "img_type": "IMGTYPE",
    "emulated": (logical_or, "EMUIMAGE"),
    "science_program": "PROGRAM",
    "observation_reason": "REASON",
    "target_name": "OBJECT",
    "air_temp": "AIRTEMP",
    "pressure": "PRESSURE",
    "humidity": "HUMIDITY",
    "wind_speed": "WINDSPD",
    "wind_dir": "WINDDIR",
    "dimm_seeing": "SEEING",
    "focus_z": "FOCUSZ",
    "vignette": "VIGNETTE",
    "vignette_min": "VIGN_MIN",
    "s_region": (fp_region, "camera", "IMGTYPE", "RA", "DEC", "ROTPA"),
}

# Instrument-specific mapping to column name from Header Service keyword
LATISS_MAPPING: dict[str, str | Sequence] = {
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

LSSTCOMCAMSIM_MAPPING: dict[str, str | Sequence] = {
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

LSSTCOMCAM_MAPPING: dict[str, str | Sequence] = {
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

LSSTCAM_MAPPING: dict[str, str | Sequence] = {
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

DETECTOR_MAPPING = {
    "ccdexposure_id": (ccdexposure_id, "translator", "exposure_id", "detector"),
    "exposure_id": "exposure_id",
    "detector": "detector",
    "s_region": (ccd_region, "camera", "IMGTYPE", "RA", "DEC", "ROTPA", "ccdname"),
}

# Mapping to column name from ObservationInfo keyword
OI_MAPPING = {
    "exposure_id": "exposure_id",
    "physical_filter": "physical_filter",
    "airmass": "boresight_airmass",
    "day_obs": "observing_day",
}

# Mapping from instrument name to Header Service topic name
TOPIC_MAPPING = {
    "LATISS": "ATHeaderService",
    "LSSTComCam": "CCHeaderService",
    "LSSTCam": "MTHeaderService",
}


########################
# Processing Functions #
########################


def process_column(column_def: str | Sequence, info: dict) -> Any:
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

    exposure_rec = dict()

    info = dict()
    content = yaml.safe_load(resource.read())

    for header in content["PRIMARY"]:
        info[header["keyword"]] = header["value"]
    instrument_obj = instrument_dict[info["CONTRLLR"]]
    info["camera"] = instrument_obj.camera
    info["translator"] = instrument_obj.translator
    for column, column_def in KW_MAPPING.items():
        exposure_rec[column] = process_column(column_def, info)
    for column, column_def in instrument_obj.instrument_mapping.items():
        exposure_rec[column] = process_column(column_def, info)

    obs_info_obj = ObservationInfo(info, translator_class=instrument_obj.translator)
    obs_info = dict()
    for keyword in OI_MAPPING.values():
        obs_info[keyword] = getattr(obs_info_obj, keyword)
    for field, keyword in OI_MAPPING.items():
        exposure_rec[field] = process_column(keyword, obs_info)

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
            det_info["exposure_id"] = obs_info["exposure_id"]
            ccdname = f"{detector[0:3]}_{detector[3:6]}"
            if ccdname == "R00_S00" and instrument_obj.instrument_name == "latiss":
                ccdname = "RXX_S00"
            det_info["ccdname"] = ccdname
            det_info["detector"] = instrument_obj.camera[ccdname].getId()
            for header in content[detector]:
                det_info[header["keyword"]] = header["value"]
            for field, keyword in instrument_obj.det_mapping.items():
                det_exposure_rec[field] = process_column(keyword, det_info)

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


def process_date(day_obs: str, instrument_dict: dict, update: bool = False) -> None:
    """Process all headers from a given observation day (as YYYY-MM-DD).

    Parameters
    ----------
    day_obs : `str`
        Observation day to process, as YYYY-MM-DD.
    """
    global TOPIC_MAPPING, bucket_prefix, instrument

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

instrument = os.environ["INSTRUMENT"]
logger.info(f"Instrument = {instrument}")
bucket_prefix = os.environ.get("BUCKET_PREFIX", "")
if bucket_prefix:
    os.environ["LSST_DISABLE_BUCKET_VALIDATION"] = "1"


engine = setup_postgres()


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
            "S": Instrument(
                "lsstcamsim",
                lsst.obs.lsst.translators.LsstCamSimTranslator,
                LSSTCAM_MAPPING,
                DETECTOR_MAPPING,
                lsst.obs.lsst.LsstCamSim.getCamera(),
            ),
        }
    else:
        raise ValueError("Unrecognized instrument: {instrument}")

    return instrument_dict


async def main() -> None:
    """Handle Header Service largeFileObjectAvailable messages."""
    global logger, instrument, bucket_prefix, TOPIC_MAPPING

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
                url = message["url"]
                # Replace local HTTP access URL with generic S3 access URL.
                url = re.sub(r"https://s3\.\w+\.lsst\.org/", "s3://", url)
                if bucket_prefix:
                    url = re.sub(r"s3://", "s3://" + bucket_prefix, url)
                resource = ResourcePath(url)
                logger.info(f"Waiting for {url}")
                while not resource.exists():
                    await asyncio.sleep(random.uniform(0.1, 2.0))
                process_resource(resource, instrument_dict)
                logger.info(f"Processed {url}")
        finally:
            await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
