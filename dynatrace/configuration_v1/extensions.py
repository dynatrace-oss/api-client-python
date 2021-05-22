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

from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class ExtensionService:

    # TODO - Early adopter as of May 12th 2021. Check back for updates
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client
        pass

    def list(self, page_size: int = 200) -> PaginatedList["ExtensionDto"]:
        """
        List all uploaded extensions

        :param page_size: The number of results per result page. Must be between 1 and 500
            Default value : 200
        """
        params = {"pageSize": page_size}
        return PaginatedList(ExtensionDto, self.__http_client, f"/api/config/v1/extensions", params, list_item="extensions")

    def get(self, extension_id: str):
        response = self.__http_client.make_request(f"/api/config/v1/extensions/{extension_id}").json()
        return Extension(raw_element=response)

    def post(self, zip_file_path: str) -> EntityShortRepresentation:

        file = Path(zip_file_path)
        with open(file, "rb") as f:
            response = self.__http_client.make_request("/api/config/v1/extensions", method="POST", files={"file": f})

        return EntityShortRepresentation(raw_element=response.json())

    def validate(self, zip_file_path: str) -> Response:

        file = Path(zip_file_path)
        with open(file, "rb") as f:
            return self.__http_client.make_request("/api/config/v1/extensions/validator", method="POST", files={"file": f})

    def list_instances(self, extension_id: str, page_size: int = 200) -> PaginatedList["ExtensionShortRepresentation"]:
        params = {"pageSize": page_size}
        return PaginatedList(
            ExtensionShortRepresentation,
            self.__http_client,
            f"/api/config/v1/extensions/{extension_id}/instances",
            list_item="configurationsList",
            target_params=params,
        )

    def get_instance(self, extension_id: str, configuration_id: str):
        response = self.__http_client.make_request(f"/api/config/v1/extensions/{extension_id}/instances/{configuration_id}").json()
        return ExtensionConfigurationDto(http_client=self.__http_client, raw_element=response)

    def post_instance(self, extension_configuration: "ExtensionConfigurationDto"):
        return extension_configuration.post()

    def validate_instance(self, extension_configuration: "ExtensionConfigurationDto") -> Response:
        return extension_configuration.validate()

    def get_instance_configuration(self, extension_id: str, configuration_id: str) -> "ExtensionConfigurationDto":
        response = self.__http_client.make_request(f"/api/config/v1/extensions/{extension_id}/instances/{configuration_id}").json()
        return ExtensionConfigurationDto(http_client=self.__http_client, raw_element=response)

    # TODO - Can't implement put_instance because of APM-300262, fixed in 1.219

    def delete_instance_configuration(self, extension_id: str, configuration_id: str) -> Response:
        return self.__http_client.make_request(f"/api/config/v1/extensions/{extension_id}/instances/{configuration_id}", method="DELETE")

    def get_global_configuration(self, extension_id: str) -> "GlobalExtensionConfiguration":
        response = self.__http_client.make_request(f"/api/config/v1/extensions/{extension_id}/global").json()
        return GlobalExtensionConfiguration(raw_element=response)

    def get_binary(self, extension_id: str) -> bytes:
        return self.__http_client.make_request(f"/api/config/v1/extensions/{extension_id}/binary").content

    def list_states(self, extension_id: str) -> PaginatedList["ExtensionState"]:
        return PaginatedList(
            ExtensionState,
            self.__http_client,
            f"/api/config/v1/extensions/{extension_id}/states",
            list_item="states",
        )

    def list_activegate_extension_modules(self) -> PaginatedList[EntityShortRepresentation]:
        return PaginatedList(
            EntityShortRepresentation,
            self.__http_client,
            f"/api/config/v1/extensions/activeGateExtensionModules",
            list_item="values",
        )

    def create_instance(
        self,
        extension_id: str,
        properties: Dict[str, Any] = None,
        enabled: Optional[bool] = True,
        use_global: Optional[bool] = True,
        host_id: Optional[str] = None,
        activegate: Optional[EntityShortRepresentation] = None,
        endpoint_id: Optional[str] = None,
        endpoint_name: Optional[str] = None,
    ) -> "ExtensionConfigurationDto":

        raw_element = {
            "extensionId": extension_id,
            "enabled": enabled,
            "useGlobal": use_global,
            "properties": properties,
            "hostId": host_id,
            "activeGate": activegate._raw_element if activegate else {},
            "endpointId": endpoint_id,
            "endpointName": endpoint_name,
        }

        return ExtensionConfigurationDto(http_client=self.__http_client, raw_element=raw_element)


