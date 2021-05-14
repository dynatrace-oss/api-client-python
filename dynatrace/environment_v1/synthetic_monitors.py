from typing import List, Optional, Dict, Any
from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient

class MonitorCollectionElement(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.name: str = raw_element.get("name")
        self.entity_id: str = raw_element.get("entityId")
        self.monitor_type: str = raw_element.get("type")
        self.enabled: bool = raw_element.get("enabled")

class OutageHandlingPolicy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.global_outage: bool = raw_element.get("globalOutage")
        self.local_outage: bool = raw_element.get("localOutage")

class LoadingTimeThreshold(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: str = raw_element.get("type")
        self.value_ms: int = raw_element.get("valueMs")
        self.request_index: int = raw_element.get("requestIndex")
        self.event_index: int = raw_element.get("eventIndex")

class LoadingTimeThresholdsPolicy(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: bool = raw_element.get("enabled")
        self.thresholds: List[LoadingTimeThreshold] = [LoadingTimeThreshold(raw_element=threshold) for threshold in raw_element.get("thresholds")]

class AnomalyDetection(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        pass

class TagWithSourceInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.source: str = raw_element.get("source")
        self.context: str = raw_element.get("context")
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
        self.enabled: bool = raw_element.hget("enabled")
        self.type: str = raw_element.get("type")
        self.created_from: str = raw_element.get("createdFrom")
        self.script: dict = raw_element.get("script")
        self.locations: List[str] = raw_element.get("locations")
        self.anomaly_detection: AnomalyDetection  = AnomalyDetection(raw_element=raw_element.get("anomalyDetection"))
        self.tags: List[TagWithSourceInfo] = [TagWithSourceInfo(raw_element=tag) for tag in raw_element.get("tags")]
        self.management_zones: List[ManagementZone] = [ManagementZone(raw_element=zone) for zone in raw_element.get("managementZones")]
        self.automatically_assigned_apps: List[str] = raw_element.get("automaticallyAssignedApps")
        self.manually_assigned_apps: List[str] = raw_element.get("manuallyAssignedApps")

class SyntheticMonitorsService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self, monitor_type: Optional[str] = None) -> PaginatedList[MonitorCollectionElement]:
        """
        Lists all synthetic monitors in the environment.
        """
        params = {}
        if monitor_type is not None:
            params.update({"type": monitor_type})
        return PaginatedList(MonitorCollectionElement, self.__http_client, f"/api/v1/synthetic/monitors",target_params=params, list_item="monitors")

    def get_full_monitor_configuration(self, monitor_id: str) -> SyntheticMonitor:
        """
        Get full monitor configuration for the specified monitor id (aka entity id).
        """
        return SyntheticMonitor(raw_element=self.__http_client.make_request(f"/api/v1/synthetic/monitors/{monitor_id}").json())