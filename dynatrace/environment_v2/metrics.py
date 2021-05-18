"""
Copyright 2021 Dynatrace LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Dict, Any

from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.utils import timestamp_to_string, int64_to_datetime


class MetricService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def query(
        self,
        metric_selector: str,
        resolution: str = None,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None,
        entity_selector: Optional[str] = None,
    ) -> PaginatedList["MetricSeriesCollection"]:

        params = {
            "metricSelector": metric_selector,
            "resolution": resolution,
            "from": timestamp_to_string(time_from),
            "to": timestamp_to_string(time_to),
            "entitySelector": entity_selector,
        }
        return PaginatedList(MetricSeriesCollection, self.__http_client, "/api/v2/metrics/query", params, list_item="result")

    def list(
        self,
        metric_selector: Optional[str] = None,
        text: Optional[str] = None,
        fields: Optional[str] = None,
        written_since: Optional[Union[str, datetime]] = None,
        metadata_selector: Optional[str] = None,
        page_size=100,
    ) -> PaginatedList["MetricDescriptor"]:
        params = {
            "pageSize": page_size,
            "metricSelector": metric_selector,
            "text": text,
            "fields": fields,
            "writtenSince": timestamp_to_string(written_since),
            "metadataSelector": metadata_selector,
        }
        return PaginatedList(MetricDescriptor, self.__http_client, "/api/v2/metrics", params, list_item="metrics")

    def get(self, metric_id: str) -> "MetricDescriptor":
        response = self.__http_client.make_request(f"/api/v2/metrics/{metric_id}").json()
        return MetricDescriptor(http_client=self.__http_client, raw_element=response)

    def delete(self, metric_id) -> Response:
        return self.__http_client.make_request(f"/api/v2/metrics/{metric_id}", method="DELETE")

    def ingest(self, lines: List[str]):
        lines = "\n".join(lines)
        return self.__http_client.make_request(
            f"/api/v2/metrics/ingest", method="POST", data=lines, headers={"Content-Type": "text/plain; charset=utf-8"}
        ).json()


class MetricSeries(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.timestamps: List[datetime] = [int64_to_datetime(timestamp) for timestamp in raw_element.get("timestamps", [])]
        self.dimensions: List[str] = raw_element.get("dimensions", [])
        self.values: List[float] = raw_element.get("values", [])
        self.dimension_map: Optional[Dict[str, Any]] = raw_element.get("dimensionMap", [])


class MetricSeriesCollection(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        self.metric_id: str = raw_element.get("metricId")
        self.data: List[MetricSeries] = [MetricSeries(self._http_client, self._headers, metric_serie) for metric_serie in raw_element.get("data", [])]
        self.warnings: Optional[List[str]] = raw_element.get("warnings")


class MetricDefaultAggregation(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.parameter: float = raw_element.get("parameter")
        self.type: str = raw_element.get("type")


class MetricDimensionDefinition(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.index: int = raw_element.get("index")
        self.name: str = raw_element.get("name")
        self.key: str = raw_element.get("key")
        self.type: str = raw_element.get("type")


class AggregationType(Enum):
    AUTO = "auto"
    AVG = "avg"
    COUNT = "count"
    MAX = "max"
    MEDIAN = "median"
    MIN = "min"
    PERCENTILE = "percentile"
    SUM = "sum"
    VALUE = "value"


class Transformation(Enum):
    DEFAULT = "default"
    FILTER = "filter"
    FOLD = "fold"
    LAST = "last"
    LIMIT = "limit"
    MERGE = "merge"
    NAMES = "names"
    PARENTS = "parents"
    RATE = "rate"
    SORT = "sort"
    SPLITBY = "splitBy"
    TIMESHIFT = "timeshift"


class Unit(Enum):
    BIT = "Bit"
    BITPERHOUR = "BitPerHour"
    BITPERMINUTE = "BitPerMinute"
    BITPERSECOND = "BitPerSecond"
    BYTE = "Byte"
    BYTEPERHOUR = "BytePerHour"
    BYTEPERMINUTE = "BytePerMinute"
    BYTEPERSECOND = "BytePerSecond"
    CORES = "Cores"
    COUNT = "Count"
    DAY = "Day"
    DECIBELMILLIWATT = "DecibelMilliWatt"
    GIBIBYTE = "GibiByte"
    GIGA = "Giga"
    GIGABYTE = "GigaByte"
    HOUR = "Hour"
    KIBIBYTE = "KibiByte"
    KIBIBYTEPERHOUR = "KibiBytePerHour"
    KIBIBYTEPERMINUTE = "KibiBytePerMinute"
    KIBIBYTEPERSECOND = "KibiBytePerSecond"
    KILO = "Kilo"
    KILOBYTE = "KiloByte"
    KILOBYTEPERHOUR = "KiloBytePerHour"
    KILOBYTEPERMINUTE = "KiloBytePerMinute"
    KILOBYTEPERSECOND = "KiloBytePerSecond"
    MSU = "MSU"
    MEBIBYTE = "MebiByte"
    MEBIBYTEPERHOUR = "MebiBytePerHour"
    MEBIBYTEPERMINUTE = "MebiBytePerMinute"
    MEBIBYTEPERSECOND = "MebiBytePerSecond"
    MEGA = "Mega"
    MEGABYTE = "MegaByte"
    MEGABYTEPERHOUR = "MegaBytePerHour"
    MEGABYTEPERMINUTE = "MegaBytePerMinute"
    MEGABYTEPERSECOND = "MegaBytePerSecond"
    MICROSECOND = "MicroSecond"
    MILLICORES = "MilliCores"
    MILLISECOND = "MilliSecond"
    MILLISECONDPERMINUTE = "MilliSecondPerMinute"
    MINUTE = "Minute"
    MONTH = "Month"
    NANOSECOND = "NanoSecond"
    NANOSECONDPERMINUTE = "NanoSecondPerMinute"
    NOTAPPLICABLE = "NotApplicable"
    PERHOUR = "PerHour"
    PERMINUTE = "PerMinute"
    PERSECOND = "PerSecond"
    PERCENT = "Percent"
    PIXEL = "Pixel"
    PROMILLE = "Promille"
    RATIO = "Ratio"
    SECOND = "Second"
    STATE = "State"
    UNSPECIFIED = "Unspecified"
    WEEK = "Week"
    YEAR = "Year"


class MetricDescriptor(DynatraceObject):
    def _create_from_raw_data(self, raw_element):

        # required
        self.metric_id: str = raw_element.get("metricId")

        # optional
        self.aggregation_types: Optional[List[AggregationType]] = [AggregationType(element) for element in raw_element.get("aggregationTypes", [])]
        self.created: Optional[datetime] = int64_to_datetime(raw_element.get("created"))
        self.ddu_billable: Optional[bool] = raw_element.get("dduBillable")
        self.default_aggregation: Optional[MetricDefaultAggregation] = MetricDefaultAggregation(raw_element=raw_element.get("defaultAggregation"))
        self.description: Optional[str] = raw_element.get("description")
        self.dimension_definitions: Optional[List[MetricDimensionDefinition]] = [
            MetricDimensionDefinition(raw_element=element) for element in raw_element.get("dimensionDefinitions", [])
        ]
        self.display_name: Optional[str] = raw_element.get("displayName")
        self.entity_type: Optional[List[str]] = raw_element.get("entityType", [])
        self.impact_relevant: Optional[bool] = raw_element.get("impactRelevant")
        self.last_written: Optional[datetime] = int64_to_datetime(raw_element.get("lastWritten"))
        self.maximum_value: Optional[float] = raw_element.get("maximumValue")
        self.metric_value_type: Optional["MetricValueType"] = (
            MetricValueType(raw_element=raw_element.get("metricValueType")) if raw_element.get("metricValueType") else None
        )
        self.minimum_value: Optional[float] = raw_element.get("minimumValue")
        self.root_cause_relevant: Optional[bool] = raw_element.get("rootCauseRelevant")
        self.tags: Optional[List[str]] = raw_element.get("tags")
        self.transformations: Optional[List[Transformation]] = [Transformation(element) for element in raw_element.get("transformations", [])]
        self.unit: Optional[Unit] = Unit(raw_element.get("unit"))
        self.warnings: Optional[List[str]] = raw_element.get("warnings")


class ValueType(Enum):
    ERROR = "error"
    SCORE = "score"
    UNKNOWN = "unknown"


class MetricValueType(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type = ValueType(raw_element.get("type"))
