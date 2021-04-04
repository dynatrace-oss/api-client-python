from datetime import datetime
from typing import List

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class MetricService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def query(
        self,
        metric_selector: str,
        resolution: str = None,
        time_from=None,
        time_to=None,
        entity_selector=None,
    ) -> PaginatedList["MetricSeriesCollection"]:
        """

        :param metric_selector: The metric selector: https://www.dynatrace.com/support/help/shortlink/api-metrics-v2-selector
        :param resolution:
        :param time_from:
        :param time_to:
        :param entity_selector:
        :return:
        """

        params = {
            "metricSelector": metric_selector,
            "resolution": resolution,
            "from": time_from,
            "to": time_to,
            "entitySelector": entity_selector,
        }
        return PaginatedList(MetricSeriesCollection, self.__http_client, "/api/v2/metrics/query", params, list_item="result")

    def list(self, metric_selector: str = None, text: str = None, fields: str = None, page_size=100) -> PaginatedList["MetricDescriptor"]:
        params = {
            "pageSize": page_size,
            "metricSelector": metric_selector,
            "text": text,
            "fields": fields,
        }
        return PaginatedList(MetricDescriptor, self.__http_client, "/api/v2/metrics", params, list_item="metrics")

    def get(self, metric_id: str) -> "MetricDescriptor":
        response = self.__http_client.make_request(f"/api/v2/metrics/{metric_id}").json()
        return MetricDescriptor(self.__http_client, None, response)

    def ingest(self, lines: List[str]):
        lines = "\n".join(lines)
        return self.__http_client.make_request(
            f"/api/v2/metrics/ingest", method="POST", data=lines, headers={"Content-Type": "text/plain; charset=utf-8"}
        ).json()


class MetricSeries(DynatraceObject):
    @property
    def timestamps(self) -> List[datetime]:
        return self._timestamps

    @property
    def dimensions(self) -> List[str]:
        return self._dimensions

    @property
    def values(self) -> List[float]:
        return self._values

    def _create_from_raw_data(self, raw_element):
        self._timestamps = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in raw_element.get("timestamps", [])]
        self._dimensions = raw_element.get("dimensions", [])
        self._values = raw_element.get("values", [])


class MetricSeriesCollection(DynatraceObject):
    @property
    def metric_id(self) -> str:
        return self._metric_id

    @property
    def data(self) -> List[MetricSeries]:
        return self._data

    def _create_from_raw_data(self, raw_element: dict):
        self._metric_id = raw_element.get("metricId")
        self._data = [MetricSeries(self._http_client, self._headers, metric_serie) for metric_serie in raw_element.get("data", [])]


class MetricDefaultAggregation(DynatraceObject):
    @property
    def parameter(self) -> float:
        """
        The percentile to be delivered. Valid values are between 0 and 100.
        Applicable only to the percentile aggregation type.
        """
        return self._parameter

    @property
    def type(self) -> str:
        """
        The type of default aggregation.
        [ auto, avg, count, max, median, min, percentile, sum, value ]
        """
        return self._type

    def _create_from_raw_data(self, raw_element):
        self._parameter = raw_element.get("parameter")
        self._type = raw_element.get("type")


class MetricDimensionDefinition(DynatraceObject):
    @property
    def index(self) -> int:
        """
        The unique 0-based index of the dimension.
        :return:
        """
        return self._index

    @property
    def name(self) -> int:
        """
        The name of the dimension.
        :return:
        """
        return self._name

    @property
    def key(self) -> int:
        """
        The key of the dimension.
        :return:
        """
        return self._key

    @property
    def type(self) -> int:
        """
        The type of the dimension.
        :return:[ ENTITY, NUMBER, OTHER, STRING, VOID ]
        """
        return self._type

    def _create_from_raw_data(self, raw_element):
        self._index = raw_element.get("index")
        self._name = raw_element.get("name")
        self._key = raw_element.get("key")
        self._type = raw_element.get("type")


class MetricDescriptor(DynatraceObject):
    @property
    def default_aggregation(self) -> MetricDefaultAggregation:
        """
        The default aggregation of a metric.
        """
        return self._default_aggregation

    @property
    def dimension_definitions(self) -> List[MetricDimensionDefinition]:
        """
        The fine metric division (for example, process group and process ID for some process-related metric).
        """
        return self._dimension_definitions

    @property
    def metric_id(self) -> str:
        """
        The fully qualified key of the metric.
        If a transformation has been used it is reflected in the metric key.
        """
        return self._metric_id

    @property
    def entity_type(self):
        return self._entity_type

    @property
    def aggregation_types(self):
        return self._aggregation_types

    @property
    def description(self):
        return self._description

    @property
    def transformations(self):
        return self._transformations

    @property
    def unit(self):
        return self._unit

    @property
    def display_name(self):
        return self._display_name

    def _create_from_raw_data(self, raw_element):
        self._default_aggregation = (
            MetricDefaultAggregation(self._http_client, self._headers, raw_element.get("defaultAggregation")) if raw_element.get("defaultAggregation") else None
        )
        self._dimension_definitions = [
            MetricDimensionDefinition(self._http_client, self._headers, element) for element in raw_element.get("dimensionDefinitions", [])
        ]

        self._metric_id = raw_element.get("metricId")
        self._description = raw_element.get("description")
        self._entity_type = raw_element.get("entityType")
        self._aggregation_types = raw_element.get("aggregationTypes")
        self._transformations = raw_element.get("transformations")
        self._unit = raw_element.get("unit")
        self._display_name = raw_element.get("displayName")
