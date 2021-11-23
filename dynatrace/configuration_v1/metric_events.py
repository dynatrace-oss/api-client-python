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

from typing import List, Optional, Dict, Any, Union
from enum import Enum
from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient


class AggregationType(Enum):
    AVG = "AVG"
    COUNT = "COUNT"
    MAX = "MAX"
    MEDIAN = "MEDIAN"
    MIN = "MIN"
    P90 = "P90"
    SUM = "SUM"
    VALUE = "VALUE"


class AlertCondition(Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"


class DisabledReason(Enum):
    METRIC_DEFINITION_INCONSISTENCY = "METRIC_DEFINITION_INCONSISTENCY"
    NONE = "NONE"
    TOO_MANY_DIMS = "TOO_MANY_DIMS"
    TOPX_FORCIBLY_DEACTIVATED = "TOPX_FORCIBLY_DEACTIVATED"


class MetricEventAlertingScopeFilterType(Enum):
    ENTITY_ID = "ENTITY_ID"
    MANAGEMENT_ZONE = "MANAGEMENT_ZONE"
    TAG = "TAG"
    NAME = "NAME"
    CUSTOM_DEVICE_GROUP_NAME = "CUSTOM_DEVICE_GROUP_NAME"
    HOST_GROUP_NAME = "HOST_GROUP_NAME"
    HOST_NAME = "HOST_NAME"
    PROCESS_GROUP_ID = "PROCESS_GROUP_ID"
    PROCESS_GROUP_NAME = "PROCESS_GROUP_NAME"


class MetricEventDimensionsFilterType(Enum):
    ENTITY = "ENTITY"
    STRING = "STRING"


class MetricEventMonitoringStrategyType(Enum):
    STATIC_THRESHOLD = "STATIC_THRESHOLD"
    AUTO_ADAPTIVE_BASELINE = "AUTO_ADAPTIVE_BASELINE"


class Severity(Enum):
    AVAILABILITY = "AVAILABILITY"
    CUSTOM_ALERT = "CUSTOM_ALERT"
    ERROR = "ERROR"
    INFO = "INFO"
    PERFORMANCE = "PERFORMANCE"
    RESOURCE_CONTENTION = "RESOURCE_CONTENTION"


class Unit(Enum):
    BIT = "BIT"
    BIT_PER_HOUR = "BIT_PER_HOUR"
    BIT_PER_MINUTE = "BIT_PER_MINUTE"
    BIT_PER_SECOND = "BIT_PER_SECOND"
    BYTE = "BYTE"
    BYTE_PER_HOUR = "BYTE_PER_HOUR"
    BYTE_PER_MINUTE = "BYTE_PER_MINUTE"
    BYTE_PER_SECOND = "BYTE_PER_SECOND"
    CORES = "CORES"
    COUNT = "COUNT"
    DAY = "DAY"
    DECIBEL_MILLI_WATT = "DECIBEL_MILLI_WATT"
    GIBI_BYTE = "GIBI_BYTE"
    GIGA = "GIGA"
    GIGA_BYTE = "GIGA_BYTE"
    HOUR = "HOUR"
    KIBI_BYTE = "KIBI_BYTE"
    KIBI_BYTE_PER_HOUR = "KIBI_BYTE_PER_HOUR"
    KIBI_BYTE_PER_MINUTE = "KIBI_BYTE_PER_MINUTE"
    KIBI_BYTE_PER_SECOND = "KIBI_BYTE_PER_SECOND"
    KILO = "KILO"
    KILO_BYTE = "KILO_BYTE"
    KILO_BYTE_PER_HOUR = "KILO_BYTE_PER_HOUR"
    KILO_BYTE_PER_MINUTE = "KILO_BYTE_PER_MINUTE"
    KILO_BYTE_PER_SECOND = "KILO_BYTE_PER_SECOND"
    MEBI_BYTE = "MEBI_BYTE"
    MEBI_BYTE_PER_HOUR = "MEBI_BYTE_PER_HOUR"
    MEBI_BYTE_PER_MINUTE = "MEBI_BYTE_PER_MINUTE"
    MEBI_BYTE_PER_SECOND = "MEBI_BYTE_PER_SECOND"
    MEGA = "MEGA"
    MEGA_BYTE = "MEGA_BYTE"
    MEGA_BYTE_PER_HOUR = "MEGA_BYTE_PER_HOUR"
    MEGA_BYTE_PER_MINUTE = "MEGA_BYTE_PER_MINUTE"
    MEGA_BYTE_PER_SECOND = "MEGA_BYTE_PER_SECOND"
    MICRO_SECOND = "MICRO_SECOND"
    MILLI_CORES = "MILLI_CORES"
    MILLI_SECOND = "MILLI_SECOND"
    MILLI_SECOND_PER_MINUTE = "MILLI_SECOND_PER_MINUTE"
    MINUTE = "MINUTE"
    MONTH = "MONTH"
    MSU = "MSU"
    NANO_SECOND = "NANO_SECOND"
    NANO_SECOND_PER_MINUTE = "NANO_SECOND_PER_MINUTE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    PERCENT = "PERCENT"
    PER_HOUR = "PER_HOUR"
    PER_MINUTE = "PER_MINUTE"
    PER_SECOND = "PER_SECOND"
    PIXEL = "PIXEL"
    PROMILLE = "PROMILLE"
    RATIO = "RATIO"
    SECOND = "SECOND"
    STATE = "STATE"
    UNSPECIFIED = "UNSPECIFIED"
    WEEK = "WEEK"
    YEAR = "YEAR"


class WarningReason(Enum):
    NONE = "NONE"
    TOO_MANY_DIMS = "TOO_MANY_DIMS"


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
        self.filter_type: MetricEventAlertingScopeFilterType = MetricEventAlertingScopeFilterType(raw_element.get("filterType"))
        self.tag_filter: TagFilter = TagFilter(raw_element=raw_element.get("tagFilter"))
        self.name_filter: MetricEventTextFilter = MetricEventTextFilter(raw_element=raw_element.get("nameFilter"))
        self.entity_id: str = raw_element.get("entityId")
        self.management_zone_id: str = raw_element.get("mzId")
        self.process_group_id: str = raw_element.get("processGroupId")


class MetricEventDimension(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.filter_type: MetricEventDimensionsFilterType = MetricEventDimensionsFilterType(raw_element.get("filterType"))
        self.key: str = raw_element.get("key")
        self.name_filter: MetricEventTextFilter = MetricEventTextFilter(raw_element=raw_element.get("nameFilter"))
        self.text_filter: MetricEventTextFilter = MetricEventTextFilter(raw_element=raw_element.get("textFilter"))


class MetricEventMonitoringStrategy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: MetricEventMonitoringStrategyType = MetricEventMonitoringStrategyType(raw_element.get("type"))


class MetricEventAutoAdaptiveBaselineMonitoringStrategy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: MetricEventMonitoringStrategyType = MetricEventMonitoringStrategyType(raw_element.get("type"))
        self.samples: int = raw_element.get("samples")
        self.violating_samples: int = raw_element.get("violatingSamples")
        self.dealtering_samples: int = raw_element.get("dealertingSamples")
        self.alert_condition: AlertCondition = AlertCondition(raw_element.get("alertCondition"))
        self.alerting_on_missing_data: Optional[bool] = raw_element.get("alertingOnMissingData") if raw_element.get("alertingOnMissingData") else None
        self.number_of_signal_fluctuations: int = raw_element.get("numberOfSignalFluctuations")


class MetricEventStaticThresholdMonitoringStrategy(MetricEventMonitoringStrategy):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: MetricEventMonitoringStrategyType = MetricEventMonitoringStrategyType(raw_element.get("type"))
        self.samples: int = raw_element.get("samples")
        self.violating_samples: int = raw_element.get("violatingSamples")
        self.dealtering_samples: int = raw_element.get("dealertingSamples")
        self.alert_condition: AlertCondition = AlertCondition(raw_element.get("alertCondition"))
        self.alerting_on_missing_data: Optional[bool] = raw_element.get("alertingOnMissingData") if raw_element.get("alertingOnMissingData") else None
        self.threshold: int = raw_element.get("threshold")
        self.unit: Optional[Unit] = Unit(raw_element.get("unit")) if raw_element.get("unit") else None


class MetricEvent(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))
        self.id: str = raw_element.get("id")
        self.metric_id: str = raw_element.get("metricId")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")
        self.aggregation_type: Optional[AggregationType] = AggregationType(raw_element.get("aggregationType")) if raw_element.get("aggregationType") else None
        self.severity: Severity = Severity(raw_element.get("severity"))
        self.enabled: bool = raw_element.get("enabled")
        self.disabled_reason: DisabledReason = DisabledReason(raw_element.get("disabledReason"))
        self.warning_reason: WarningReason = WarningReason(raw_element.get("warningReason"))
        self.alerting_scope: List[MetricEventAlertingScope] = [
            MetricEventAlertingScope(raw_element=raw_scope) for raw_scope in raw_element.get("alertingScope", [])
        ]
        self.metric_dimensions: List[MetricEventDimension] = [
            MetricEventDimension(raw_element=raw_dimension) for raw_dimension in raw_element.get("metricDimensions", [])
        ]
        self.monitoring_strategy: Union[
            MetricEventMonitoringStrategy, MetricEventStaticThresholdMonitoringStrategy, MetricEventAutoAdaptiveBaselineMonitoringStrategy
        ] = self._create_specific_monitoring_strategy(raw_element.get("monitoringStrategy"))
        self.primary_dimension_key: str = raw_element.get("primaryDimensionKey")

    def _create_specific_monitoring_strategy(self, raw_element: Dict[str, Any]):
        strategy_type = MetricEventMonitoringStrategyType(raw_element.get("type"))
        if strategy_type == MetricEventMonitoringStrategyType.AUTO_ADAPTIVE_BASELINE:
            return MetricEventAutoAdaptiveBaselineMonitoringStrategy(raw_element=raw_element)
        elif strategy_type == MetricEventMonitoringStrategyType.STATIC_THRESHOLD:
            return MetricEventStaticThresholdMonitoringStrategy(raw_element=raw_element)
        else:
            return MetricEventMonitoringStrategy(raw_element=raw_element)


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
