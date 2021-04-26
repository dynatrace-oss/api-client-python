from typing import List, Optional
from requests import Response

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient

class MetricEventTextFilter(DynatraceObject):
    @property
    def value(self) -> str:
        return self._value

    @property
    def operator(self) -> str:
        return self._operator

    def _create_from_raw_data(self, raw_element):
        self._value = raw_element.get("value")
        self._operator = raw_element.get("operator")

class TagFilter(DynatraceObject):
    @property
    def context(self) -> str:
        return self._context

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> str:
        return self._value

    def _create_from_raw_data(self, raw_element):
        self._context = raw_element.get("context")
        self._key = raw_element.get("key")
        self._value = raw_element.get("value")

class MetricEventAlertingScope(DynatraceObject):
    @property
    def filter_type(self) -> str:
        return self._filter_type

    @property
    def tag_filter(self) -> TagFilter:
        return self._tag_filter

    @property
    def name_filter(self) -> MetricEventTextFilter:
        return self._name_filter

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @property
    def management_zone(self) -> str:
        return self._management_zone_id

    @property
    def process_group_id(self) -> str:
        return self._process_group_id

    def _create_from_raw_data(self, raw_element):
        self._filter_type = raw_element.get("filterType")
        self._tag_filter = TagFilter(raw_element=raw_element.get("tagFilter"))
        self._name_filter = MetricEventTextFilter(raw_element=raw_element.get("nameFilter"))
        self._entity_id = raw_element.get("entityId")
        self._management_zone_id = raw_element.get("mzId")
        self._process_group_id = raw_element.get("processGroupId")

class MetricEventDimension(DynatraceObject):
    @property
    def filter_type(self) -> str:
        return self._filter_type

    @property
    def key(self) -> str:
        return self._key

    @property
    def name_filter(self) -> MetricEventTextFilter:
        return self._name_filter

    @property
    def text_filter(self) -> MetricEventTextFilter:
        return self._text_filter
    
    def _create_from_raw_data(self, raw_element):
        self._filter_type = raw_element.get("filterType")
        self._key = raw_element.get("key")
        self._name_filter = MetricEventTextFilter(raw_element=raw_element.get("nameFilter"))
        self._text_filter = MetricEventTextFilter(raw_element=raw_element.get("textFilter"))

class MetricEventMonitoringStrategy(DynatraceObject):
    @property
    def type(self) -> str:
        return self._type

    @property
    def samples(self) -> int:
        return self._samples

    @property
    def violating_samples(self) -> int:
        return self._violating_samples

    @property
    def dealtering_samples(self) -> int:
        return self._dealtering_samples

    @property
    def alert_condition(self) -> str:
        return self._alert_condition

    @property
    def alerting_on_missing_data(self) -> bool:
        return self._alerting_on_missing_data

    @property
    def number_of_signal_fluctuations(self) -> int:
        return self._number_of_signal_fluctuations

    @property
    def threshold(self) -> int:
        return self._threshold

    @property
    def unit(self) -> str:
        return self._unit

    def _create_from_raw_data(self, raw_element):
        self._type = raw_element.get("type")
        self._samples = raw_element.get("samples")
        self._violating_samples = raw_element.get("violatingSamples")
        self._dealtering_samples = raw_element.get("dealertingSamples")
        self._alert_condition = raw_element.get("alertCondition")
        self._alerting_on_missing_data = raw_element.get("alertingOnMissingData")
        self._number_of_signal_fluctuations = raw_element.get("numberOfSignalFluctuations")
        self._threshold = raw_element.get("threshold")
        self._unit = raw_element.get("unit")

class MetricEventMetadata(DynatraceObject):
    @property
    def configuration_versions(self) -> List[int]:
        return self._configuration_versions

    @property
    def current_configuration_versions(self) -> List[int]:
        return self._current_configuration_versions

    @property
    def cluster_version(self) -> str:
        return self._cluster_version

    def _create_from_raw_data(self, raw_element):
        self._configuration_versions = raw_element.get("configurationVersions")
        self._current_configuration_versions = raw_element.get("currentConfigurationVersions")
        self._cluster_version = raw_element.get("clusterVersion")

class MetricEvent(DynatraceObject):
    @property
    def metadata(self)-> MetricEventMetadata:
        return self._metadata

    @property
    def id(self) -> str:
        return self._id

    @property
    def metric_id(self) -> str:
        return self._metric_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def aggregation_type(self) -> str:
        return self._aggregation_type

    @property
    def severity(self) -> str:
        return self._severity

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def disabled_reason(self) -> str:
        return self._disabled_reason

    @property
    def warning_reason(self) -> str:
        return self._warning_reason

    @property
    def alerting_scope(self) -> List[MetricEventAlertingScope]:
        return self._alerting_scope

    @property
    def metric_dimensions(self) -> List[MetricEventDimension]:
        return self._metric_dimensions

    @property
    def monitoring_strategy(self) -> MetricEventMonitoringStrategy:
        return self._monitoring_strategy

    @property
    def primary_dimension_key(self) -> str:
        return self._primary_dimension_key

    def _create_from_raw_data(self, raw_element):
        self._metadata = MetricEventMetadata(raw_element=raw_element.get("metadata"))
        self._id = raw_element.get("id")
        self._metric_id = raw_element.get("metricId")
        self._name = raw_element.get("name")
        self._description = raw_element.get("description")
        self._aggregation_type = raw_element.get("aggregationType")
        self._severity = raw_element.get("severity")
        self._enabled = raw_element.get("enabled")
        self._disabled_reason = raw_element.get("disabledReason")
        self._warning_reason = raw_element.get("warningReason")
        self._alerting_scope = [MetricEventAlertingScope(raw_element=raw_scope) for raw_scope in raw_element.get("alertingScope", [])]
        self._metric_dimensions = [MetricEventDimension(raw_element=raw_dimension) for raw_dimension in raw_element.get("metricDimensions", [])]
        self._monitoring_strategy = MetricEventMonitoringStrategy(raw_element=raw_element.get("monitoringStrategy"))
        self._primary_dimension_key = raw_element.get("primaryDimensionKey")

class MetricEventStub(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._description = raw_element.get("description")

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

    def list(self) -> PaginatedList[MetricEventStub]:
        """
        Lists all metric events in the environment. No configurable parameters.
        """
        return PaginatedList(MetricEventStub, self.__http_client, f"/api/config/v1/anomalyDetection/metricEvents", list_item="values")