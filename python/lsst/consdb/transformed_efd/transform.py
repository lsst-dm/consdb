# This file is part of consdb.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Provides functions and utilities for transformed EFD."""

import logging
from typing import Any, Dict, List, Tuple

import astropy.time
import pandas
from lsst.consdb.transformed_efd.dao.butler import ButlerDao
from lsst.consdb.transformed_efd.dao.exposure_efd import ExposureEfdDao, ExposureEfdUnpivotedDao
from lsst.consdb.transformed_efd.dao.influxdb import InfluxDbDao
from lsst.consdb.transformed_efd.dao.visit_efd import VisitEfdDao, VisitEfdUnpivotedDao
from lsst.consdb.transformed_efd.summary import Summary
from lsst.daf.butler import Butler


class Transform:
    """A class that represents a data transformation process."""

    # ====================
    # Public API Methods
    # ====================
    def __init__(
        self,
        butler: Butler,
        db_uri: str,
        efd: InfluxDbDao,
        config: Dict[str, Any],
        logger: logging.Logger,
        commit_every: int = 100,
    ):
        """Initialize new instance of the Transform class."""
        self.log = logger
        self.butler_dao = ButlerDao(butler)
        self.db_uri = db_uri
        self.efd = efd
        self.config = config
        self.commit_every = commit_every
        self.log.info("----------- Transform -----------")

    def get_schema_by_instrument(self, instrument: str) -> str:
        """Get the schema name for the given instrument."""
        schemas = {
            "latiss": "efd_latiss",
            "lsstcomcam": "efd_lsstcomcam",
            "lsstcomcamsim": "efd_lsstcomcamsim",
        }
        return schemas[instrument.lower()]

    def get_instrument(self, instrument: str) -> str:
        """Get the instrument name."""
        instruments = {
            "latiss": "LATISS",
            "lsstcomcam": "LSSTComCam",
            "lsstcomcamsim": "LSSTComCamSim",
        }
        return instruments[instrument.lower()]

    def process_interval(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> Dict[str, int]:
        """Process the given time interval for a specific instrument."""
        count = self._initialize_counts()
        self.log.info(f"Processing interval {start_time} - {end_time}")

        exposures, visits = self._retrieve_exposures_and_visits(instrument, start_time, end_time)

        if not exposures and not visits:
            self.log.info("No exposures or visits found for the period.")
            return count

        results = self._process_interval(exposures, visits, start_time, end_time)
        count = self._store_results(instrument, results)
        return count

    # ====================
    # Private Helper Methods
    # ====================
    def _compute_column_value(
        self,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
        topics: List[Dict[str, pandas.DataFrame]],
        transform_function: str,
        **function_kwargs: Any,
    ) -> Any:
        """Compute column value using named transformation."""
        ts_start = pandas.to_datetime(start_time.utc.datetime, utc=True)
        ts_end = pandas.to_datetime(end_time.utc.datetime, utc=True)
        valid_series = [
            topic["series"].sort_index().loc[ts_start:ts_end] for topic in topics if not topic["series"].empty
        ]
        values = pandas.concat(valid_series, copy=False) if valid_series else pandas.DataFrame()

        if values.empty:
            return None

        return Summary(dataframe=values, exposure_start=start_time, exposure_end=end_time).apply(
            transform_function, **function_kwargs
        )

    def _map_topics(self) -> Dict[str, Any]:
        """Map topics and fields to perform a single query per topic."""
        topics_map = {}
        for column in self.config["columns"]:
            for values in column["topics"]:
                topic = values["name"]
                if topic not in topics_map.keys():
                    topics_map[topic] = {
                        "name": topic,
                        "fields": [],
                        "packed_series": [],
                        "columns": [],
                    }
                for field in values["fields"]:
                    topics_map[topic]["fields"].append(field["name"])
                topics_map[topic]["fields"] = list(set(topics_map[topic]["fields"]))
                topics_map[topic]["packed_series"].append(column["packed_series"])
                topics_map[topic]["columns"].append(column)
            topics_map[topic]["is_packed"] = any(topics_map[topic]["packed_series"])
        return topics_map

    def _process_interval(
        self,
        exposures: List[Dict[str, Any]],
        visits: List[Dict[str, Any]],
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> Dict[str, Any]:
        """Process the given time interval for a specific instrument."""
        results = {
            "exposures": {exp["id"]: {"exposure_id": exp["id"]} for exp in exposures},
            "visits": {vis["id"]: {"visit_id": vis["id"]} for vis in visits},
            "exposures_unpivoted": [],
            "visits_unpivoted": [],
        }

        topic_interval = self._get_topic_interval(start_time, end_time, exposures, visits)
        self.log.info(f"Topic interval: {topic_interval[0]} - {topic_interval[1]}")
        topics_map = self._map_topics()

        for topic_name, topic in topics_map.items():
            self._process_topic(topic, topic_interval, exposures, visits, results)

        return results

    def _process_topic(
        self,
        topic: Dict[str, Any],
        topic_interval: List[astropy.time.Time],
        exposures: List[Dict[str, Any]],
        visits: List[Dict[str, Any]],
        results: Dict[str, Any],
    ) -> None:
        """Process a single topic and update results."""
        self.log.info(f"Querying Topic {topic['name']}")
        topic_series = self._query_efd_values(topic, topic_interval, topic["is_packed"])

        if topic_series.empty:
            self.log.warning(f"No data in topic {topic['name']}")
            return

        for column in topic["columns"]:
            self._process_column(column, topic, topic_series, exposures, visits, results)

    def _process_column(
        self,
        column: Dict[str, Any],
        topic: Dict[str, Any],
        topic_series: pandas.DataFrame,
        exposures: List[Dict[str, Any]],
        visits: List[Dict[str, Any]],
        results: Dict[str, Any],
    ) -> None:
        """Process a single column and update results."""
        self.log.info(f"Processing Column {column['name']}")
        data = self._prepare_column_data(column, topic, topic_series)

        if "exposure_efd" in column["tables"]:
            self._process_exposures(column, data, exposures, results["exposures"])

        if "exposure_efd_unpivoted" in column["tables"]:
            self._process_exposures_unpivoted(topic, column, data, exposures, results["exposures_unpivoted"])

        if "visit1_efd" in column["tables"]:
            self._process_visits(column, data, visits, results["visits"])

        if "visit1_efd_unpivoted" in column["tables"]:
            self._process_visits_unpivoted(topic, column, data, visits, results["visits_unpivoted"])

    def _process_exposures(
        self,
        column: Dict[str, Any],
        data: List[Dict[str, pandas.DataFrame]],
        exposures: List[Dict[str, Any]],
        results: Dict[str, Any],
    ) -> None:
        """Process exposure data and update results."""
        for exposure in exposures:
            function_kwargs = column["function_args"] or {}
            column_value = self._compute_column_value(
                start_time=exposure["timespan"].begin.utc,
                end_time=exposure["timespan"].end.utc,
                topics=data,
                transform_function=column["function"],
                **function_kwargs,
            )
            results[exposure["id"]][column["name"]] = column_value

    def _process_exposures_unpivoted(
        self,
        topic: Dict[str, Any],
        column: Dict[str, Any],
        data: List[Dict[str, pandas.DataFrame]],
        exposures: List[Dict[str, Any]],
        results: List[Dict[str, Any]],
    ) -> None:
        """Process exposure unpivoted data and update results."""
        for exposure in exposures:
            function_kwargs = column["function_args"] or {}
            series_df = data[0]["series"]
            for col in series_df.columns:
                new_topic = topic.copy()
                new_topic["fields"] = [col]
                new_topic["columns"][0]["topics"][0]["fields"] = [{"name": col}]
                new_data = [{"topic": new_topic, "series": series_df[[col]]}]
                column_value = self._compute_column_value(
                    start_time=exposure["timespan"].begin.utc,
                    end_time=exposure["timespan"].end.utc,
                    topics=new_data,
                    transform_function=column.get("function"),
                    **function_kwargs,
                )
                if column_value:
                    results.append(
                        {
                            "exposure_id": exposure["id"],
                            "property": column["name"],
                            "field": col,
                            "value": column_value,
                        }
                    )

    def _process_visits(
        self,
        column: Dict[str, Any],
        data: List[Dict[str, pandas.DataFrame]],
        visits: List[Dict[str, Any]],
        results: Dict[str, Any],
    ) -> None:
        """Process visit data and update results."""
        for visit in visits:
            function_kwargs = column["function_args"] or {}
            column_value = self._compute_column_value(
                start_time=visit["timespan"].begin.utc,
                end_time=visit["timespan"].end.utc,
                topics=data,
                transform_function=column["function"],
                **function_kwargs,
            )
            results[visit["id"]][column["name"]] = column_value

    def _process_visits_unpivoted(
        self,
        topic: Dict[str, Any],
        column: Dict[str, Any],
        data: List[Dict[str, pandas.DataFrame]],
        visits: List[Dict[str, Any]],
        results: List[Dict[str, Any]],
    ) -> None:
        """Process visit unpivoted data and update results."""
        for visit in visits:
            function_kwargs = column["function_args"] or {}
            series_df = data[0]["series"]
            for col in series_df.columns:
                new_topic = topic.copy()
                new_topic["fields"] = [col]
                new_topic["columns"][0]["topics"][0]["fields"] = [{"name": col}]
                new_data = [{"topic": new_topic, "series": series_df[[col]]}]
                column_value = self._compute_column_value(
                    start_time=visit["timespan"].begin.utc,
                    end_time=visit["timespan"].end.utc,
                    topics=new_data,
                    transform_function=column.get("function"),
                    **function_kwargs,
                )
                if column_value:
                    results.append(
                        {
                            "visit_id": visit["id"],
                            "property": column["name"],
                            "field": col,
                            "value": column_value,
                        }
                    )

    def _prepare_column_data(
        self,
        column: Dict[str, Any],
        topic: Dict[str, Any],
        topic_series: pandas.DataFrame,
    ) -> List[Dict[str, pandas.DataFrame]]:
        """Prepare data for a single column."""
        if not topic_series.empty:
            fields = [f["name"] for f in column["topics"][0]["fields"]]
            if column["subset_field"]:
                subset_field = str(column["subset_field"])
                subset_value = str(column["subset_value"])
                if subset_field in topic_series and not topic_series[subset_field].empty:
                    topic_series[subset_field] = topic_series[subset_field].fillna("").astype(str)
                    subset_value = str(subset_value)
                    filtered_df = topic_series.loc[topic_series[subset_field] == subset_value]
                    fields.remove(subset_field)
                    valid_fields = [field for field in fields if field in filtered_df.columns]
                    if valid_fields:
                        data = [
                            {
                                "topic": topic["name"],
                                "series": filtered_df[valid_fields].dropna(),
                            }
                        ]
                    else:
                        self.log.warning(
                            f"No valid fields found in filtered DataFrame " f"in Topic {topic['name']}"
                        )
                        data = [
                            {
                                "topic": topic["name"],
                                "series": pandas.DataFrame(),
                            }
                        ]
                else:
                    data = [{"topic": topic["name"], "series": pandas.DataFrame()}]
            else:
                data = [
                    {
                        "topic": topic["name"],
                        "series": topic_series[fields].dropna(),
                    }
                ]
        else:
            data = [{"topic": topic["name"], "series": pandas.DataFrame()}]

        return data

    def _initialize_counts(self) -> Dict[str, int]:
        """Initialize counts for exposures and visits."""
        return {
            "exposures": 0,
            "visits1": 0,
            "exposures_unpivoted": 0,
            "visits1_unpivoted": 0,
        }

    def _retrieve_exposures_and_visits(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Retrieve exposures and visits from Butler"""
        instrument_name = self.get_instrument(instrument)
        exposures = self.butler_dao.exposures_by_period(instrument_name, start_time, end_time)
        self.log.info(f"Exposures: {len(exposures)}")
        visits = self.butler_dao.visits_by_period(instrument_name, start_time, end_time)
        self.log.info(f"Visits: {len(visits)}")
        return exposures, visits

    def _store_results(
        self,
        instrument: str,
        results: Dict[str, Any],
    ) -> Dict[str, int]:
        """Store the processed results into the database."""
        count = {
            "exposures": 0,
            "visits1": 0,
            "exposures_unpivoted": 0,
            "visits1_unpivoted": 0,
        }

        schema = self.get_schema_by_instrument(instrument)

        # Store exposures
        if results["exposures"]:
            exposures_list = list(results["exposures"].values())
            df_exposures = pandas.DataFrame(exposures_list)
            if not df_exposures.empty:
                exp_dao = ExposureEfdDao(db_uri=self.db_uri, schema=schema)
                affected_rows = exp_dao.upsert(df=df_exposures, commit_every=self.commit_every)
                count["exposures"] = affected_rows
                self.log.info(f"Stored {affected_rows} exposure records")

        # Store visits
        if results["visits"]:
            visits_list = list(results["visits"].values())
            df_visits = pandas.DataFrame(visits_list)
            if not df_visits.empty:
                vis_dao = VisitEfdDao(db_uri=self.db_uri, schema=schema)
                affected_rows = vis_dao.upsert(df=df_visits, commit_every=self.commit_every)
                count["visits1"] = affected_rows
                self.log.info(f"Stored {affected_rows} visit records")

        # Store unpivoted exposures
        if results["exposures_unpivoted"]:
            df_exposures_unpivoted = pandas.DataFrame(results["exposures_unpivoted"])
            if not df_exposures_unpivoted.empty:
                exp_unpivoted_dao = ExposureEfdUnpivotedDao(db_uri=self.db_uri, schema=schema)
                affected_rows = exp_unpivoted_dao.upsert(
                    df=df_exposures_unpivoted, commit_every=self.commit_every
                )
                count["exposures_unpivoted"] = affected_rows
                self.log.info(f"Stored {affected_rows} unpivoted exposure records")

        # Store unpivoted visits
        if results["visits_unpivoted"]:
            df_visits_unpivoted = pandas.DataFrame(results["visits_unpivoted"])
            if not df_visits_unpivoted.empty:
                vis_unpivoted_dao = VisitEfdUnpivotedDao(db_uri=self.db_uri, schema=schema)
                affected_rows = vis_unpivoted_dao.upsert(
                    df=df_visits_unpivoted, commit_every=self.commit_every
                )
                count["visits1_unpivoted"] = affected_rows
                self.log.info(f"Stored {affected_rows} unpivoted visit records")

        return count

    def _query_efd_values(
        self,
        topic: Dict[str, Any],
        topic_interval: List[astropy.time.Time],
        packed_series: bool = False,
    ) -> pandas.DataFrame:
        """Query EFD values for a topic within a specified time interval."""
        start = topic_interval[0].utc
        end = topic_interval[1].utc
        window = astropy.time.TimeDelta(topic.get("window", 0.0), format="sec")
        fields = [f for f in topic["fields"]]
        chunk_size = 100
        chunks = [fields[i : i + chunk_size] for i in range(0, len(fields), chunk_size)]

        all_series = []
        for chunk in chunks:
            try:
                if packed_series:
                    series = self.efd.select_packed_time_series(
                        topic["name"],
                        chunk,
                        start - window,
                        end + window,
                        ref_timestamp_scale="utc",
                    )
                else:
                    series = self.efd.select_time_series(
                        topic["name"],
                        chunk,
                        start - window,
                        end + window,
                    )
                if not series.empty:
                    all_series.append(series)
            except Exception as e:
                self.log.warning(f"An unexpected error occurred: {e}")

        return pandas.concat(all_series, axis=1) if all_series else pandas.DataFrame()

    def _get_topic_interval(
        self,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
        exposures: List[dict],
        visits: List[dict],
    ) -> List[astropy.time.Time]:
        """Get the topic interval based on the given start and end times."""
        min_topic_time = start_time
        max_topic_time = end_time
        for exposure in exposures:
            if exposure["timespan"].end < end_time:
                min_topic_time = min(exposure["timespan"].begin, min_topic_time)
                max_topic_time = max(exposure["timespan"].begin, max_topic_time)
        for visit in visits:
            if visit["timespan"].end < end_time:
                min_topic_time = min(visit["timespan"].begin, min_topic_time)
                max_topic_time = max(visit["timespan"].begin, max_topic_time)
        return [min_topic_time, max_topic_time]
