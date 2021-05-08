from typing import List, Dict, Any, Optional

from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class ExtensionService:
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
        return Extension(self.__http_client, None, response)

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
        return ExtensionConfigurationDto(self.__http_client, None, response)

    def post_instance(self, extension_configuration: "ExtensionConfigurationDto"):
        return extension_configuration.post()

    def create_instance(
        self,
        extension_id: str,
        properties: Dict[str, Any] = None,
        enabled: Optional[bool] = True,
        use_global: Optional[bool] = True,
        host_id: Optional[str] = None,
        active_gate: Optional[EntityShortRepresentation] = None,
        endpoint_id: Optional[str] = None,
        endpoint_name: Optional[str] = None,
    ) -> "ExtensionConfigurationDto":

        raw_element = {
            "extensionId": extension_id,
            "enabled": enabled,
            "useGlobal": use_global,
            "properties": properties,
            "hostId": host_id,
            "activeGate": active_gate._raw_element if active_gate else {},
            "endpointId": endpoint_id,
            "endpointName": endpoint_name,
        }

        return ExtensionConfigurationDto(self.__http_client, None, raw_element)


class ExtensionProperty(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.key: str = raw_element.get("key")
        self.type: str = raw_element.get("type")
        self.default_value: str = raw_element.get("defaultValue")
        self.dropdown_values: List[str] = raw_element.get("dropdownValues")


class ExtensionConfigurationDto(DynatraceObject):
    def post(self):
        return self._http_client.make_request(f"/api/config/v1/extensions/{self.extension_id}/instances", params=self._raw_element, method="POST")

    def _create_from_raw_data(self, raw_element):
        self.extension_id: str = raw_element.get("extensionId")
        self.enabled: bool = raw_element.get("enabled")
        self.use_global: bool = raw_element.get("useGlobal")
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
        self.type: str = raw_element.get("type")
        self.version: str = raw_element.get("version")
        self.metric_group: str = raw_element.get("metricGroup")
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(self._http_client, None, raw_element.get("metadata"))
        self.properties: List[ExtensionProperty] = [ExtensionProperty(self._http_client, None, prop) for prop in raw_element.get("properties")]


class ExtensionDto(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.type: str = raw_element.get("type")

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
        return PaginatedList(ExtensionShortRepresentation, self._http_client, f"/api/config/v1/extensions/{self.id}/instances", list_item="configurationsList", target_params=params)

    def delete(self) -> Response:
        """
        Deletes the ZIP file of this extension
        """
        return self._http_client.make_request(f"/api/config/v1/extensions/{self.id}", method="DELETE")
