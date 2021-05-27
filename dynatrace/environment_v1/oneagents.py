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
from typing import List, Optional, Union
from datetime import datetime

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.utils import datetime_to_int64


class ConfiguredMonitoringMode(Enum):
    CLOUD_INFRASTRUCTURE = "CLOUD_INFRASTRUCTURE"
    FULL_STACK = "FULL_STACK"


class UpdateStatus(Enum):
    INCOMPATIBLE = "INCOMPATIBLE"
    OUTDATED = "OUTDATED"
    SCHEDULED = "SCHEDULED"
    SUPPRESSED = "SUPPRESSED"
    UNKNOWN = "UNKNOWN"
    UP2DATE = "UP2DATE"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_PENDING = "UPDATE_PENDING"
    UPDATE_PROBLEM = "UPDATE_PROBLEM"


class MonitoringType(Enum):
    CLOUD_INFRASTRUCTURE = "CLOUD_INFRASTRUCTURE"
    FULL_STACK = "FULL_STACK"
    STANDALONE = "STANDALONE"


class AvailabilityState(Enum):
    MONITORED = "MONITORED"
    UNMONITORED = "UNMONITORED"
    CRASHED = "CRASHED"
    LOST = "LOST"
    PRE_MONITORED = "PRE_MONITORED"
    SHUTDOWN = "SHUTDOWN"
    UNEXPECTED_SHUTDOWN = "UNEXPECTED_SHUTDOWN"
    UNKNOWN = "UNKNOWN"


class AutoUpdate(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class OsType(Enum):
    AIX = "AIX"
    LINUX = "LINUX"
    WINDOWS = "WINDOWS"
    SOLARIS = "SOLARIS"
    ZOS = "ZOS"


class OneAgentOnAHostService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        include_details: Optional[bool] = None,
        start_timestamp: Optional[Union[datetime, int]] = None,
        end_timestamp: Optional[Union[datetime, int]] = None,
        relative_time: Optional[str] = None,
        tag: Optional[List[str]] = None,
        entity: Optional[List[str]] = None,
        mz_id: Optional[str] = None,
        management_zone: Optional[str] = None,
        network_zone_id: Optional[str] = None,
        host_group_id: Optional[str] = None,
        host_group_name: Optional[str] = None,
        os_type: Optional[Union[OsType, str]] = None,
        availability_state: Optional[Union[AvailabilityState, str]] = None,
        monitoring_type: Optional[Union[MonitoringType, str]] = None,
        auto_update: Optional[Union[AutoUpdate, str]] = None,
    ) -> PaginatedList["HostAgentInfo"]:
        """
        Lists OneAgents on a Host. Older API - timestamps are of type integer and therefore require conversion
        """
        params = {
            "includeDetails": include_details,
            "startTimestamp": datetime_to_int64(start_timestamp),
            "endTimestamp": datetime_to_int64(end_timestamp),
            "relativeTime": relative_time,
            "tag": tag,
            "entity": entity,
            "managementZoneId": mz_id,
            "managementZone": management_zone,
            "networkZoneId": network_zone_id,
            "hostGroupId": host_group_id,
            "hostGroupName": host_group_name,
            "osType": OsType(os_type).value if os_type else None,
            "availabilityState": AvailabilityState(availability_state).value if availability_state else None,
            "monitoringType": MonitoringType(monitoring_type).value if monitoring_type else None,
            "autoUpdateSetting": AutoUpdate(auto_update).value if auto_update else None,
        }
        return PaginatedList(HostAgentInfo, self.__http_client, "/api/v1/oneagents", params, list_item="hosts")


# todo - create class objects for ModuleInfo[] and PluginInfo[]
class HostAgentInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.host_info: HostInfo = HostInfo(raw_element=raw_element.get("hostInfo"))
        self.faulty_version: bool = raw_element.get("faultyVersion")
        self.active: bool = raw_element.get("active")
        self.configured_monitoring_mode: ConfiguredMonitoringMode = ConfiguredMonitoringMode(raw_element.get("configuredMonitoringMode"))
        self.monitoring_type: MonitoringType = MonitoringType(raw_element.get("monitoringType"))
        self.auto_update: AutoUpdate = AutoUpdate(raw_element.get("autoUpdateSetting"))
        self.update_status: UpdateStatus = UpdateStatus(raw_element.get("updateStatus"))
        self.available_versions: str = raw_element.get("availableVersions", [])
        self.config_monitoring_enabled: bool = raw_element.get("configuredMonitoringEnabled")
        self.availability_state: AvailabilityState = AvailabilityState(raw_element.get("availabilityState"))
        self.activegate_id: int = raw_element.get("currentActiveGateId")
        self.networkzone_id: str = raw_element.get("currentNetworkZoneId")


# todo - incomplete + firstSeenTimestamp is of type integer, how do we work with that here?
class HostInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.entity_id: str = raw_element.get("entityId")
        self.display_name: str = raw_element.get("displayName")
        self.discovered_name: str = raw_element.get("discoveredName")
        self.consumed_host_units: str = raw_element.get("consumedHostUnits")
        self.os_version: str = raw_element.get("osVersion")
        self.host_group: HostGroup = HostGroup(raw_element=raw_element.get("hostGroup"))
        self.tags: List[TagInfo] = [TagInfo(t) for t in raw_element.get("tags", [])]
        self.os_type: Optional[OsType] = OsType(raw_element.get("osType")) if raw_element.get("osType") else None


class HostGroup(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.me_id: str = raw_element.get("meId")
        self.name: str = raw_element.get("name")


class TagInfo(DynatraceObject):
    # todo - convert context to Enum
    def _create_from_raw_data(self, raw_element):
        self.context: str = raw_element.get("context")
        self.key: str = raw_element.get("key")
        self.value: str = raw_element.get("value")
