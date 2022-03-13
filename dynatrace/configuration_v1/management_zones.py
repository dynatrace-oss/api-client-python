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

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dynatrace import http_client

from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.configuration_v1.dt_enums import ConditionKeyAttribute


class ManagementZoneService:
    ENDPOINT = "/api/config/v1/managementZones"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self, page_size: int = 200) -> PaginatedList["ManagementZoneShortRepresentation"]:
        """
        List all management zones.

        :param page_size: The number of results per result page. Must be between 1 and 500
            Default value : 200
        """
        params = {"pageSize": page_size}
        return PaginatedList(ManagementZoneShortRepresentation, self.__http_client, f"{self.ENDPOINT}", params, list_item="values")

    def get(self, management_zone_id: str) -> "ManagementZone":
        """Gets the description of a management zone referenced by ID.

        :param _id: The ID of the required management zone.

        :returns Event: the requested management zone
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{management_zone_id}")
        return ManagementZone(raw_element=response.json(), http_client=self.__http_client)

    def delete(self, management_zone_id: str):
        """Deletes the specified management zone

        :param networkzone_id: the ID of the management zone
        :return: HTTP response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{management_zone_id}", method="DELETE")


class PropagationType(Enum):
    SERVICE_TO_PROCESS_GROUP_LIKE = "SERVICE_TO_PROCESS_GROUP_LIKE"
    SERVICE_TO_HOST_LIKE = "SERVICE_TO_HOST_LIKE"
    PROCESS_GROUP_TO_HOST = "PROCESS_GROUP_TO_HOST"
    PROCESS_GROUP_TO_SERVICE = "PROCESS_GROUP_TO_SERVICE"
    HOST_TO_PROCESS_GROUP_INSTANCE = "HOST_TO_PROCESS_GROUP_INSTANCE"
    AZURE_TO_PG = "AZURE_TO_PG"
    AZURE_TO_SERVICE = "AZURE_TO_SERVICE"
    NONE = None


class ConditionKeyType(Enum):
    PROCESS_CUSTOM_METADATA_KEY = "PROCESS_CUSTOM_METADATA_KEY"
    HOST_CUSTOM_METADATA_KEY = "HOST_CUSTOM_METADATA_KEY"
    PROCESS_PREDEFINED_METADATA_KEY = "PROCESS_PREDEFINED_METADATA_KEY"
    STRING = "STRING"
    STATIC = "STATIC"
    NONE = None


class ComparisonBasicType(Enum):
    APPLICATION_TYPE = "APPLICATION_TYPE"
    AZURE_COMPUTE_MODE = "AZURE_COMPUTE_MODE"
    AZURE_SKU = "AZURE_SKU"
    BITNESS = "BITNESS"
    CLOUD_TYPE = "CLOUD_TYPE"
    CUSTOM_APPLICATION_TYPE = "CUSTOM_APPLICATION_TYPE"
    DATABASE_TOPOLOGY = "DATABASE_TOPOLOGY"
    DCRUM_DECODER_TYPE = "DCRUM_DECODER_TYPE"
    ENTITY_ID = "ENTITY_ID"
    HYPERVISOR_TYPE = "HYPERVISOR_TYPE"
    INDEXED_NAME = "INDEXED_NAME"
    INDEXED_STRING = "INDEXED_STRING"
    INDEXED_TAG = "INDEXED_TAG"
    INTEGER = "INTEGER"
    IP_ADDRESS = "IP_ADDRESS"
    MOBILE_PLATFORM = "MOBILE_PLATFORM"
    OS_ARCHITECTURE = "OS_ARCHITECTURE"
    OS_TYPE = "OS_TYPE"
    PAAS_TYPE = "PAAS_TYPE"
    SERVICE_TOPOLOGY = "SERVICE_TOPOLOGY"
    SERVICE_TYPE = "SERVICE_TYPE"
    SIMPLE_HOST_TECH = "SIMPLE_HOST_TECH"
    SIMPLE_TECH = "SIMPLE_TECH"
    STRING = "STRING"
    SYNTHETIC_ENGINE_TYPE = "SYNTHETIC_ENGINE_TYPE"
    TAG = "TAG"
    NONE = None


