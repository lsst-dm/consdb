import asyncio
import os
import random
import re
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
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import insert

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
    "controller": "CONTRLLR",
    "seq_num": "SEQNUM",
    "band": "FILTBAND",
    "ra": "RA",
    "decl": "DEC",
    "skyrotation": "ROTPA",
    "azimuth_start": "AZSTART",
    "azimuth_end": "AZEND",
    "altitude_start": (ninety_minus, "ELSTART"),
    "altitude_end": (ninety_minus, "ELEND"),
    "zenithdistance_start": "ELSTART",
    "zenithdistance_end": "ELEND",
    "expmidpt": (tai_mean, "DATE-BEG", "DATE-END"),
    "expmidptmjd": (mean, "MJD-BEG", "MJD-END"),
    "obsstart": (tai_convert, "DATE-BEG"),
    "obsstartmjd": "MJD-BEG",
    "obsend": (tai_convert, "DATE-END"),
    "obsendmjd": "MJD-END",
    "exptime": "EXPTIME",
    "shuttime": "SHUTTIME",
    "darktime": "DARKTIME",
    "group_id": "GROUPID",
    "curindex": "CURINDEX",
    "maxindex": "MAXINDEX",
    "imgtype": "IMGTYPE",
    "emulated": (logical_or, "EMUIMAGE"),
    "science_program": "PROGRAM",
    "observation_reason": "REASON",
    "target_name": "OBJECT",
    "airtemp": "AIRTEMP",
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
        to the values of one or more info keywords.
    info: `dict`
        A dictionary containing keyword/value pairs.

    Returns
    -------
    column_value: `Any`
        The value to use for the column.
    """
    if type(column_def) is str:
        if column_def in info:
            return info[column_def]
    elif type(column_def) is tuple:
        fn = column_def[0]
        args = column_def[1:]
        if all([a in info for a in args]):
            return fn(*[info[a] for a in args])


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

host = os.environ.get("DB_HOST")
passwd = os.environ.get("DB_PASS")
user = os.environ.get("DB_USER")
dbname = os.environ.get("DB_NAME")
url = ""
if host and passwd and user and dbname:
    print(f"Connecting to {host} as {user} to {dbname}")
    url = f"postgresql://{user}:{passwd}@{host}/{dbname}"
else:
    url = os.environ.get(
        "POSTGRES_URL", "postgresql://usdf-butler.slac.stanford.edu:5432/lsstdb1"
    )
    print("Using POSTGRES_URL {user} {host} {dbname}")
engine = create_engine(url)
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
        try:
            async for msg in consumer:
                message = (await deserializer.deserialize(msg.value))["message"]
                url = message["url"]
                if bucket_prefix:
                    url = re.sub(r"s3://", "s3://" + bucket_prefix, url)
                resource = ResourcePath(url)
                while not resource.exists():
                    await asyncio.sleep(random.uniform(0.1, 2.0))
                process_resource(resource)
        finally:
            await consumer.stop()


asyncio.run(main())
