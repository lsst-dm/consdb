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

import copy
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


def handle_processing_errors(func):
    """Log error and re-raise to interrupt processing."""

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.log.error(f"Error in {func.__name__}: {e}")
            raise

    return wrapper


class Transform:
    """A class that represents a data transformation process."""

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

    def get_schema_by_instrument(self, instrument: str) -> str:
        """Get the schema name for the given instrument."""
        schemas = {
            "latiss": "efd_latiss",
            "lsstcomcam": "efd_lsstcomcam",
            "lsstcomcamsim": "efd_lsstcomcamsim",
            "lsstcam": "efd_lsstcam",
        }
        return schemas[instrument.lower()]

    def get_instrument(self, instrument: str) -> str:
        """Get the instrument name."""
        instruments = {
            "latiss": "LATISS",
            "lsstcomcam": "LSSTComCam",
            "lsstcomcamsim": "LSSTComCamSim",
            "lsstcam": "LSSTCam",
        }
        return instruments[instrument.lower()]

    @handle_processing_errors
    def process_interval(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> Dict[str, int]:
        """Process the given time interval for a specific instrument."""
        count = self._initialize_counts()
        self.log.debug(f"Interval + Time Window: start_time={start_time} end_time={end_time}")

        exposures, visits = self._retrieve_exposures_and_visits(instrument, start_time, end_time)

        if not exposures and not visits:
            self.log.debug("No exposures or visits found for the period.")
            return count

        # Recalculate start and end times based on exposures and visits
        # self.log.debug(f"Original Interval: start_time={start_time.iso} end_time={end_time.iso} delta=~{int((end_time - start_time).sec)} seconds")
        # all_items = exposures + visits
        # start_time = min(item['timespan'].begin for item in all_items).utc
        # end_time = max(item['timespan'].end for item in all_items).utc

        # self.log.debug(f"Adjusted Interval: start_time={start_time.iso} end_time={end_time.iso} delta=~{int((end_time - start_time).sec)} seconds")

        results = self._process_interval(exposures, visits, start_time, end_time)

        count = self._store_results(instrument, results)
        return count

    # ====================
    # Private Helper Methods
    # ====================
    @handle_processing_errors
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
        if "start_offset" in function_kwargs:
            ts_start += pandas.Timedelta(function_kwargs["start_offset"], unit="h")

        ts_end = pandas.to_datetime(end_time.utc.datetime, utc=True)

        # valid_series = [
        #     topic["series"].sort_index().loc[(topic["series"].index > ts_start) & (topic["series"].index < ts_end)] for topic in topics if not topic["series"].empty
        # ]
        valid_series = []

        for topic in topics:
            if not topic["series"].empty:
                series = topic["series"].loc[
                    (topic["series"].index >= ts_start) & (topic["series"].index <= ts_end)
                ]
                if not series.empty:
                    valid_series.append(series)

        values = pandas.concat(valid_series, copy=False) if valid_series else pandas.DataFrame()

        if values.empty:
            return None

        return Summary(dataframe=values, exposure_start=start_time, exposure_end=end_time).apply(
            transform_function, **function_kwargs
        )

    @handle_processing_errors
    def _map_topics(self) -> Dict[str, Any]:
        """Map topics and fields to perform a single query per topic."""
        groups_map = {}

        # 1. Itera e agrupa as informações
        for column in self.config["columns"]:
            start_offset = column.get("start_offset")
            packed_series = column.get("packed_series")
            pre_aggregate_interval = column.get("pre_aggregate_interval")
            function = column.get("function")

            for topic_info in column["topics"]:
                topic_name = topic_info["name"]

                # Cria a chave composta
                group_key = (
                    topic_name,
                    packed_series,
                    start_offset,
                    pre_aggregate_interval,
                    function if pre_aggregate_interval is not None else None,
                )

                # Inicializa o grupo se for a primeira vez que o vemos
                if group_key not in groups_map:
                    groups_map[group_key] = {
                        "name": topic_name,
                        "start_offset": start_offset,
                        "pre_aggregate_interval": pre_aggregate_interval,
                        "function": function,
                        "fields": set(),
                        "columns": [],
                    }

                # Agrega os campos necessários para a consulta
                for field in topic_info["fields"]:
                    groups_map[group_key]["fields"].add(field["name"])

                # Agrupa a configuração completa da coluna
                groups_map[group_key]["columns"].append(column)

        # 2. Finaliza a estrutura de dados para cada grupo
        for group_key, group_data in groups_map.items():
            # Converte o set de campos para uma lista
            group_data["fields"] = list(group_data["fields"])

        return groups_map

    @handle_processing_errors
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
        self.log.debug(f"Topic Interval: start={topic_interval[0]} end={topic_interval[1]}")
        topics_map = self._map_topics()
        for key, topic in topics_map.items():
            processing_topic = copy.deepcopy(topic)
            _, packed_series, start_offset, pre_aggregate_interval, function = key
            processing_topic["is_packed"] = packed_series
            processing_topic["pre_aggregate_interval"] = None

            if pre_aggregate_interval is not None and function in ["mean", "max", "min"]:
                processing_topic["pre_aggregate_interval"] = pre_aggregate_interval

            # apply offset to the topic interval if specified
            if start_offset is not None:
                processing_topic["function_args"]["start_offset"] = start_offset
                offset_topic_interval = topic_interval.copy()
                offset_topic_interval[0] += astropy.time.TimeDelta(float(start_offset) * 3600, format="sec")
                self._process_topic(processing_topic, offset_topic_interval, exposures, visits, results)
            else:
                self._process_topic(processing_topic, topic_interval, exposures, visits, results)

        return results

    @handle_processing_errors
    def _process_topic(
        self,
        topic: Dict[str, Any],
        topic_interval: List[astropy.time.Time],
        exposures: List[Dict[str, Any]],
        visits: List[Dict[str, Any]],
        results: Dict[str, Any],
    ) -> None:
        """Process a single topic and update results."""
        self.log.debug(f"Querying Topic: name={topic['name']}")
        topic_series = self._query_efd_values(topic, topic_interval, topic["is_packed"])

        if topic_series.empty:
            if self.log.isEnabledFor(logging.DEBUG):
                self.log.warning(f"No data in topic: name={topic['name']}")
            return

        for column in topic["columns"]:
            self._process_column(column, topic, topic_series, exposures, visits, results)

    @handle_processing_errors
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
        self.log.debug(f"Processing Column: name={column['name']}")
        data = self._prepare_column_data(column, topic, topic_series)

        if "exposure_efd" in column["tables"]:
            self._process_exposures(column, data, exposures, results["exposures"])

        if "exposure_efd_unpivoted" in column["tables"]:
            self._process_exposures_unpivoted(topic, column, data, exposures, results["exposures_unpivoted"])

        if "visit1_efd" in column["tables"]:
            self._process_visits(column, data, visits, results["visits"])

        if "visit1_efd_unpivoted" in column["tables"]:
            self._process_visits_unpivoted(topic, column, data, visits, results["visits_unpivoted"])

    @handle_processing_errors
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

    @handle_processing_errors
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
            series_df = data[0]["series"].copy()
            for col in series_df.columns:
                col_series = series_df[[col]].copy()
                new_topic = topic.copy()
                new_topic["fields"] = [col]
                new_topic["columns"][0]["topics"][0]["fields"] = [{"name": col}]

                new_data = [{"topic": new_topic, "series": col_series}]
                column_value = self._compute_column_value(
                    start_time=exposure["timespan"].begin.utc,
                    end_time=exposure["timespan"].end.utc,
                    topics=new_data,
                    transform_function=column.get("function"),
                    **function_kwargs,
                )
                if column_value is not None:
                    results.append(
                        {
                            "exposure_id": exposure["id"],
                            "property": column["name"],
                            "field": col,
                            "value": column_value,
                        }
                    )

    @handle_processing_errors
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

    @handle_processing_errors
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

    @handle_processing_errors
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
                raw_subset_value = column["subset_value"]

                if subset_field in topic_series and not topic_series[subset_field].empty:
                    topic_series[subset_field] = topic_series[subset_field].fillna("").astype(str)

                    # Handle single value or list of values for filtering
                    if isinstance(raw_subset_value, list):
                        subset_values_str = [str(val) for val in raw_subset_value]
                        filtered_df = topic_series.loc[topic_series[subset_field].isin(subset_values_str)]
                    else:
                        subset_value_str = str(raw_subset_value)
                        filtered_df = topic_series.loc[topic_series[subset_field] == subset_value_str]

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
                        self.log.debug(
                            f"No valid fields found in filtered DataFrame in Topic: " f"name={topic['name']}"
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

    @handle_processing_errors
    def _retrieve_exposures_and_visits(
        self,
        instrument: str,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Retrieve exposures and visits from Butler"""
        instrument_name = self.get_instrument(instrument)
        exposures = self.butler_dao.exposures_by_period(instrument_name, start_time, end_time)
        self.log.debug(f"Exposures fetched from Butler: count={len(exposures)}")
        visits = self.butler_dao.visits_by_period(instrument_name, start_time, end_time)
        self.log.debug(f"Visits fetched from Butler: count={len(visits)}")

        return exposures, visits

    @handle_processing_errors
    def _store_results(
        self,
        instrument: str,
        results: Dict[str, Any],
    ) -> Dict[str, int]:
        """Store the processed results into the database."""
        count = {"exposures": 0, "visits1": 0}

        schema = self.get_schema_by_instrument(instrument)

        # Store exposures
        if results["exposures"]:
            exposures_list = list(results["exposures"].values())
            df_exposures = pandas.DataFrame(exposures_list)
            if not df_exposures.empty:
                exp_dao = ExposureEfdDao(db_uri=self.db_uri, schema=schema, logger=self.log)
                affected_rows = exp_dao.upsert(df=df_exposures, commit_every=self.commit_every)
                count["exposures"] = affected_rows
                self.log.debug(f"Stored exposure records: affected_rows={affected_rows}")

        # Store visits
        if results["visits"]:
            visits_list = list(results["visits"].values())
            df_visits = pandas.DataFrame(visits_list)
            if not df_visits.empty:
                vis_dao = VisitEfdDao(db_uri=self.db_uri, schema=schema, logger=self.log)
                affected_rows = vis_dao.upsert(df=df_visits, commit_every=self.commit_every)
                count["visits1"] = affected_rows
                self.log.debug(f"Stored visit records: affected_rows={affected_rows}")

        # Store unpivoted exposures
        if results["exposures_unpivoted"]:
            df_exposures_unpivoted = pandas.DataFrame(results["exposures_unpivoted"])
            if not df_exposures_unpivoted.empty:
                exp_unpivoted_dao = ExposureEfdUnpivotedDao(
                    db_uri=self.db_uri, schema=schema, logger=self.log
                )
                affected_rows = exp_unpivoted_dao.upsert(
                    df=df_exposures_unpivoted, commit_every=self.commit_every
                )
                count["exposures_unpivoted"] = affected_rows
                self.log.debug(f"Stored unpivoted exposure records: affected_rows={affected_rows}")
                if not count["exposures"]:
                    count["exposures"] = len(results["exposures"])

        # Store unpivoted visits
        if results["visits_unpivoted"]:
            df_visits_unpivoted = pandas.DataFrame(results["visits_unpivoted"])
            if not df_visits_unpivoted.empty:
                vis_unpivoted_dao = VisitEfdUnpivotedDao(db_uri=self.db_uri, schema=schema, logger=self.log)
                affected_rows = vis_unpivoted_dao.upsert(
                    df=df_visits_unpivoted, commit_every=self.commit_every
                )
                count["visits1_unpivoted"] = affected_rows
                self.log.debug(f"Stored unpivoted visit records: affected_rows={affected_rows}")
                if not count["visits1"]:
                    count["visits1"] = len(results["visits"])

        return count

    @handle_processing_errors
    def _query_efd_values(
        self,
        topic: Dict[str, Any],
        topic_interval: List[astropy.time.Time],
        packed_series: bool = False,
    ) -> pandas.DataFrame:
        """
        Query EFD values for a topic within a specified time interval.

        This method acts as a high-level wrapper around the EFD client (DAO),
        preparing parameters and delegating the actual database query. The underlying
        DAO is responsible for handling query complexities, such as chunking
        large requests.
        """
        # 1. Prepare parameters from the input topic and interval
        start = topic_interval[0].utc
        end = topic_interval[1].utc
        fields = list(topic["fields"])  # Use a list copy

        aggregate_interval = topic.get("pre_aggregate_interval")
        aggregate_func = topic.get("function")

        self.log.info(f"Querying topic '{topic['name']}' from {start.iso} to {end.iso}.")
        if aggregate_interval:
            self.log.info(f"Aggregation: interval={aggregate_interval}, function={aggregate_func}")

        # 2. Delegate the query to the appropriate DAO method
        try:
            if packed_series:
                self.log.debug(f"Calling select_packed_time_series for {len(fields)} base fields.")
                return self.efd.select_packed_time_series(
                    topic_name=topic["name"],
                    base_fields=fields,
                    start=start,
                    end=end,
                    ref_timestamp_scale="utc",
                )
            else:
                self.log.debug(f"Calling select_time_series for {len(fields)} fields.")
                return self.efd.select_time_series(
                    topic_name=topic["name"],
                    fields=fields,
                    start=start,
                    end=end,
                    aggregate_interval=aggregate_interval,
                    aggregate_func=aggregate_func,
                )
        except Exception as e:
            # 3. Handle any exceptions from the DAO and return an empty DataFrame
            self.log.error(
                f"DAO query failed for topic '{topic['name']}': {e}",
                exc_info=True,  # Provides a full traceback in the logs
            )
            return pandas.DataFrame()

    def _update_bounds(
        self,
        timespans: List[dict],
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
        min_time: astropy.time.Time,
        max_time: astropy.time.Time,
    ) -> tuple[astropy.time.Time, astropy.time.Time]:
        """Update time bounds based on items within the given interval."""

        for item in timespans:
            ts = item["timespan"]
            if ts.begin.utc >= start_time and ts.end.utc <= end_time:
                min_time = min(ts.begin.utc, min_time)
                max_time = max(ts.end.utc, max_time)

        return min_time, max_time

    @handle_processing_errors
    def _get_topic_interval(
        self,
        start_time: astropy.time.Time,
        end_time: astropy.time.Time,
        exposures: List[dict],
        visits: List[dict],
    ) -> List[astropy.time.Time]:
        """Get the time bounds within the given interval."""

        min_topic_time = end_time
        max_topic_time = start_time

        min_topic_time, max_topic_time = self._update_bounds(
            exposures, start_time, end_time, min_topic_time, max_topic_time
        )

        min_topic_time, max_topic_time = self._update_bounds(
            visits, start_time, end_time, min_topic_time, max_topic_time
        )

        return [min_topic_time, max_topic_time]
