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
        return self.__http_client.make_request(f"/api/v2/metrics/ingest", method="POST", data=lines, headers={"Content-Type": "text/plain; charset=utf-8"}).json()


class MetricSeries(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.timestamps: List[datetime] = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in raw_element.get("timestamps", [])]
        self.dimensions: List[str] = raw_element.get("dimensions", [])
        self.values: List[float] = raw_element.get("values", [])


class MetricSeriesCollection(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        self.metric_id: str = raw_element.get("metricId")
        self.data: List[MetricSeries] = [MetricSeries(self._http_client, self._headers, metric_serie) for metric_serie in raw_element.get("data", [])]


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


class MetricDescriptor(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        # TODO - Several more properties needed, document optional ones
        self.default_aggregation: MetricDefaultAggregation = (
            MetricDefaultAggregation(self._http_client, self._headers, raw_element.get("defaultAggregation")) if raw_element.get("defaultAggregation") else None
        )
        self.dimension_definitions: List[MetricDimensionDefinition] = [MetricDimensionDefinition(self._http_client, self._headers, element) for element in raw_element.get("dimensionDefinitions", [])]

        self.metric_id: str = raw_element.get("metricId")
        self.description: str = raw_element.get("description")
        self.entity_type: str = raw_element.get("entityType")
        self.aggregation_types: str = raw_element.get("aggregationTypes")
        self.transformations: List[str] = raw_element.get("transformations")
        self.unit: str = raw_element.get("unit")
        self.display_name: str = raw_element.get("displayName")
