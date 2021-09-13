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
from typing import List, Optional, Dict, Any
from requests import Response

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.configuration_v1.schemas import ConfigurationMetadata, StringComparisonOperator
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.environment_v2.custom_tags import METag


class AlertingProfileTagFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.include_mode: TagFilterIncludeMode = TagFilterIncludeMode(raw_element["includeMode"])
        self.tag_filters: Optional[List[METag]] = [METag(raw_element=tag) for tag in raw_element.get("tagFilters", [])]

    def to_json(self) -> Dict[str, Any]:
        details: Dict[str, Any] = {"includeMode": str(self.include_mode)}
        if self.tag_filters:
            details["tagFilters"] = [tf.to_json() for tf in self.tag_filters]
        return details


class AlertingProfileSeverityRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.severity_level: SeverityLevel = SeverityLevel(raw_element["severityLevel"])
        self.tag_filter: AlertingProfileTagFilter = AlertingProfileTagFilter(raw_element=raw_element["tagFilter"])
        self.delay_in_minutes: int = raw_element["delayInMinutes"]

    def to_json(self) -> Dict[str, Any]:
        return {"severityLevel": str(self.severity_level), "tagFilter": self.tag_filter.to_json(), "delayInMinutes": self.delay_in_minutes}


class AlertingPredefinedEventFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.event_type: AlertingPredefinedEvent = AlertingPredefinedEvent(raw_element["eventType"])
        self.negate: bool = raw_element["negate"]

    def to_json(self) -> Dict[str, Any]:
        return {"eventType": str(self.event_type), "negate": self.negate}


class AlertingCustomTextFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.enabled: bool = raw_element["enabled"]
        self.value: str = raw_element["value"]
        self.operator: StringComparisonOperator = StringComparisonOperator(raw_element["operator"])
        self.negate: bool = raw_element["negate"]
        self.case_insensitive: bool = raw_element["caseInsensitive"]

    def to_json(self) -> Dict[str, Any]:
        return {"enabled": self.enabled, "value": self.value, "operator": str(self.operator), "negate": self.negate, "caseInsensitive": self.case_insensitive}


class AlertingCustomEventFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.custom_title_filter: Optional[AlertingCustomTextFilter] = (
            AlertingCustomTextFilter(raw_element=raw_element.get("customTitleFilter")) if "customTitleFilter" in raw_element.keys() else None
        )
        self.custom_description_filter: Optional[AlertingCustomTextFilter] = (
            AlertingCustomTextFilter(raw_element=raw_element.get("customDescriptionFilter")) if "customDescriptionFilter" in raw_element.keys() else None
        )

    def to_json(self) -> Dict[str, Any]:
        details = {}
        if self.custom_title_filter:
            details["customTitleFilter"] = self.custom_title_filter.to_json()
        if self.custom_description_filter:
            details["customDescriptionFilter"] = self.custom_description_filter.to_json()
        return details