class ManagementZoneRuleType(Enum):
    APPLICATION = "APPLICATION"
    AWS_APPLICATION_LOAD_BALANCER = "AWS_APPLICATION_LOAD_BALANCER"
    AWS_CLASSIC_LOAD_BALANCER = "AWS_CLASSIC_LOAD_BALANCER"
    AWS_NETWORK_LOAD_BALANCER = "AWS_NETWORK_LOAD_BALANCER"
    AWS_RELATIONAL_DATABASE_SERVICE = "AWS_RELATIONAL_DATABASE_SERVICE"
    AZURE = "AZURE"
    CUSTOM_APPLICATION = "CUSTOM_APPLICATION"
    CUSTOM_DEVICE = "CUSTOM_DEVICE"
    DCRUM_APPLICATION = "DCRUM_APPLICATION"
    ESXI_HOST = "ESXI_HOST"
    EXTERNAL_SYNTHETIC_TEST = "EXTERNAL_SYNTHETIC_TEST"
    HOST = "HOST"
    HTTP_CHECK = "HTTP_CHECK"
    MOBILE_APPLICATION = "MOBILE_APPLICATION"
    PROCESS_GROUP = "PROCESS_GROUP"
    SERVICE = "SERVICE"
    SYNTHETIC_TEST = "SYNTHETIC_TEST"
    WEB_APPLICATION = "WEB_APPLICATION"
    WEB_APPLICATION_NAME = "WEB_APPLICATION_NAME"
    NONE = None


class ComparisonBasic(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.operator: str = raw_element.get("operator")
        self.value: dict = raw_element.get("value")
        self.negate: bool = raw_element.get("negate")
        self.type: ComparisonBasicType = ComparisonBasicType(raw_element.get("type"))
        self.case_sensitive: bool = raw_element.get("caseSensitive")


class ConditionKey(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.attribute: ConditionKeyAttribute = ConditionKeyAttribute(raw_element.get("attribute"))
        self.type: ConditionKeyType = ConditionKeyType(raw_element.get("type"))


class EntityRuleEngineCondition(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.key: ConditionKey = ConditionKey(raw_element=raw_element.get("key"))
        self.comparison_info: ComparisonBasic = ComparisonBasic(raw_element=raw_element.get("comparisonInfo"))


class EntitySelectorBasedManagementZoneRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: bool = raw_element.get("enabled")
        self.entity_selector: str = raw_element.get("entitySelector")
        self.value_format: str = raw_element.get("valueFormat")


class ManagementZoneRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: ManagementZoneRuleType = ManagementZoneRuleType(raw_element.get("type"))
        self.enabled: bool = raw_element.get("enabled")
        self.value_format: str = raw_element.get("valueFormat")
        self.propagation_types: List[PropagationType] = [PropagationType(prop_type) for prop_type in (raw_element.get("propagationTypes") or [])]
        self.conditions: List[EntityRuleEngineCondition] = [
            EntityRuleEngineCondition(raw_element=condition) for condition in (raw_element.get("conditions") or [])
        ]


class ManagementZone(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(self._http_client, None, raw_element.get("metadata"))
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")
        self.rules: List[ManagementZoneRule] = [ManagementZoneRule(raw_element=rule) for rule in raw_element.get("rules")]
        self.entity_selector_based_rules: List[EntitySelectorBasedManagementZoneRule] = [
            EntitySelectorBasedManagementZoneRule(raw_element=rule) for rule in (raw_element.get("entitySelectorBasedRules") or [])
        ]


class ManagementZoneShortRepresentation(EntityShortRepresentation):
    def get_full_configuration(self):
        """
        Get the full configuration for this management zone short representation.
        """
        response = self._http_client.make_request(f"{ManagementZoneService.ENDPOINT}_{self.id}").json()
        return ManagementZone(http_client=self._http_client, raw_element=response)
