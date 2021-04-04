from datetime import datetime
from typing import Optional, List

from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient

EVENT_TYPE_AVAILABILITY_EVENT = "AVAILABILITY_EVENT"
EVENT_TYPE_CUSTOM_ALERT = "CUSTOM_ALERT"
EVENT_TYPE_CUSTOM_ANNOTATION = "CUSTOM_ANNOTATION"
EVENT_TYPE_CUSTOM_CONFIGURATION = "CUSTOM_CONFIGURATION"
EVENT_TYPE_CUSTOM_DEPLOYMENT = "CUSTOM_DEPLOYMENT"
EVENT_TYPE_CUSTOM_INFO = "CUSTOM_INFO"
EVENT_TYPE_ERROR_EVENT = "ERROR_EVENT"
EVENT_TYPE_MARKED_FOR_TERMINATION = "MARKED_FOR_TERMINATION"
EVENT_TYPE_PERFORMANCE_EVENT = "PERFORMANCE_EVENT"
EVENT_TYPE_RESOURCE_CONTENTION = "RESOURCE_CONTENTION"


class EventService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def create_event(
        self,
        event_type: str,
        entity_id: str,
        source: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        timeout_minutes: Optional[int] = None,
        annotation_type: Optional[str] = None,
        annotation_description: Optional[str] = None,
        description: Optional[str] = None,
        title: Optional[str] = None,
        custom_properties: Optional[str] = None,
        allow_davis_merge: Optional[bool] = None,
    ) -> Response:

        attach_rules = PushEventAttachRules(entity_ids=[entity_id], tag_rule=None)
        return EventCreation(
            self.__http_client,
            event_type=event_type,
            attach_rules=attach_rules,
            source=source,
            start=start,
            end=end,
            timeout_minutes=timeout_minutes,
            annotation_type=annotation_type,
            annotation_description=annotation_description,
            description=description,
            title=title,
            custom_properties=custom_properties,
            allow_davis_merge=allow_davis_merge,
        ).post()


class EventCreation(DynatraceObject):
    def __init__(
        self,
        http_client,
        event_type: str,
        attach_rules: "PushEventAttachRules",
        source: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        timeout_minutes: Optional[int] = None,
        annotation_type: Optional[str] = None,
        annotation_description: Optional[str] = None,
        description: Optional[str] = None,
        title: Optional[str] = None,
        custom_properties: Optional[str] = None,
        allow_davis_merge: Optional[bool] = None,
    ):

        raw_element = {
            "eventType": event_type,
            "start": int(start.timestamp()) * 1000 if start else None,
            "end": int(end.timestamp()) * 1000 if start else None,
            "timeoutMinutes": timeout_minutes,
            "source": source,
            "annotationType": annotation_type,
            "annotationDescription": annotation_description,
            "attachRules": attach_rules._raw_element,
            "description": description,
            "title": title,
            "customProperties": custom_properties,
            "allowDavisMerge": allow_davis_merge,
        }

        super().__init__(http_client, None, raw_element)

    def post(self):
        return self._http_client.make_request(f"/api/v1/events", params=self._raw_element, method="POST")


class PushEventAttachRules:
    def __init__(self, entity_ids: Optional[List[str]], tag_rule: Optional[List["TagMatchRule"]]):

        self._raw_element = {
            "entityIds": entity_ids,
            "tagRule": [t._raw_element for t in tag_rule] if tag_rule else None,
        }


class TagMatchRule:
    def __init__(self, me_types: List[str], tags: List[str]):
        self._raw_element = {
            "meTypes": me_types,
            "tags": tags,
        }


"""
type EventStoreResult struct {
	StoredEventIds       []int    `json:"storedEventIds,omitempty"`
	StoredIds            []string `json:"storedIds,omitempty"`
	StoredCorrelationIds []string `json:"storedCorrelationIds,omitempty"`
}
"""
