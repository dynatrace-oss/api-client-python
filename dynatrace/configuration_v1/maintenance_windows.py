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

from enum import Enum
from typing import Optional, Dict, Any, List
from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList

from dynatrace.environment_v2.custom_tags import METag
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation


class TagCombination(Enum):
    AND = "AND"
    OR = "OR"
    NONE = None

    def __str__(self) -> str:
        return self.value


class MonitoredEntityFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.type: str = raw_element.get("type")
        self.mz_id: str = raw_element.get("mzId")
        self.tags: Optional[List[METag]] = [METag(raw_element=tag) for tag in raw_element.get("tags", [])]
        self.tag_combination: Optional[TagCombination] = TagCombination(raw_element.get("tagCombination"))

    def to_json(self) -> Dict[str, Any]:
        return {"type": self.type, "mzId": self.mz_id, "tags": [t.to_json() for t in self.tags], "tagCombination": str(self.tag_combination)}


class Scope(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.entities: List[str] = raw_element.get("entities")
        self.matches: Optional[List[MonitoredEntityFilter]] = [MonitoredEntityFilter(raw_element=m) for m in raw_element.get("matches")]

    def to_json(self) -> Dict[str, Any]:
        return {"entities": self.entities, "matches": [m.to_json() for m in self.matches]}


class Recurrence(DynatraceObject):
    @staticmethod
    def create(start_time: str, duration: int, day_of_week: Optional[str] = None, day_of_month: Optional[int] = None):
        raw_element = {"dayOfWeek": day_of_week.upper(), "dayOfMonth": day_of_month, "startTime": start_time, "durationMinutes": duration}
        return Recurrence(raw_element=raw_element)

    def _create_from_raw_data(self, raw_element):
        self.day_of_week: str = raw_element.get("dayOfWeek")
        self.day_of_month: str = raw_element.get("dayOfMonth")
        self.start_time: Optional[str] = raw_element.get("startTime")
        self.duration: Optional[int] = raw_element.get("durationMinutes")


class Schedule(DynatraceObject):
    @staticmethod
    def create(recurrence_type: str, start: str, end: str, zone_id: str, recurrence: Optional[Recurrence] = None):
        raw_element = {"recurrenceType": recurrence_type, "recurrence": recurrence, "start": start, "end": end, "zoneId": zone_id}
        return Schedule(raw_element=raw_element)

    @property
    def schedule_snippet(self) -> Dict[str, Any]:
        representation = {}
        if self.recurrence_type == "DAILY":
            representation = {
                "recurrenceType": self.recurrence_type,
                "recurrence": {"startTime": self.recurrence.start_time, "durationMinutes": self.recurrence.duration},
                "start": self.start_time,
                "end": self.end_time,
                "zoneId": self.zone_id,
            }
        if self.recurrence_type == "WEEKLY":
            representation = {
                "recurrenceType": self.recurrence_type,
                "recurrence": {"dayOfWeek": self.recurrence.day_of_week, "startTime": self.recurrence.start_time, "durationMinutes": self.recurrence.duration},
                "start": self.start_time,
                "end": self.end_time,
                "zoneId": self.zone_id,
            }
        if self.recurrence_type == "MONTHLY":
            representation = {
                "recurrenceType": self.recurrence_type,
                "recurrence": {
                    "dayOfMonth": self.recurrence.day_of_month,
                    "startTime": self.recurrence.start_time,
                    "durationMinutes": self.recurrence.duration,
                },
                "start": self.start_time,
                "end": self.end_time,
                "zoneId": self.zone_id,
            }
        if self.recurrence_type == "ONCE":
            representation = {"recurrenceType": self.recurrence_type, "start": self.start_time, "end": self.end_time, "zoneId": self.zone_id}
        return representation

    def _create_from_raw_data(self, raw_element):
        self.recurrence_type: str = raw_element.get("recurrenceType")
        self.recurrence: Recurrence = Recurrence(raw_element=raw_element.get("recurrence"))
        self.start_time: str = raw_element.get("start")
        self.end_time: str = raw_element.get("end")
        self.zone_id: str = raw_element.get("zoneId")


class MaintenanceWindow(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")
        self.type: str = raw_element.get("type")
        self.suppression: str = raw_element.get("suppression")
        self.suppress_synthetic_monitors_execution: bool = raw_element.get("suppressSyntheticMonitorsExecution")
        self.scope: Scope = Scope(raw_element=raw_element.get("scope"))
        self.schedule: Schedule = Schedule(raw_element=raw_element.get("schedule"))

    def post(self) -> EntityShortRepresentation:
        """Creates the Maintenance Window configuration in Dynatrace (POST).

        :param maintenance_window: the Maintenance Window configuration details

        :returns EntityShortRepresentation: basic details of the created Maintenance Window

        :throws ValueError: if operation cannot be executed due to missing HTTP Client
        """
        if not self._http_client:
            raise ValueError("Object does not have an HTTP Client. Use maintenance_window.post() instead.")
        response = self._http_client.make_request(path=MaintenanceWindowService.ENDPOINT, params=self.to_json(), method="POST")
        self.id = response.json().get("id")

        return EntityShortRepresentation(raw_element=response.json())

    def to_json(self) -> Dict[str, Any]:
        """Get a JSON (dict) representation of this config."""
        mw: Dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "suppression": self.suppression,
            "suppressSyntheticMonitorsExecution": self.suppress_synthetic_monitors_execution,
            "schedule": self.schedule.schedule_snippet,
            "scope": self.scope.to_json(),
        }
        return mw


class MaintenanceWindowService:
    ENDPOINT = "/api/config/v1/maintenanceWindows"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList["MaintenanceWindowStub"]:
        """
        Lists all maintenance windows in the environment. No configurable parameters.
        """
        return PaginatedList(MaintenanceWindowStub, self.__http_client, self.ENDPOINT, list_item="values")

    def get(self, mw_id: str) -> MaintenanceWindow:
        """Gets the full details of the Maintenance Window referenced by ID.

        :param mw_id: ID of the alerting profile

        :returns AlertingProfile: alerting profile details
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{mw_id}")
        return MaintenanceWindow(http_client=self.__http_client, raw_element=response.json())

    def post(self, mw: MaintenanceWindow) -> EntityShortRepresentation:
        """Creates the Maintenance Window configuration in Dynatrace (POST).

        :param maintenace_window: the Maintenance Window configuration details

        :returns EntityShortRepresentation: basic details of the created Maintenance Window
        """
        if not mw._http_client:
            mw._http_client = self.__http_client
        return mw.post()

    def create_schedule(
        self,
        recurrence_type: str,
        start: str,
        end: str,
        zone_id: str,
        recurrence_start_time: Optional[str] = None,
        recurrence_duration: Optional[int] = None,
        recurrence_day_of_week: Optional[str] = None,
        recurrence_day_of_month: Optional[int] = None,
    ) -> "Schedule":
        """
        Create a schedule to be used when creating a maintenance window.
        """
        recurrence = (
            Recurrence.create(recurrence_start_time, recurrence_duration, recurrence_day_of_week, recurrence_day_of_month)
            if recurrence_type != "ONCE"
            else None
        )
        return Schedule.create(recurrence_type, start, end, zone_id, recurrence)

    def create(
        self,
        name: str,
        description: str,
        window_type: str,
        suppression: str,
        schedule: Schedule,
        maintenance_window_id: Optional[str] = None,
        suppress_synthetic: Optional[bool] = False,
        scope: Optional[Scope] = None,
        recurrence: Optional[Recurrence] = None,
    ) -> "MaintenanceWindowCreated":
        # TODO - scope and recurrence are not used here but they should
        """
        Create a maintenance window with the specified parameters.
        You must first use create_schedule() to create a schedule with optional recurrence.
        """
        body = {
            "id": maintenance_window_id,
            "name": name,
            "description": description,
            "type": window_type,
            "suppression": suppression,
            "suppressSyntheticMonitorsExecution": suppress_synthetic,
            "schedule": schedule.schedule_snippet,
            "scope": {"entities": scope.entities, "matches": [s.to_json() for s in scope.matches]},
        }

        response = self.__http_client.make_request(self.ENDPOINT, method="POST", params=body).json()
        return MaintenanceWindowCreated(raw_element=response)

    def delete(self, zone_id: str) -> Response:
        """
        Delete the maintenance window with the specified id
        """
        return self.__http_client.make_request(f"{self.ENDPOINT}/{zone_id}", method="DELETE")


class MaintenanceWindowCreated(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")


class MaintenanceWindowStub(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")

    def get_full_maintenance_window(self) -> MaintenanceWindow:
        """
        Gets the full maintenance window for this stub
        """
        response = self._http_client.make_request(f"{MaintenanceWindowService.ENDPOINT}/{self.id}").json()
        return MaintenanceWindow(self._http_client, None, response)
