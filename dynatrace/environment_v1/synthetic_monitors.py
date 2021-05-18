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

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient


class MonitorType(Enum):
    BROWSER = "BROWSER"
    HTTP = "HTTP"


class LoadingTimeThresholdType(Enum):
    ACTION = "ACTION"
    TOTAL = "TOTAL"


class TagSource(Enum):
    AUTO = "AUTO"
    RULE_BASED = "RULE_BASED"
    USER = "USER"


class CreatedFrom(Enum):
    API = "API"
    GUI = "GUI"


class TagContext(Enum):
    AWS = "AWS"
    AWS_GENERIC = "AWS_GENERIC"
    AZURE = "AZURE"
    CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
    CONTEXTLESS = "CONTEXTLESS"
    ENVIRONMENT = "ENVIRONMENT"
    GOOGLE_CLOUD = "GOOGLE_CLOUD"
    KUBERNETES = "KUBERNETES"


class MonitorCollectionElement(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.name: str = raw_element.get("name")
        self.entity_id: str = raw_element.get("entityId")
        self.monitor_type: str = raw_element.get("type")
        self.enabled: bool = raw_element.get("enabled")


class LocalOutagePolicy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.affected_locations: int = raw_element.get("affectedLocations")
        self.consecutive_runs: int = raw_element.get("consecutiveRuns")


class OutageHandlingPolicy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.global_outage: bool = raw_element.get("globalOutage")
        self.local_outage: bool = raw_element.get("localOutage")
        self.local_outage_policy: LocalOutagePolicy = LocalOutagePolicy(raw_element=raw_element.get("localOutagePolicy"))
        self.retry_on_error: bool = raw_element.get("retryOnError")


class LoadingTimeThreshold(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: LoadingTimeThresholdType = LoadingTimeThresholdType(raw_element.get("type"))
        self.value_ms: int = raw_element.get("valueMs")
        self.request_index: int = raw_element.get("requestIndex")
        self.event_index: int = raw_element.get("eventIndex")


class LoadingTimeThresholdsPolicyDto(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: bool = raw_element.get("enabled")
        self.thresholds: List[LoadingTimeThreshold] = [LoadingTimeThreshold(raw_element=threshold) for threshold in raw_element.get("thresholds")]


class AnomalyDetection(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.outage_handling: OutageHandlingPolicy = OutageHandlingPolicy(raw_element=raw_element.get("outageHandling"))
        self.loading_time_thresholds: LoadingTimeThresholdsPolicyDto = LoadingTimeThresholdsPolicyDto(raw_element=raw_element.get("loadingTimeThresholds"))


class TagWithSourceInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.source: TagSource = TagSource(raw_element.get("source"))
        self.context: TagContext = TagContext(raw_element.get("context"))
        self.key: str = raw_element.get("key")
        self.value: str = raw_element.get("value")


class ManagementZone(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")


class SyntheticMonitor(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.entity_id: str = raw_element.get("entityId")
        self.name: str = raw_element.get("name")
        self.frequency_min: int = raw_element.get("frequencyMin")
        self.enabled: bool = raw_element.get("enabled")
        self.type: MonitorType = MonitorType(raw_element.get("type"))
        self.created_from: CreatedFrom = CreatedFrom(raw_element.get("createdFrom"))
        self.script: dict = raw_element.get("script")
        self.locations: List[str] = raw_element.get("locations")
        self.anomaly_detection: AnomalyDetection = AnomalyDetection(raw_element=raw_element.get("anomalyDetection"))
        self.tags: List[TagWithSourceInfo] = [TagWithSourceInfo(raw_element=tag) for tag in raw_element.get("tags")]
        self.management_zones: List[ManagementZone] = [ManagementZone(raw_element=zone) for zone in raw_element.get("managementZones")]
        self.automatically_assigned_apps: List[str] = raw_element.get("automaticallyAssignedApps")
        self.manually_assigned_apps: List[str] = raw_element.get("manuallyAssignedApps")


class SyntheticMonitorsService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self, monitor_type: Optional[Union[MonitorType, str]] = None) -> PaginatedList[MonitorCollectionElement]:
        """
        Lists all synthetic monitors in the environment.
        """
        params = {"type": MonitorType(monitor_type).value if monitor_type else None}
        return PaginatedList(MonitorCollectionElement, self.__http_client, f"/api/v1/synthetic/monitors", target_params=params, list_item="monitors")

    def get_full_monitor_configuration(self, monitor_id: str) -> SyntheticMonitor:
        """
        Get full monitor configuration for the specified monitor id (aka entity id).
        """
        return SyntheticMonitor(self.__http_client, raw_element=self.__http_client.make_request(f"/api/v1/synthetic/monitors/{monitor_id}").json())
