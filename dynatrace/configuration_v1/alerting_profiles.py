from typing import List, Optional
from requests import Response

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.entity import EntityShortRepresentation
from dynatrace.configuration_v1.metag import METag
from dynatrace.http_client import HttpClient

class AlertingProfileMetadata(DynatraceObject):
    @property
    def configuration_versions(self) -> List[int]:
        return self._configuration_versions

    @property
    def current_configuration_versions(self) -> List[int]:
        return self._current_configuration_versions

    @property
    def cluster_version(self) -> str:
        return self._cluster_version

    def _create_from_raw_data(self, raw_element):
        self._configuration_versions = raw_element.get("configurationVersions")
        self._current_configuration_versions = raw_element.get("currentConfigurationVersions")
        self._cluster_version = raw_element.get("clusterVersion")

class AlertingProfileTagFilter(DynatraceObject):
    @property
    def include_mode(self) -> str:
        return self._include_mode

    @property
    def tag_filters(self) -> List[METag]:
        return self._tag_filters

    def _create_from_raw_data(self, raw_element):
        self._include_mode = raw_element.get("includeMode")
        self._tag_filters = [METag(raw_element=tag) for tag in raw_element.get("tagFilters", {})]

class AlertingProfileSeverityRule(DynatraceObject):
    @property
    def severity_level(self) -> str:
        return self._severity_level

    @property
    def tag_filter(self) -> AlertingProfileTagFilter:
        return self._tag_filter

    def _create_from_raw_data(self, raw_element):
        self._severity_level = raw_element.get("severityLevel")
        self._tag_filter = AlertingProfileTagFilter(raw_element=raw_element.get("tagFilter"))
        self._delay_in_minutes = raw_element.get("delayInMinutes")

class AlertingPredefinedEventFilter(DynatraceObject):
    @property
    def event_type(self) -> str:
        return self._event_type

    @property
    def negate(self) -> bool:
        return self._negate

    def _create_from_raw_data(self, raw_element):
        self._event_type = raw_element.get("eventType")
        self._negate = raw_element.get("negate")

class AlertingCustomTextFilter(DynatraceObject):
    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def value(self) -> str:
        return self._value

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def negate(self) -> bool:
        return self._negate

    @property
    def case_insensitive(self) -> bool:
        return self._case_insensitive

    def _create_from_raw_data(self, raw_element):
        self._enabled = raw_element.get("enabled")
        self._value = raw_element.get("value")
        self._operator = raw_element.get("operator")
        self._negate = raw_element.get("negate")
        self._case_insensitive = raw_element.get("caseInsensitive")

class AlertingCustomEventFilter(DynatraceObject):
    @property
    def custom_title_filter(self) -> AlertingCustomTextFilter:
        return self._custom_title_filter

    @property
    def custom_description_filter(self) -> AlertingCustomTextFilter:
        return self._custom_description_filter

    def _create_from_raw_data(self, raw_element):
        self._custom_title_filter = AlertingCustomTextFilter(raw_element=raw_element.get("customTitleFilter"))
        self._custom_description_filter = AlertingCustomTextFilter(raw_element=raw_element.get("customDescriptionFilter"))

class AlertingEventTypeFilter(DynatraceObject):
    @property
    def predefined_event_filter(self) -> AlertingPredefinedEventFilter:
        return self._predefined_event_filter

    @property
    def custom_event_filter(self) -> AlertingCustomEventFilter:
        return self._custom_event_filter

    def _create_from_raw_data(self, raw_element):
        self._predefined_event_filter = AlertingPredefinedEventFilter(raw_element=raw_element.get("predefinedEventFilter"))
        self._custom_event_filter = AlertingCustomEventFilter(raw_element=raw_element.get("customEventFilter"))

class AlertingProfile(DynatraceObject):
    @property
    def metadata(self) -> AlertingProfileMetadata:
        return self._metadata

    @property
    def id(self) -> str:
        return self._id

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def rules(self) -> List[AlertingProfileSeverityRule]:
        return self._rules

    @property
    def management_zone(self) -> str:
        return self._management_zone_id

    @property
    def event_type_filters(self) -> List[AlertingEventTypeFilter]:
        return self._event_type_filters

    def _create_from_raw_data(self, raw_element):
        self._metadata = raw_element.get("metadata")
        self._id = raw_element.get("id")
        self._display_name = raw_element.get("displayName")
        self._rules = [AlertingProfileSeverityRule(raw_element=rule) for rule in raw_element.get("rules", {})]
        self._management_zone_id = raw_element.get("mzId")
        self._event_type_filters = [AlertingEventTypeFilter(raw_element=event_filter) for event_filter in raw_element.get("eventTypeFilters", {})]

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
