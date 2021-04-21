from typing import List, Optional
from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.environment_v2.entity import Entity

class Scope(DynatraceObject):
    @property
    def entities(self):
        return self._entities
    
    def _create_from_raw_data(self, raw_element):
        self._entities = raw_element.get("entities")
        self._matches = raw_element.get("matches")

class Recurrence(DynatraceObject):
    def __init__(self, start_time: str, duration: int, day_of_week: Optional[str] = None, day_of_month: Optional[int] = None):
        self._day_of_week = day_of_week.upper()
        self._day_of_month = day_of_month
        self._start_time = start_time
        self._duration = duration

    @property
    def day_of_week(self) -> str:
        return self._day_of_week

    @property
    def day_of_month(self) -> str:
        return self._day_of_month

    @property
    def start_time(self) -> str:
        return self._start_time

    @property
    def duration(self) -> int:
        return self._duration

    def _create_from_raw_data(self, raw_element):
        self._day_of_week = raw_element.get("dayOfWeek")
        self._day_of_month = raw_element.get("dayOfMonth")
        self._start_time = raw_element.get("startTime")
        self._duration = raw_element.get("durationMinutes")

class Schedule(DynatraceObject):    
    def __init__(self, recurrence_type:str, start: str, end: str, zone_id: str, recurrence: Optional[Recurrence] = None):
        self._recurrence_type = recurrence_type.upper()
        self._recurrence = recurrence
        self._start_time = start
        self._end_time = end
        self._zone_id = zone_id

    @property
    def recurrence_type(self) -> str:
        return self._recurrence_type

    @property
    def recurrence(self) -> str:
        return self._recurrence

    @property
    def start_time(self) -> str:
        return self._start_time

    @property
    def end_time(self) -> str:
        return self._end_time

    @property
    def zone_id(self) -> str:
        return self._zone_id

    @property
    def schedule_snippet(self) -> dict:
        if self._recurrence_type == "DAILY":
            representation = {"recurrenceType": self._recurrence_type, "recurrence": {"startTime": self._recurrence.start_time, "durationMinutes": self._recurrence.duration}, "start": self._start_time, "end": self._end_time, "zoneId": self._zone_id}
        if self._recurrence_type == "WEEKLY":
            representation = {"recurrenceType": self._recurrence_type, "recurrence": {"dayOfWeek": self._recurrence.day_of_week, "startTime": self._recurrence.start_time, "durationMinutes": self._recurrence.duration}, "start": self._start_time, "end": self._end_time, "zoneId": self._zone_id}
        if self._recurrence_type == "MONTHLY":
            representation = {"recurrenceType": self._recurrence_type, "recurrence": {"dayOfMonth": self._recurrence.day_of_month, "startTime": self._recurrence.start_time, "durationMinutes": self._recurrence.duration}, "start": self._start_time, "end": self._end_time, "zoneId": self._zone_id}
        if self._recurrence_type == "ONCE":
            representation = {"recurrenceType": self._recurrence_type, "start": self._start_time, "end": self._end_time, "zoneId": self._zone_id}
        return representation

    def _create_from_raw_data(self, raw_element):
        self._recurrence_type = raw_element.get("recurrenceType")
        self._recurrence = Recurrence(raw_element=raw_element.get("recurrence"))
        self._start_time = raw_element.get("start")
        self._end_time = raw_element.get("end")
        self._zone_id = raw_element.get("zoneId")


class MaintenanceWindowService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList["MaintenanceWindowStub"]:
        """
        Lists all maintenance windows in the environment. No configurable parameters.
        """
        return PaginatedList(MaintenanceWindowStub, self.__http_client, f"/api/config/v1/maintenanceWindows", list_item="values")

    def create_schedule(
        self, recurrence_type: str, start: str, end: str, zone_id: str, recurrence_start_time: Optional[str] = None, recurrence_duration: Optional[int] = None, recurrence_day_of_week: Optional[str] = None, recurrence_day_of_month: Optional[int] = None
    ) -> "Schedule":
        """
        Create a schedule to be used when creating a maintenance window.
        """
        recurrence = Recurrence(recurrence_start_time, recurrence_duration, recurrence_day_of_week, recurrence_day_of_month) if recurrence_type != "ONCE" else None

        return Schedule(recurrence_type, start, end, zone_id, recurrence)

    def create(
        self, name: str, description: str, window_type: str, suppression: str, schedule: Schedule, id: Optional[str] = None, suppress_synthetic: Optional[bool] = False, scope: Optional[Scope] = None, recurrence: Optional[Recurrence] = None, scope_entities: Optional[list] = None
    ) -> "MaintenanceWindowCreated":
        """
        Create a maintenance window with the specified parameters.
        You must first use create_schedule() to create a schedule with optional recurrence.
        """
        body = {"id": id, "name": name, "description": description, "type": window_type, "suppression": suppression, "suppressSyntheticMonitorsExecution": suppress_synthetic, 
                "schedule": schedule.schedule_snippet, "scope": {"entities": scope_entities, "matches": []}}

        response = self.__http_client.make_request("/api/config/v1/maintenanceWindows", method="POST", params=body)
        return MaintenanceWindowCreated(raw_element=response.json())

    def delete(self, zone_id: str) -> Response:
        """
        Delete the maintenance window with the specified id
        """
        return self.__http_client.make_request(f"/api/config/v1/maintenanceWindows/{zone_id}", method="DELETE")

class MaintenanceWindowCreated(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._description = raw_element.get("description")

class MaintenanceWindow(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def type(self) -> str:
        return self._type

    @property
    def suppression(self) -> str:
        return self._suppression

    @property
    def suppress_synthetic(self) -> bool:
        return self._suppress_synthetic

    @property
    def scope(self) -> Scope:
        return self._scope

    @property
    def schedule(self) -> dict:
        return self._schedule

    def _create_from_raw_data(self, raw_element):
        if raw_element is None:
            raw_element = {}
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._description = raw_element.get("description")
        self._type = raw_element.get("type")
        self._suppression = raw_element.get("suppression")
        self._suppress_synthetic = raw_element.get("suppressSyntheticMonitorsExecution")
        self._scope = Scope(raw_element=raw_element.get("scope"))
        self._schedule = Schedule(raw_element=raw_element.get("schedule"))


class MaintenanceWindowStub(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._description = raw_element.get("description")

    def get_full_maintenance_window(self) -> MaintenanceWindow:
        """
        Gets the full maintenance window for this stub
        """
        response = self._http_client.make_request(f"/api/config/v1/maintenanceWindows/{self.id}").json()
        return MaintenanceWindow(self._http_client, None, response)