class AlertingEventTypeFilter(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.predefined_event_filter: Optional[AlertingPredefinedEventFilter] = (
            AlertingPredefinedEventFilter(raw_element=raw_element.get("predefinedEventFilter")) if "predefinedEventFilter" in raw_element.keys() else None
        )
        self.custom_event_filter: Optional[AlertingCustomEventFilter] = (
            AlertingCustomEventFilter(raw_element=raw_element.get("customEventFilter")) if "customEventFilter" in raw_element.keys() else None
        )

    def to_json(self) -> Dict[str, Any]:
        details = {}
        if self.predefined_event_filter:
            details["predefinedEventFilter"] = self.predefined_event_filter.to_json()
        if self.custom_event_filter:
            details["customEventFilter"] = self.custom_event_filter.to_json()
        return details


class AlertingProfile(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: Optional[ConfigurationMetadata] = ConfigurationMetadata(raw_element=raw_element.get("metadata"))
        self.id: Optional[str] = raw_element.get("id")
        self.display_name: str = raw_element["displayName"]
        self.rules: Optional[List[AlertingProfileSeverityRule]] = [AlertingProfileSeverityRule(raw_element=rule) for rule in raw_element.get("rules", [])]
        self.management_zone_id: Optional[str] = raw_element.get("mzId")
        self.event_type_filters: Optional[List[AlertingEventTypeFilter]] = [
            AlertingEventTypeFilter(raw_element=event_filter) for event_filter in raw_element.get("eventTypeFilters", [])
        ]

    def post(self) -> EntityShortRepresentation:
        """Creates the Alerting Profile configuration in Dynatrace (POST).

        :param alerting_profile: the Alerting Profile configuration details

        :returns EntityShortRepresentation: basic details of the created Alerting Profile

        :throws ValueError: if operation cannot be executed due to missing HTTP Client
        """
        if not self._http_client:
            raise ValueError("Object does not have an HTTP Client. Use alerting_profiles.post() instead.")
        response = self._http_client.make_request(path=AlertingProfileService.ENDPOINT, params=self.to_json(), method="POST")
        self.id = response.json().get("id")

        return EntityShortRepresentation(raw_element=response.json())

    def put(self) -> Response:
        """Updates the Alerting Profile configuration in Dynatrace (PUT).
        If the ID does not exist in Dynatrace, a new Alerting Profile will be created with the given ID.

        :param alerting_profile: the Alerting Profile configuration details

        :returns Response: HTTP Response to the request. Will contain basic details in JSON body if config is created.

        :throws ValueError: if operation cannot be executed due to missing HTTP Client
        """
        if not self._http_client:
            raise ValueError("Object does not have an HTTP Client. Use alerting_profiles.put() instead.")
        response = self._http_client.make_request(path=f"{AlertingProfileService.ENDPOINT}/{self.id}", params=self.to_json(), method="PUT")
        if response.status_code == 201:
            self.id = response.json().get("id")

        return response

    def to_json(self) -> Dict[str, Any]:
        """Get a JSON (dict) representation of this config."""
        details: Dict[str, Any] = {"displayName": self.display_name}
        if self.rules:
            details["rules"] = [r.to_json() for r in self.rules]
        if self.management_zone_id:
            details["mzId"] = self.management_zone_id
        if self.event_type_filters:
            details["eventTypeFilters"] = [etf.to_json() for etf in self.event_type_filters]
        return details


class AlertingProfileStub(EntityShortRepresentation):
    def get_full_configuration(self):
        """
        Gathers the full details of the alerting profile
        """
        if not self._http_client:
            raise ValueError("Object does not have an HTTP Client implemented.")
        response = self._http_client.make_request(f"{AlertingProfileService.ENDPOINT}/{self.id}").json()
        return AlertingProfile(self._http_client, None, response)


class AlertingProfileService:
    ENDPOINT = "/api/config/v1/alertingProfiles"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList[AlertingProfileStub]:
        """
        Lists all alerting profiles in the environmemt. No configurable parameters.
        """
        return PaginatedList(AlertingProfileStub, self.__http_client, f"{self.ENDPOINT}", list_item="values")

    def get(self, profile_id: str) -> AlertingProfile:
        """Gets the full details of the Alerting Profile referenced by ID.

        :param profile_id: ID of the alerting profile

        :returns AlertingProfile: alerting profile details
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{profile_id}")
        return AlertingProfile(http_client=self.__http_client, raw_element=response.json())

    def delete(self, profile_id: str) -> Response:
        """
        Delete the alerting profile with the specified id.
        """
        return self.__http_client.make_request(f"{self.ENDPOINT}/{profile_id}", method="DELETE")

    def post(self, alerting_profile: AlertingProfile) -> EntityShortRepresentation:
        """Creates the Alerting Profile configuration in Dynatrace (POST).

        :param alerting_profile: the Alerting Profile configuration details

        :returns EntityShortRepresentation: basic details of the created Alerting Profile
        """
        if not alerting_profile._http_client:
            alerting_profile._http_client = self.__http_client
        return alerting_profile.post()

    def put(self, alerting_profile: AlertingProfile) -> Response:
        """Updates the Alerting Profile configuration in Dynatrace (PUT).
        If the ID does not exist in Dynatrace, a new Alerting Profile will be created with the given ID.

        :param alerting_profile: the Alerting Profile configuration details

        :returns Response: HTTP Response to the request. Will contain basic details in JSON body if config is created.
        """
        if not alerting_profile._http_client:
            alerting_profile._http_client = self.__http_client
        return alerting_profile.put()


class TagFilterIncludeMode(Enum):
    INCLUDE_ALL = "INCLUDE_ALL"
    INCLUDE_ANY = "INCLUDE_ANY"
    NONE = "NONE"

    def __str__(self) -> str:
        return self.value


class AlertingPredefinedEvent(Enum):
    APPLICATION_ERROR_RATE_INCREASED = "APPLICATION_ERROR_RATE_INCREASED"
    APPLICATION_SLOWDOWN = "APPLICATION_SLOWDOWN"
    APPLICATION_UNEXPECTED_HIGH_LOAD = "APPLICATION_UNEXPECTED_HIGH_LOAD"
    APPLICATION_UNEXPECTED_LOW_LOAD = "APPLICATION_UNEXPECTED_LOW_LOAD"
    AWS_LAMBDA_HIGH_ERROR_RATE = "AWS_LAMBDA_HIGH_ERROR_RATE"
    CUSTOM_APPLICATION_ERROR_RATE_INCREASED = "CUSTOM_APPLICATION_ERROR_RATE_INCREASED"
    CUSTOM_APPLICATION_SLOWDOWN = "CUSTOM_APPLICATION_SLOWDOWN"
    CUSTOM_APPLICATION_UNEXPECTED_HIGH_LOAD = "CUSTOM_APPLICATION_UNEXPECTED_HIGH_LOAD"
    CUSTOM_APPLICATION_UNEXPECTED_LOW_LOAD = "CUSTOM_APPLICATION_UNEXPECTED_LOW_LOAD"
    CUSTOM_APP_CRASH_RATE_INCREASED = "CUSTOM_APP_CRASH_RATE_INCREASED"
    DATABASE_CONNECTION_FAILURE = "DATABASE_CONNECTION_FAILURE"
    DATA_CENTER_SERVICE_PERFORMANCE_DEGRADATION = "DATA_CENTER_SERVICE_PERFORMANCE_DEGRADATION"
    DATA_CENTER_SERVICE_UNAVAILABLE = "DATA_CENTER_SERVICE_UNAVAILABLE"
    EBS_VOLUME_HIGH_LATENCY = "EBS_VOLUME_HIGH_LATENCY"
    EC2_HIGH_CPU = "EC2_HIGH_CPU"
    ELB_HIGH_BACKEND_ERROR_RATE = "ELB_HIGH_BACKEND_ERROR_RATE"
    ENTERPRICE_APPLICATION_PERFORMANCE_DEGRADATION = "ENTERPRICE_APPLICATION_PERFORMANCE_DEGRADATION"
    ENTERPRISE_APPLICATION_UNAVAILABLE = "ENTERPRISE_APPLICATION_UNAVAILABLE"
    ESXI_GUEST_ACTIVE_SWAP_WAIT = "ESXI_GUEST_ACTIVE_SWAP_WAIT"
    ESXI_GUEST_CPU_LIMIT_REACHED = "ESXI_GUEST_CPU_LIMIT_REACHED"
    ESXI_HOST_CPU_SATURATION = "ESXI_HOST_CPU_SATURATION"
    ESXI_HOST_DATASTORE_LOW_DISK_SPACE = "ESXI_HOST_DATASTORE_LOW_DISK_SPACE"
    ESXI_HOST_DISK_QUEUE_SLOW = "ESXI_HOST_DISK_QUEUE_SLOW"
    ESXI_HOST_DISK_SLOW = "ESXI_HOST_DISK_SLOW"
    ESXI_HOST_MEMORY_SATURATION = "ESXI_HOST_MEMORY_SATURATION"
    ESXI_HOST_NETWORK_PROBLEMS = "ESXI_HOST_NETWORK_PROBLEMS"
    ESXI_HOST_OVERLOADED_STORAGE = "ESXI_HOST_OVERLOADED_STORAGE"
    ESXI_VM_IMPACT_HOST_CPU_SATURATION = "ESXI_VM_IMPACT_HOST_CPU_SATURATION"
    ESXI_VM_IMPACT_HOST_MEMORY_SATURATION = "ESXI_VM_IMPACT_HOST_MEMORY_SATURATION"
    EXTERNAL_SYNTHETIC_TEST_OUTAGE = "EXTERNAL_SYNTHETIC_TEST_OUTAGE"
    EXTERNAL_SYNTHETIC_TEST_SLOWDOWN = "EXTERNAL_SYNTHETIC_TEST_SLOWDOWN"
    HOST_OF_SERVICE_UNAVAILABLE = "HOST_OF_SERVICE_UNAVAILABLE"
    HTTP_CHECK_GLOBAL_OUTAGE = "HTTP_CHECK_GLOBAL_OUTAGE"
    HTTP_CHECK_LOCAL_OUTAGE = "HTTP_CHECK_LOCAL_OUTAGE"
    HTTP_CHECK_TEST_LOCATION_SLOWDOWN = "HTTP_CHECK_TEST_LOCATION_SLOWDOWN"
    MOBILE_APPLICATION_ERROR_RATE_INCREASED = "MOBILE_APPLICATION_ERROR_RATE_INCREASED"
    MOBILE_APPLICATION_SLOWDOWN = "MOBILE_APPLICATION_SLOWDOWN"
    MOBILE_APPLICATION_UNEXPECTED_HIGH_LOAD = "MOBILE_APPLICATION_UNEXPECTED_HIGH_LOAD"
    MOBILE_APPLICATION_UNEXPECTED_LOW_LOAD = "MOBILE_APPLICATION_UNEXPECTED_LOW_LOAD"
    MOBILE_APP_CRASH_RATE_INCREASED = "MOBILE_APP_CRASH_RATE_INCREASED"
    MONITORING_UNAVAILABLE = "MONITORING_UNAVAILABLE"
    OSI_DISK_LOW_INODES = "OSI_DISK_LOW_INODES"
    OSI_GRACEFULLY_SHUTDOWN = "OSI_GRACEFULLY_SHUTDOWN"
    OSI_HIGH_CPU = "OSI_HIGH_CPU"
    OSI_HIGH_MEMORY = "OSI_HIGH_MEMORY"
    OSI_LOW_DISK_SPACE = "OSI_LOW_DISK_SPACE"
    OSI_NIC_DROPPED_PACKETS_HIGH = "OSI_NIC_DROPPED_PACKETS_HIGH"
    OSI_NIC_ERRORS_HIGH = "OSI_NIC_ERRORS_HIGH"
    OSI_NIC_UTILIZATION_HIGH = "OSI_NIC_UTILIZATION_HIGH"
    OSI_SLOW_DISK = "OSI_SLOW_DISK"
    OSI_UNEXPECTEDLY_UNAVAILABLE = "OSI_UNEXPECTEDLY_UNAVAILABLE"
    PGI_OF_SERVICE_UNAVAILABLE = "PGI_OF_SERVICE_UNAVAILABLE"
    PGI_UNAVAILABLE = "PGI_UNAVAILABLE"
    PG_LOW_INSTANCE_COUNT = "PG_LOW_INSTANCE_COUNT"
    PROCESS_CRASHED = "PROCESS_CRASHED"
    PROCESS_HIGH_GC_ACTIVITY = "PROCESS_HIGH_GC_ACTIVITY"
    PROCESS_MEMORY_RESOURCE_EXHAUSTED = "PROCESS_MEMORY_RESOURCE_EXHAUSTED"
    PROCESS_NA_HIGH_CONN_FAIL_RATE = "PROCESS_NA_HIGH_CONN_FAIL_RATE"
    PROCESS_NA_HIGH_LOSS_RATE = "PROCESS_NA_HIGH_LOSS_RATE"
    PROCESS_THREADS_RESOURCE_EXHAUSTED = "PROCESS_THREADS_RESOURCE_EXHAUSTED"
    RDS_HIGH_CPU = "RDS_HIGH_CPU"
    RDS_HIGH_LATENCY = "RDS_HIGH_LATENCY"
    RDS_LOW_MEMORY = "RDS_LOW_MEMORY"
    RDS_LOW_STORAGE_SPACE = "RDS_LOW_STORAGE_SPACE"
    RDS_OF_SERVICE_UNAVAILABLE = "RDS_OF_SERVICE_UNAVAILABLE"
    RDS_RESTART_SEQUENCE = "RDS_RESTART_SEQUENCE"
    SERVICE_ERROR_RATE_INCREASED = "SERVICE_ERROR_RATE_INCREASED"
    SERVICE_SLOWDOWN = "SERVICE_SLOWDOWN"
    SERVICE_UNEXPECTED_HIGH_LOAD = "SERVICE_UNEXPECTED_HIGH_LOAD"
    SERVICE_UNEXPECTED_LOW_LOAD = "SERVICE_UNEXPECTED_LOW_LOAD"
    SYNTHETIC_GLOBAL_OUTAGE = "SYNTHETIC_GLOBAL_OUTAGE"
    SYNTHETIC_LOCAL_OUTAGE = "SYNTHETIC_LOCAL_OUTAGE"
    SYNTHETIC_NODE_OUTAGE = "SYNTHETIC_NODE_OUTAGE"
    SYNTHETIC_PRIVATE_LOCATION_OUTAGE = "SYNTHETIC_PRIVATE_LOCATION_OUTAGE"
    SYNTHETIC_TEST_LOCATION_SLOWDOWN = "SYNTHETIC_TEST_LOCATION_SLOWDOWN"

    def __str__(self) -> str:
        return self.value


class SeverityLevel(Enum):
    AVAILABILITY = "AVAILABILITY"
    CUSTOM_ALERT = "CUSTOM_ALERT"
    ERROR = "ERROR"
    MONITORING_UNAVAILABLE = "MONITORING_UNAVAILABLE"
    PERFORMANCE = "PERFORMANCE"
    RESOURCE_CONTENTION = "RESOURCE_CONTENTION"

    def __str__(self) -> str:
        return self.value
