import asyncio
import logging
import os
import random
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Sequence

import aiokafka
import astropy.time
import httpx
import kafkit.registry
import kafkit.registry.httpx
import yaml
from astro_metadata_translator import ObservationInfo
from lsst.resources import ResourcePath
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from utils import setup_postgres

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


def mean(*iterable: float) -> Any:
    return sum(iterable) / len(iterable)


def logical_or(*bools: int | str | None) -> bool:
    return any([b == 1 or b == "1" for b in bools])


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
    "s_decl": "DEC",
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
    "obs_endmjd": "MJD-END",
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
}

# Instrument-specific mapping to column name from Header Service keyword
LATISS_MAPPING: dict[str, str | Sequence] = {
    "focus_z": "FOCUSZ",
    "dome_azimuth": "DOMEAZ",
    "shut_lower": "SHUTLOWR",
    "shut_upper": "SHUTUPPR",
    #     "temp_set": "TEMP_SET",
    "simulated": (
        logical_or,
        "SIMULATE ATMCS",
        "SIMULATE ATHEXAPOD",
        "SIMULAT ATPNEUMATICS",
        "SIMULATE ATDOME",
        "SIMULATE ATSPECTROGRAPH",
    ),
}

LSSTCOMCAM_MAPPING: dict[str, str | Sequence] = {}
LSSTCOMCAMSIM_MAPPING: dict[str, str | Sequence] = {}
LSSTCAM_MAPPING: dict[str, str | Sequence] = {}

# LATISS_DETECTOR_MAPPING = {
#     "ccdtemp": "CCDTEMP",
# }

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
    "LSSTComCamSim": "CCHeaderService",
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
    column_def: `str`
        Definition of the column.  Either a string specifying the info keyword
        to use as the column value, or a tuple containing a function to apply
        to the values of one or more info keywords or function application
        tuples.
    info: `dict`
        A dictionary containing keyword/value pairs.

    Returns
    -------
    column_value: `Any`
        The value to use for the column.
        None if any input value is missing.
    """
    if isinstance(column_def, str):
        if column_def in info:
            return info[column_def]
    elif isinstance(column_def, tuple):
        fn = column_def[0]
        arg_values = [process_column(a, info) for a in column_def[1:]]
        if all(arg_values):
            return fn(*arg_values)


def process_resource(resource: ResourcePath) -> None:
    """Process a header resource.

    Uses configured mappings and the ObservationInfo translator to generate
    column values that are inserted into the exposure table.

    Parameters
    ----------
    resource: `ResourcePath`
        Path to the Header Service header resource.
    """
    global KW_MAPPING, OI_MAPPING, instrument_mapping, translator
    global engine, exposure_table

    exposure_rec = dict()

    info = dict()
    content = yaml.safe_load(resource.read())
    for header in content["PRIMARY"]:
        info[header["keyword"]] = header["value"]
    for column, column_def in KW_MAPPING.items():
        exposure_rec[column] = process_column(column_def, info)
    for column, column_def in instrument_mapping.items():
        exposure_rec[column] = process_column(column_def, info)

    obs_info_obj = ObservationInfo(info, translator_class=translator)
    obs_info = dict()
    for keyword in OI_MAPPING.values():
        obs_info[keyword] = getattr(obs_info_obj, keyword)
    for field, keyword in OI_MAPPING.items():
        exposure_rec[field] = process_column(keyword, obs_info)

    logging.debug(f"Inserting {exposure_rec}")
    stmt = insert(exposure_table).values(exposure_rec).on_conflict_do_nothing()
    with engine.begin() as conn:
        conn.execute(stmt)

    # TODO: exposure_detector table processing
    #     det_info = dict()
    #     for header in content["R00S00_PRIMARY"]:
    #         det_info[header["keyword"]] = header["value"]
    #     for field, keyword in LATISS_DETECTOR_MAPPING.items():
    #         det_exposure_rec[field] = process_column(keyword, det_info)


def process_date(day_obs: str) -> None:
    """Process all headers from a given observation day (as YYYY-MM-DD).

    Parameters
    ----------
    day_obs: `str`
        Observation day to process, as YYYY-MM-DD.
    """
    global TOPIC_MAPPING, bucket_prefix, instrument

    date = "/".join(day_obs.split("-"))
    d = ResourcePath(
        f"s3://{bucket_prefix}rubinobs-lfa-cp/{TOPIC_MAPPING[instrument]}/header/{date}/"
    )
    for dirpath, dirnames, filenames in d.walk():
        for fname in filenames:
            process_resource(d.join(fname))


##################
# Initialization #
##################


@dataclass
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


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

instrument = os.environ.get("INSTRUMENT", "LATISS")
match instrument:
    case "LATISS":
        from lsst.obs.lsst.translators import LatissTranslator

        translator = LatissTranslator
        instrument_mapping = LATISS_MAPPING
    case "LSSTComCam":
        from lsst.obs.lsst.translators import LsstComCamTranslator

        translator = LsstComCamTranslator
        instrument_mapping = LSSTCOMCAM_MAPPING
    case "LSSTComCamSim":
        from lsst.obs.lsst.translators import LsstComCamSimTranslator

        translator = LsstComCamSimTranslator
        instrument_mapping = LSSTCOMCAMSIM_MAPPING
    case "LSSTCam":
        from lsst.obs.lsst.translators import LsstCamTranslator

        translator = LsstCamTranslator
        instrument_mapping = LSSTCAM_MAPPING
logging.info(f"Instrument = {instrument}")

engine = setup_postgres()
metadata_obj = MetaData(schema=f"cdb_{instrument.lower()}")
exposure_table = Table("exposure", metadata_obj, autoload_with=engine)


bucket_prefix = os.environ.get("BUCKET_PREFIX", "")
if bucket_prefix:
    os.environ["LSST_DISABLE_BUCKET_VALIDATION"] = "1"


topic = f"lsst.sal.{TOPIC_MAPPING[instrument]}.logevent_largeFileObjectAvailable"


#################
# Main Function #
#################


async def main() -> None:
    """Handle Header Service largeFileObjectAvailable messages."""
    global bucket_prefix

    kafka_config = get_kafka_config()
    async with httpx.AsyncClient() as client:
        schema_registry = kafkit.registry.httpx.RegistryApi(
            http_client=client, url=kafka_config.schema_url
        )
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
        logging.info("Consumer started")
        try:
            async for msg in consumer:
                message = (await deserializer.deserialize(msg.value))["message"]
                logging.debug(f"Received message {message}")
                url = message["url"]
                # Replace local HTTP access URL with generic S3 access URL.
                url = re.sub(r"https://s3\.\w+\.lsst\.org/", "s3://", url)
                if bucket_prefix:
                    url = re.sub(r"s3://", "s3://" + bucket_prefix, url)
                resource = ResourcePath(url)
                logging.info(f"Waiting for {url}")
                while not resource.exists():
                    await asyncio.sleep(random.uniform(0.1, 2.0))
                process_resource(resource)
                logging.info(f"Processed {url}")
        finally:
            await consumer.stop()


asyncio.run(main())