class ExtensionProperty(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.key: str = raw_element.get("key")
        self.type: str = raw_element.get("type")
        self.default_value: str = raw_element.get("defaultValue")
        self.dropdown_values: List[str] = raw_element.get("dropdownValues")


class ExtensionConfigurationDto(DynatraceObject):
    def post(self):

        return self._http_client.make_request(f"/api/config/v1/extensions/{self.extension_id}/instances", params=self.to_json(), method="POST")

    def validate(self):
        return self._http_client.make_request(f"/api/config/v1/extensions/{self.extension_id}/instances/validator", params=self.to_json(), method="POST")

    def to_json(self) -> Dict[str, Any]:
        return {
            "extensionId": self.extension_id,
            "enabled": self.enabled,
            "useGlobal": self.use_global,
            "properties": self.properties,
            "hostId": self.host_id,
            "activeGate": self.active_gate.to_json(),
            "endpointId": self.endpoint_id,
            "endpointName": self.endpoint_name,
        }

    def _create_from_raw_data(self, raw_element):
        self.extension_id: str = raw_element.get("extensionId")
        self.enabled: bool = raw_element.get("enabled")
        self.use_global: bool = raw_element.get("useGlobal", True)
        self.properties: Dict[str, Any] = raw_element.get("properties")
        self.host_id: str = raw_element.get("hostId")
        self.active_gate: EntityShortRepresentation = EntityShortRepresentation(self._http_client, None, raw_element.get("activeGate"))
        self.endpoint_id: str = raw_element.get("endpointId")
        self.endpoint_name: str = raw_element.get("endpointName")


class ExtensionShortRepresentation(EntityShortRepresentation):
    def get_full_configuration(self, extension_id: str):
        """
        Gets the full extension configuration for this ExtensionShortRepresentation
        """
        response = self._http_client.make_request(f"/api/config/v1/extensions/{extension_id}/instances/{self.id}").json()
        return ExtensionConfigurationDto(self._http_client, raw_element=response)


class Extension(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.type: str = ExtensionType(raw_element.get("type"))
        self.version: str = raw_element.get("version")
        self.metric_group: str = raw_element.get("metricGroup")
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(self._http_client, None, raw_element.get("metadata"))
        self.properties: List[ExtensionProperty] = [ExtensionProperty(self._http_client, None, prop) for prop in raw_element.get("properties")]


class ExtensionType(Enum):
    ACTIVEGATE = "ACTIVEGATE"
    CODEMODULE = "CODEMODULE"
    JMX = "JMX"
    ONEAGENT = "ONEAGENT"
    PMI = "PMI"
    UNKNOWN = "UNKNOWN"


class ExtensionDto(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.type: ExtensionType = ExtensionType(raw_element.get("type"))

    def get_full_extension(self) -> Extension:
        """
        Gets the full extension for this ExtensionDto
        """
        response = self._http_client.make_request(f"/api/config/v1/extensions/{self.id}").json()
        return Extension(self._http_client, None, response)

    @property
    def instances(self, page_size: int = 200) -> PaginatedList["ExtensionShortRepresentation"]:
        """
        Returns the list of instances for this extension
        :param page_size: Page size, default 200
        """
        params = {"pageSize": page_size}
        return PaginatedList(
            ExtensionShortRepresentation,
            self._http_client,
            f"/api/config/v1/extensions/{self.id}/instances",
            list_item="configurationsList",
            target_params=params,
        )

    def delete(self) -> Response:
        """
        Deletes the ZIP file of this extension
        """
        return self._http_client.make_request(f"/api/config/v1/extensions/{self.id}", method="DELETE")


class GlobalExtensionConfiguration(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: bool = raw_element.get("enabled")
        self.extension_id: Optional[str] = raw_element.get("extensionId")
        self.infraOnlyEnabled: Optional[bool] = raw_element.get("infraOnlyEnabled")
        self.properties: Optional[Dict[str, Any]] = raw_element.get("properties")


class ExtensionStateEnum(Enum):
    ERROR_AUTH = "ERROR_AUTH"
    ERROR_COMMUNICATION_FAILURE = "ERROR_COMMUNICATION_FAILURE"
    ERROR_CONFIG = "ERROR_CONFIG"
    ERROR_TIMEOUT = "ERROR_TIMEOUT"
    ERROR_UNKNOWN = "ERROR_UNKNOWN"
    INCOMPATIBLE = "INCOMPATIBLE"
    LIMIT_REACHED = "LIMIT_REACHED"
    NOTHING_TO_REPORT = "NOTHING_TO_REPORT"
    OK = "OK"
    STATE_TYPE_UNKNOWN = "STATE_TYPE_UNKNOWN"
    UNINITIALIZED = "UNINITIALIZED"
    UNSUPPORTED = "UNSUPPORTED"
    WAITING_FOR_STATE = "WAITING_FOR_STATE"


class ExtensionState(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.extension_id: Optional[str] = raw_element.get("extensionId")
        self.version: Optional[str] = raw_element.get("version")
        self.endpoint_id: Optional[str] = raw_element.get("endpointId")
        self.state: Optional[ExtensionStateEnum] = ExtensionStateEnum(raw_element.get("state"))
        self.state_description: Optional[str] = raw_element.get("stateDescription")
        self.host_id: Optional[str] = raw_element.get("hostId")
        self.process_id: Optional[str] = raw_element.get("processId")
        self.timestamp: Optional[datetime] = datetime.utcfromtimestamp(raw_element.get("timestamp") / 1000)
