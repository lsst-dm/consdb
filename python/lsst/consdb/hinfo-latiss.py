from datetime import datetime
import os
import sys
from typing import Any, Iterable

import yaml
from astropy.time import Time
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert

from astro_metadata_translator import ObservationInfo
from lsst.resources import ResourcePath
from lsst.obs.lsst.translators import LatissTranslator

# import Kafka interface



def ninety_minus(angle: float) -> float:
    return 90.0 - angle

def tai_convert(t: str) -> datetime:
    return Time(t, format="isot", scale="tai").datetime

def tai_mean(start: str, end: str) -> datetime:
    s = Time(start, format="isot", scale="tai")
    e = Time(end, format="isot", scale="tai")
    return (s + (e - s) / 2).datetime

def mean(*iterable: Iterable[Any]) -> Any:
    return sum(iterable) / len(iterable)

def logical_or(*bools: Iterable[int | str | None]) -> bool:
    return any([b == 1 or b == "1" for b in bools])


KW_MAPPING = {
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

LATISS_MAPPING = {
    "focus_z": "FOCUSZ",
    "dome_azimuth": "DOMEAZ",
    "shut_lower": "SHUTLOWR",
    "shut_upper": "SHUTUPPR",
#     "temp_set": "TEMP_SET",
    "simulated": (logical_or, "SIMULATE ATMCS", "SIMULATE ATHEXAPOD", "SIMULAT ATPNEUMATICS", "SIMULATE ATDOME", "SIMULATE ATSPECTROGRAPH"),
}

# LATISS_DETECTOR_MAPPING = {
#     "ccdtemp": "CCDTEMP",
# }

OI_MAPPING = {
    "exposure_id": "exposure_id",
    "physical_filter": "physical_filter",
    "airmass": "boresight_airmass",
    "day_obs": "observing_day",
}

TOPIC_MAPPING = {
     "LATISS": "ATHeaderService",
     "LSSTComCam": "CCHeaderService",
     "LSSTCam": "MTHeaderService",
}


url = os.environ.get("POSTGRES_URL", "postgresql://usdf-butler.slac.stanford.edu:5432/lsstdb1")
engine = create_engine(url)
instrument = os.environ.get("INSTRUMENT", "LATISS")
metadata_obj = MetaData(schema=f"cdb_{instrument.lower()}")
exposure_table = Table("exposure", metadata_obj, autoload_with=engine)


def process_keyword(keyword: str | tuple, info: dict) -> Any:
    if type(keyword) == str:
        if keyword in info:
            return info[keyword]
    elif type(keyword) == tuple:
        fn = keyword[0]
        args = keyword[1:]
        if all([a in info for a in args]):
            return fn(*[info[a] for a in args])

def process_resource(resource: ResourcePath) -> None:
    global engine, exposure_table

    content = yaml.safe_load(resource.read())
    exposure_rec = dict()

    info = dict()
    for header in content["PRIMARY"]:
        info[header["keyword"]] = header["value"]
    for field, keyword in KW_MAPPING.items():
        exposure_rec[field] = process_keyword(keyword, info)
    for field, keyword in LATISS_MAPPING.items():
        exposure_rec[field] = process_keyword(keyword, info)

#     det_info = dict()
#     for header in content["R00S00_PRIMARY"]:
#         det_info[header["keyword"]] = header["value"]
#     for field, keyword in LATISS_DETECTOR_MAPPING.items():
#         det_exposure_rec[field] = process_keyword(keyword, det_info)

    obs_info_obj = ObservationInfo(info, translator_class=LatissTranslator)
    obs_info = dict()
    for keyword in OI_MAPPING.values():
        obs_info[keyword] = getattr(obs_info_obj, keyword)
    for field, keyword in OI_MAPPING.items():
        exposure_rec[field] = process_keyword(keyword, obs_info)

    stmt = insert(exposure_table).values(exposure_rec).on_conflict_do_nothing()
    with engine.begin() as conn:
        result = conn.execute(stmt)

    # print(exposure_rec)


site = os.environ.get("SITE", "USDF")
if site == "USDF":
    os.environ["LSST_DISABLE_BUCKET_VALIDATION"] = "1"
    bucket_prefix = "rubin:"
else:
    bucket_prefix = ""

# For Kafka:
# consumer = configure_kafka()
# while True:
#     msgs = consumer.consume()
#     for msg in msgs:
#         re.sub(r"s3://", "s3://" + bucket_prefix, msg.data)
#         process_resource(msg.data)

# To process all of a given date:
date = "/".join(sys.argv[1].split("-"))
d = ResourcePath(f"s3://{bucket_prefix}rubinobs-lfa-cp/{TOPIC_MAPPING[instrument]}/header/{date}/")
for dirpath, dirnames, filenames in d.walk():
    for fname in filenames:
        process_resource(d.join(fname))
