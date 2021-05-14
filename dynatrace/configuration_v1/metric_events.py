from typing import List, Optional, Dict, Any
from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient


class MetricEventTextFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.value: str = raw_element.get("value")
        self.operator: str = raw_element.get("operator")


class TagFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.context: str = raw_element.get("context")
        self.key: str = raw_element.get("key")
        self.value: str = raw_element.get("value")


class MetricEventAlertingScope(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.filter_type: str = raw_element.get("filterType")
        self.tag_filter: TagFilter = TagFilter(raw_element=raw_element.get("tagFilter"))
        self.name_filter: MetricEventTextFilter = MetricEventTextFilter(raw_element=raw_element.get("nameFilter"))
        self.entity_id: str = raw_element.get("entityId")
        self.management_zone_id: str = raw_element.get("mzId")
        self.process_group_id: str = raw_element.get("processGroupId")


class MetricEventDimension(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.filter_type: str = raw_element.get("filterType")
        self.key: str = raw_element.get("key")
        self.name_filter: MetricEventTextFilter = MetricEventTextFilter(raw_element=raw_element.get("nameFilter"))
        self.text_filter: MetricEventTextFilter = MetricEventTextFilter(raw_element=raw_element.get("textFilter"))


class MetricEventStaticThresholdMonitoringStrategy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: str = raw_element.get("type")
        self.samples: int = raw_element.get("samples")
        self.violating_samples: int = raw_element.get("violatingSamples")
        self.dealtering_samples: int = raw_element.get("dealertingSamples")
        self.alert_condition: str = raw_element.get("alertCondition")
        self.alerting_on_missing_data: Optional[bool] = raw_element.get("alertingOnMissingData")
        self.number_of_signal_fluctuations: int = raw_element.get("numberOfSignalFluctuations")
        self.threshold: int = raw_element.get("threshold")
        self.unit: str = raw_element.get("unit")


class MetricEventMonitoringStrategy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type = raw_element.get("type")


class MetricEvent(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))
        self.id: str = raw_element.get("id")
        self.metric_id: str = raw_element.get("metricId")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")
        self.aggregation_type: str = raw_element.get("aggregationType")
        self.severity = raw_element.get("severity")
        self.enabled: bool = raw_element.get("enabled")
        self.disabled_reason: str = raw_element.get("disabledReason")
        self.warning_reason: str = raw_element.get("warningReason")
        self.alerting_scope: List[MetricEventAlertingScope] = [
            MetricEventAlertingScope(raw_element=raw_scope) for raw_scope in raw_element.get("alertingScope", [])
        ]
        self.metric_dimensions: List[MetricEventDimension] = [
            MetricEventDimension(raw_element=raw_dimension) for raw_dimension in raw_element.get("metricDimensions", [])
        ]
        self.monitoring_strategy: MetricEventMonitoringStrategy = MetricEventMonitoringStrategy(raw_element=raw_element.get("monitoringStrategy"))
        self.primary_dimension_key: str = raw_element.get("primaryDimensionKey")


class MetricEventShortRepresentation(EntityShortRepresentation):
    def delete(self) -> Response:
        """
        Deletes this metric event
        """
        return self._http_client.make_request(f"/api/config/v1/anomalyDetection/metricEvents/{self.id}", method="DELETE")

    def get_full_metric_event(self) -> MetricEvent:
        """
        Gets the full metric event for this stub
        """
        response = self._http_client.make_request(f"/api/config/v1/anomalyDetection/metricEvents/{self.id}").json()
        return MetricEvent(self._http_client, None, response)


class MetricEventService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList[MetricEventShortRepresentation]:
        """
        Lists all metric events in the environment. No configurable parameters.
        """
        return PaginatedList(MetricEventShortRepresentation, self.__http_client, f"/api/config/v1/anomalyDetection/metricEvents", list_item="values")
