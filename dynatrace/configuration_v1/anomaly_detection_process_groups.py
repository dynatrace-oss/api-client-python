from typing import List, Optional, Dict, Any, Union
from enum import Enum
from requests import Response

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

    def json(self):
        """
        Get the json representation of this process group anomaly detection config.
        """
        if self.availability_monitoring.method == Method.MINIMUM_THRESHOLD:
            json = {
                "availabilityMonitoring": {
                    "method": self.availability_monitoring.method.value,
                    "minimumThreshold": self.availability_monitoring.minimum_threshold,
                }
            }
        else:
            json = {"availabilityMonitoring": {"method": self.availability_monitoring.method.value}}
        return json

    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.availability_monitoring: AvailabilityMonitoringPG = AvailabilityMonitoringPG(
            self._http_client, raw_element=raw_element.get("availabilityMonitoring")
        )


class AnomalyDetectionPGService:
    # TODO - Early adopter endpoint, be sure to check back in for updates
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get_configuration(self, id: str):
        """
        Get the anomaly detection configuration for the specified process group.
        """
        return AnomalyDetectionPG(self.__http_client, raw_element=self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}").json())

    def put_configuration(self, id: str, anomaly_detection_config: AnomalyDetectionPG):
        """
        Update the anomaly detection configuration for the specified process group.
        """
        return self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}", method="PUT", params=anomaly_detection_config.json())

    def delete_configuration(self, id: str):
        """
        Deletes the anomaly detection configuration for the process group. This is the same as turning availaility monitoring off.
        """
        return self.__http_client.make_request(f"/api/config/v1/anomalyDetection/processGroups/{id}", method="DELETE")
