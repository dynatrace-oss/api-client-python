from typing import List, Optional, Dict, Any
from enum import Enum
from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient

class MonitoringMethod(Enum):
    OFF = "OFF"
    MINIMUM_THRESHOLD = "MINIMUM_THRESHOLD"
    PROCESS_IMPACT = "PROCESS_IMPACT"

class AvailabilityMonitoringPG(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.method: MonitoringMethod = MonitoringMethod(raw_element.get("method"))
        self.minimum_threshold: int = raw_element.get("minimumThreshold") 

class AnomalyDetectionPG(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.availability_monitoring: AvailabilityMonitoringPG = AvailabilityMonitoringPG(raw_element=raw_element.get("availabilityMonitoring"))

class AnomalyDetectionPGService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get_configuration(self, id: str):
        """
        Get the anomaly detection configuration for the specified process group.
        """
        return AnomalyDetectionPG(raw_element=self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}").json())

    def update_configuration(self, id: str, method: str, minimum_threshold: Optional[int] = None):
        """
        Update the anomaly detection configuration for the specified process group.
        """
        if method == "MINIMUM_THRESHOLD":
            body = {"availabilityMonitoring": {"method": method, "minimumThreshold": minimum_threshold}}
        else:
            body = {"availabilityMonitoring": {"method": method}}
        return self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}", method="PUT", params=body)

    def delete_configuration(self, id:str):
        """
        Deletes the anomaly detection configuration for the process group. This is the same as turning availaility monitoring off.
        """
        return self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}", method="DELETE")
