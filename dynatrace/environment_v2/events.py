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

###########################################################################
# NOTE: Early Adopter implemented based on 1.226. Check back for updates. #
###########################################################################

from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime, datetime_to_int64
from dynatrace.environment_v2.custom_tags import METag
from dynatrace.environment_v2.monitored_entities import EntityStub
from dynatrace.environment_v2.schemas import ManagementZone


class EventServiceV2:
    ENDPOINT_EVENTS = "/api/v2/events"
    ENDPOINT_TYPES = "/api/v2/eventTypes"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        page_size: Optional[int] = None,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None,
        event_selector: Optional[str] = None,
        entity_selector: Optional[str] = None,
    ) -> "PaginatedList[Event]":
        params = {
            "pageSize": page_size,
            "from": time_from if isinstance(time_from, str) else datetime_to_int64(time_from),
            "to": time_to if isinstance(time_to, str) else datetime_to_int64(time_to),
            "eventSelector": event_selector,
            "entitySelector": entity_selector,
        }
        return PaginatedList(target_class=Event, http_client=self.__http_client, target_url=self.ENDPOINT_EVENTS, list_item="events", target_params=params)

    def get(self, event_id: str) -> "Event":
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_EVENTS}/{event_id}")
        return Event(raw_element=response.json(), http_client=self.__http_client)

    def list_types(self, page_size: Optional[int] = None) -> "PaginatedList[EventType]":
        params = {"pageSize": page_size}
        return PaginatedList(
            target_class=EventType, http_client=self.__http_client, target_url=self.ENDPOINT_TYPES, list_item="eventTypeInfos", target_params=params
        )

    def get_type(self, event_type: str) -> "EventType":
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_TYPES}/{event_type}")
        return EventType(raw_element=response.json(), http_client=self.__http_client)


class Event(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        # Mandatory
        self.event_id: str = raw_element["eventId"]
        self.event_type: str = raw_element["eventType"]
        self.start_time: datetime = int64_to_datetime(int(raw_element["startTime"]))
        # Optional
        self.entity_tags: Optional[List[METag]] = [METag(raw_element=et) for et in raw_element.get("entityTags", [])]
        self.suppress_alert: Optional[bool] = raw_element.get("suppressAlert")
        self.frequent_event: Optional[bool] = raw_element.get("frequentEvent")
        self.suppress_problem: Optional[bool] = raw_element.get("suppressProblem")
        self.under_maintenance: Optional[bool] = raw_element.get("underMaintenance")
        self.entity_id: Optional[EntityStub] = EntityStub(raw_element=raw_element["entityId"]) if raw_element.get("entityId") else None
        self.management_zones: Optional[List[ManagementZone]] = [ManagementZone(raw_element=mz) for mz in raw_element.get("managementZones", [])]
        self.properties: Optional[List[EventProperty]] = [EventProperty(raw_element=p) for p in raw_element.get("properties", [])]
        self.status: Optional[EventStatus] = EventStatus(raw_element.get("status")) if raw_element.get("status") else None
        self.end_time: Optional[datetime] = int64_to_datetime(raw_element.get("endTime"))
        self.title: Optional[str] = raw_element.get("title")
        self.correlation_id: Optional[str] = raw_element.get("correlationId")

    def to_json(self) -> Dict[str, Any]:
        return {
            "eventId": self.event_id,
            "eventType": self.event_type,
            "startTime": datetime_to_int64(self.start_time),
            "endTime": datetime_to_int64(self.end_time),
            "entityTags": [tag.to_json() for tag in self.entity_tags] if self.entity_tags else [],
            "suppressAlert": self.suppress_alert,
            "frequentEvent": self.frequent_event,
            "suppressProblem": self.suppress_problem,
            "underMaintenance": self.under_maintenance,
            "entityId": self.entity_id.to_json() if self.entity_id else None,
            "managementZones": [mz.to_json() for mz in self.management_zones] if self.management_zones else [],
            "properties": [p.to_json() for p in self.properties] if self.properties else [],
            "title": self.title,
            "correlationId": self.correlation_id,
        }


class EventProperty(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.key: Optional[str] = raw_element.get("key")
        self.value: Optional[str] = raw_element.get("value")

    def to_json(self) -> Dict[str, Any]:
        return {"key": self.key, "value": self.value}


class EventType(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: str = raw_element["type"]
        self.display_name: str = raw_element["displayName"]
        self.severity_level: Optional[EventSeverity] = EventSeverity(raw_element["severityLevel"]) if raw_element.get("severityLevel") else None
        self.description: Optional[str] = raw_element.get("description")

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "displayName": self.display_name,
            "severityLevel": str(self.severity_level) if self.severity_level else None,
            "description": self.description,
        }


class EventStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

    def __str__(self) -> str:
        return self.value


class EventSeverity(Enum):
    AVAILABILITY = "AVAILABILITY"
    CUSTOM_ALERT = "CUSTOM_ALERT"
    ERROR = "ERROR"
    INFO = "INFO"
    MONITORING_UNAVAILABLE = "MONITORING_UNAVAILABLE"
    PERFORMANCE = "PERFORMANCE"
    RESOURCE_CONTENTION = "RESOURCE_CONTENTION"

    def __str__(self) -> str:
        return self.value
