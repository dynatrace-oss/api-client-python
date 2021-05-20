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
from typing import Optional, Dict, Any, List, Union
from enum import Enum

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import HeaderPaginatedList


class RelativeTime(Enum):
    MIN = "min"
    FIVE_MINS = "5mins"
    TEN_MINS = "10mins"
    FIFTEEN_MINS = "15mins"
    THIRTY_MINS = "30mins"
    HOUR = "hour"
    TWO_HOURS = "2hours"
    SIX_HOURS = "6hours"
    DAY = "day"
    THREE_DAYS = "3days"


class OSArchitecture(Enum):
    ARM = "ARM"
    IA_SIXTY_FOUR = "IA64"
    PARISC = "PARISC"
    PPC = "PPC"
    PPCLE = "PPCLE"
    SYSTEM_THIRTY_NINTEY = "S390"
    SPARC = "SPARC"
    X_EIGHTY_SIX = "X86"
    ZOS = "ZOS"


class MonitoringMode(Enum):
    FULL_STACK = "FULL_STACK"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    OFF = "OFF"
    NONE = None


class TagInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.context: str = raw_element.get("context")
        self.key: str = raw_element.get("key")
        self.value: str = raw_element.get("value")


class AgentVersion(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.major: int = raw_element.get("major")
        self.minor: int = raw_element.get("minor")
        self.revision: int = raw_element.get("revision")
        self.timestamp: str = raw_element.get("timestamp")
        self.source_revision: str = raw_element.get("sourceRevision")


class HostGroup(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.me_id: str = raw_element.get("meId")
        self.name: str = raw_element.get("name")


class Host(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.entity_id: str = raw_element.get("entityId")
        self.display_name: str = raw_element.get("displayName")
        self.customized_name: str = raw_element.get("customizedName")
        self.discovered_name: str = raw_element.get("discoveredName")
        self.first_seen_timestamp: int = raw_element.get("firstSeenTimestamp")
        self.last_seen_timestamp: int = raw_element.get("lastSeenTimestamp")
        self.tags: List[TagInfo] = [TagInfo(raw_element=tag) for tag in raw_element.get("tags")]
        self.os_type: str = raw_element.get("osType")
        self.consumed_host_units: float = raw_element.get("consumedHostUnits")
        self.agent_version: AgentVersion = AgentVersion(raw_element=raw_element.get("agentVersion"))
        self.monitoring_mode: Union[MonitoringMode, None] = MonitoringMode(raw_element.get("monitoringMode"))
        self.network_zone_id: str = raw_element.get("networkZoneId")
        self.host_group: HostGroup = HostGroup(raw_element=raw_element.get("hostGroup"))
        self.os_architecture: OSArchitecture = OSArchitecture(raw_element.get("osArchitecture"))
        self.cpu_cores: int = raw_element.get("cpuCores")
        self.os_version: str = raw_element.get("osVersion")


class SmartScapeHostsService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        relative_time: Optional[Union[RelativeTime, str]] = RelativeTime.THREE_DAYS,
        page_size: int = 200,
        management_zone: Optional[int] = None,
        host_group_name: Optional[str] = None,
    ) -> HeaderPaginatedList[Host]:
        """
        List all monitored hosts

        :param management_zone: Filter hosts by a management zone ID
            Default value : None
        :param host_group_name: Filter hosts by a host group name
            Default value : None
        :param relative_time: Relative time ranger to check for (72 hours if not set)
            Default value : RelativeTime.THREE_DAYS
        """
        params = {
            "pageSize": page_size,
            "relativeTime": RelativeTime(relative_time).value,
            "managementZone": management_zone if management_zone else None,
            "hostGroupName": host_group_name if host_group_name else None,
        }
        return HeaderPaginatedList(Host, self.__http_client, f"/api/v1/entity/infrastructure/hosts", params)
