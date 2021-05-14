from typing import List
from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.configuration_v1.metag import METag
from dynatrace.http_client import HttpClient


class AlertingProfileTagFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.include_mode: str = raw_element.get("includeMode")
        self.ag_filters: List[METag] = [METag(raw_element=tag) for tag in raw_element.get("tagFilters", {})]


class AlertingProfileSeverityRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.severity_level: str = raw_element.get("severityLevel")
        self.tag_filter: AlertingProfileTagFilter = AlertingProfileTagFilter(raw_element=raw_element.get("tagFilter"))
        self.delay_in_minutes: int = raw_element.get("delayInMinutes")


class AlertingPredefinedEventFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.event_type: str = raw_element.get("eventType")
        self.negate: bool = raw_element.get("negate")


class AlertingCustomTextFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.enabled: bool = raw_element.get("enabled")
        self.value: str = raw_element.get("value")
        self.operator: str = raw_element.get("operator")
        self.negate: bool = raw_element.get("negate")
        self.case_insensitive: bool = raw_element.get("caseInsensitive")


class AlertingCustomEventFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.custom_title_filter: AlertingCustomTextFilter = AlertingCustomTextFilter(raw_element=raw_element.get("customTitleFilter"))
        self.custom_description_filter: AlertingCustomTextFilter = AlertingCustomTextFilter(raw_element=raw_element.get("customDescriptionFilter"))


class AlertingEventTypeFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.predefined_event_filter: AlertingPredefinedEventFilter = AlertingPredefinedEventFilter(raw_element=raw_element.get("predefinedEventFilter"))
        self.custom_event_filter: AlertingCustomEventFilter = AlertingCustomEventFilter(raw_element=raw_element.get("customEventFilter"))


class AlertingProfile(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element.get("metadata"))
        self.id: str = raw_element.get("id")
        self.display_name: str = raw_element.get("displayName")
        self.rules: List[AlertingProfileSeverityRule] = [AlertingProfileSeverityRule(raw_element=rule) for rule in raw_element.get("rules", {})]
        self.management_zone_id: str = raw_element.get("mzId")
        self.event_type_filters: List[AlertingEventTypeFilter] = [
            AlertingEventTypeFilter(raw_element=event_filter) for event_filter in raw_element.get("eventTypeFilters", {})
        ]


class AlertingProfileStub(EntityShortRepresentation):
    def get_full_configuration(self):
        """
        Gathers the full details of the alerting profile
        """
        response = self._http_client.make_request(f"/api/config/v1/alertingProfiles/{self.id}").json()
        return AlertingProfile(self._http_client, None, response)


class AlertingProfileService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList[AlertingProfileStub]:
        """
        Lists all alerting profiles in the environmemt. No configurable parameters.
        """
        return PaginatedList(AlertingProfileStub, self.__http_client, f"/api/config/v1/alertingProfiles", list_item="values")

    def delete(self, profile_id: str) -> Response:
        """
        Delete the alerting profile with the specified id.
        """
        return self.__http_client.make_request(f"/api/config/v1/alertingProfiles/{profile_id}", method="DELETE")
