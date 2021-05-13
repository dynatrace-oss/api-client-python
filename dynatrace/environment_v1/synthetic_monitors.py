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
        self.type: str = raw_element.get("type")
        self.enabled: bool = raw_element.get("enabled")

class SyntheticMonitorsService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList[MonitorCollectionElement]:
        """
        Lists all Synthetic monitors in the environment.
        """
        return PaginatedList(MonitorCollectionElement, self.__http_client, f"/api/v1/synthetic/monitors", list_item="monitors")