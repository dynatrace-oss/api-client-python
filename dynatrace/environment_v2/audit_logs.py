from datetime import datetime
from enum import Enum
from typing import Optional, Union, Dict, Any, List

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.utils import timestamp_to_string


class AuditLogsService:

    # TODO - Early adopter as of May 14th 2021, check back later for changes
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        log_filter: Optional[str] = None,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None,
        sort: Optional[str] = None,
    ) -> PaginatedList["AuditLogEntry"]:
        params = {"filter": log_filter, "from": timestamp_to_string(time_from), "to": timestamp_to_string(time_to), "sort": sort}
        return PaginatedList(
            target_class=AuditLogEntry, http_client=self.__http_client, target_url="/api/v2/auditlogs", target_params=params, list_item="auditLogs"
        )

    def get(self, log_id: str) -> "AuditLogEntry":
        response = self.__http_client.make_request(f"/api/v2/auditlogs/{log_id}").json()
        return AuditLogEntry(raw_element=response)


class EventType(Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    GENERAL = "GENERAL"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    READ = "READ"
    REVOKE = "REVOKE"
    UPDATE = "UPDATE"


class Category(Enum):
    CONFIG = "CONFIG"
    DEBUG_UI = "DEBUG_UI"
    TOKEN = "TOKEN"
    WEB_UI = "WEB_UI"


class UserType(Enum):
    PUBLIC_TOKEN_IDENTIFIER = "PUBLIC_TOKEN_IDENTIFIER"
    REQUEST_ID = "REQUEST_ID"
    SERVICE_NAME = "SERVICE_NAME"
    TOKEN_HASH = "TOKEN_HASH"
    USER_NAME = "USER_NAME"


class AuditLogEntry(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.category: Category = Category(raw_element.get("category"))
        self.environment_id: str = raw_element.get("environmentId")
        self.event_type: EventType = EventType(raw_element.get("eventType"))
        self.log_id: str = raw_element.get("logId")
        self.success: bool = raw_element.get("success")
        self.timestamp: datetime = datetime.utcfromtimestamp(raw_element.get("timestamp") / 1000)
        self.user: str = raw_element.get("user")
        self.user_type: UserType = UserType(raw_element.get("userType"))

        self.entity_id: Optional[str] = raw_element.get("entityId")
        self.user_origin: Optional[str] = raw_element.get("userOrigin")
        self.message: Optional[str] = raw_element.get("message")
        self.patch: Optional[List[Dict[str, Any]]] = raw_element.get("patch")
