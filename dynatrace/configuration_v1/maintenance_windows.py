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

from typing import Optional, Dict, Any, List
from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class Scope(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.entities: List[str] = raw_element.get("entities")
        # TODO - This needs to be List[MonitoredEntityFilter]
        self._matches: Any = raw_element.get("matches")


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


class MaintenanceWindowService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList["MaintenanceWindowStub"]:
        """
        Lists all maintenance windows in the environment. No configurable parameters.
        """
        return PaginatedList(MaintenanceWindowStub, self.__http_client, f"/api/config/v1/maintenanceWindows", list_item="values")

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
        scope_entities: Optional[list] = None,
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
            "scope": {"entities": scope_entities, "matches": []},
        }

        response = self.__http_client.make_request("/api/config/v1/maintenanceWindows", method="POST", params=body).json()
        return MaintenanceWindowCreated(raw_element=response)

    def delete(self, zone_id: str) -> Response:
        """
        Delete the maintenance window with the specified id
        """
        return self.__http_client.make_request(f"/api/config/v1/maintenanceWindows/{zone_id}", method="DELETE")


class MaintenanceWindowCreated(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")


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


class MaintenanceWindowStub(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")

    def get_full_maintenance_window(self) -> MaintenanceWindow:
        """
        Gets the full maintenance window for this stub
        """
        response = self._http_client.make_request(f"/api/config/v1/maintenanceWindows/{self.id}").json()
        return MaintenanceWindow(self._http_client, None, response)
