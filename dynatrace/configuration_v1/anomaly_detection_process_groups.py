from typing import List, Optional, Dict, Any, Union
from enum import Enum
from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient

class Method(Enum):
    OFF = "OFF"
    MINIMUM_THRESHOLD = "MINIMUM_THRESHOLD"
    PROCESS_IMPACT = "PROCESS_IMPACT"

class AvailabilityMonitoringPG(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.method: Method = Method(raw_element.get("method"))
        self.minimum_threshold: int = raw_element.get("minimumThreshold") 

class AnomalyDetectionPG(DynatraceObject):
    @staticmethod
    def create(method: Union[str, Method], minimum_threshold: Optional[int] = None):
        method = Method(method)
        if method == Method.MINIMUM_THRESHOLD:
            raw_element = {"availabilityMonitoring": {"method": method.value, "minimumThreshold": minimum_threshold}}
        else:
            raw_element = {"availabilityMonitoring": {"method": method.value}}
        return AnomalyDetectionPG(raw_element=raw_element)

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

    def update_configuration(self, id: str, anomaly_detection_config: AnomalyDetectionPG):
        """
        Update the anomaly detection configuration for the specified process group.
        """
        if anomaly_detection_config.availability_monitoring.method == Method.MINIMUM_THRESHOLD:
            print(anomaly_detection_config)
            body = {"availabilityMonitoring": {"method": anomaly_detection_config.availability_monitoring.method.value, "minimumThreshold": anomaly_detection_config.availability_monitoring.minimum_threshold}}
        else:
            body = {"availabilityMonitoring": {"method": anomaly_detection_config.availability_monitoring.method.value}}
        return self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}", method="PUT", params=body)

    def delete_configuration(self, id:str):
        """
        Deletes the anomaly detection configuration for the process group. This is the same as turning availaility monitoring off.
        """
        return self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}", method="DELETE")
