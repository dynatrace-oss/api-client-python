from typing import List

from requests import Response

from dynatrace.configuration import ConfigurationMetadata
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.endpoint import EndpointShortRepresentation
from dynatrace.entity import EntityShortRepresentation
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class ExtensionService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client
        pass

    def list_endpoints(self, plugin_id: str) -> PaginatedList[EndpointShortRepresentation]:
        """
        Lists endpoints of the specified ActiveGate plugin
        """
        return PaginatedList("EndpointShortRepresentation", self.__http_client, f"/api/config/v1/plugins/{plugin_id}/endpoints", list_item="values")

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
        enabled: bool = True,
        use_global: bool = True,
        properties: dict = None,
        host_id: str = None,
        active_gate: EntityShortRepresentation = None,
        endpoint_id: str = None,
        endpoint_name: str = None,
    ) -> "ExtensionConfigurationDto":

        return ExtensionConfigurationDto(self.__http_client, extension_id, enabled, use_global, properties, host_id, active_gate, endpoint_id, endpoint_name)


class ExtensionProperty(DynatraceObject):
    @property
    def key(self) -> str:
        return self._key

    @property
    def type(self) -> str:
        return self._type

    @property
    def default_value(self) -> str:
        return self._default_value

    @property
    def dropdown_values(self) -> List[str]:
        return self._dropdown_values

    def _create_from_raw_data(self, raw_element):
        self._key = raw_element.get("key")
        self._type = raw_element.get("type")
        self._default_value = raw_element.get("defaultValue")
        self._dropdown_values = raw_element.get("dropdownValues")


class ExtensionConfigurationDto(DynatraceObject):
    def __init__(
        self,
        http_client,
        extension_id: str,
        enabled: bool = True,
        use_global: bool = True,
        properties: dict = None,
        host_id: str = None,
        active_gate: EntityShortRepresentation = None,
        endpoint_id: str = None,
        endpoint_name: str = None,
    ):
        raw_element = {
            "extensionId": extension_id,
            "enabled": enabled,
            "useGlobal": use_global,
            "properties": properties,
            "hostId": host_id,
            "activeGate": active_gate._raw_element,
            "endpointId": endpoint_id,
            "endpointName": endpoint_name,
        }

        super().__init__(http_client, None, raw_element)

    def post(self):
        return self._http_client.make_request(f"/api/config/v1/extensions/{self.extension_id}/instances", params=self._raw_element, method="POST")

    @property
    def extension_id(self) -> str:
        return self._extension_id

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def use_global(self) -> bool:
        return self._use_global

    @property
    def properties(self) -> dict:
        return self._properties

    @property
    def host_id(self) -> str:
        return self._host_id

    @property
    def active_gate(self) -> EntityShortRepresentation:
        return self._active_gate

    @property
    def endpoint_id(self) -> str:
        return self._endpoint_id

    @property
    def endpoint_name(self) -> str:
        return self._endpoint_name

    def _create_from_raw_data(self, raw_element):
        self._extension_id = raw_element.get("extensionId")
        self._enabled = raw_element.get("enabled")
        self._use_global = raw_element.get("useGlobal")
        self._properties = raw_element.get("properties")
        self._host_id = raw_element.get("hostId")
        self._active_gate = EntityShortRepresentation(self._http_client, None, raw_element.get("activeGate"))
        self._endpoint_id = raw_element.get("endpointId")
        self._endpoint_name = raw_element.get("endpointName")


class ExtensionShortRepresentation(EntityShortRepresentation):
    def get_full_configuration(self, extension_id: str):
        """
        Gets the full extension configuration for this ExtensionShortRepresentation
        """
        response = self._http_client.make_request(f"/api/config/v1/extensions/{extension_id}/instances/{self.id}").json()
        return ExtensionConfigurationDto(self._http_client, None, response)


class Extension(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def version(self):
        return self._version

    @property
    def metric_group(self):
        return self._metric_group

    @property
    def metadata(self) -> ConfigurationMetadata:
        return self._metadata

    @property
    def properties(self) -> List[ExtensionProperty]:
        return self._properties

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._type = raw_element.get("type")
        self._version = raw_element.get("version")
        self._metric_group = raw_element.get("metricGroup")
        self._metadata = ConfigurationMetadata(self._http_client, None, raw_element.get("metadata"))
        self._properties = [ExtensionProperty(self._http_client, None, prop) for prop in raw_element.get("properties")]


class ExtensionDto(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._type = raw_element.get("type")

    def get_full_extension(self) -> Extension:
        """
        Gets the full extension for this ExtensionDto
        """
        response = self._http_client.make_request(f"/api/config/v1/extensions/{self.id}").json()
        return Extension(self._http_client, None, response)

    @property
    def instances(self) -> PaginatedList[ExtensionShortRepresentation]:
        return PaginatedList(
            ExtensionShortRepresentation,
            self._http_client,
            f"/api/config/v1/extensions/{self.id}/instances",
            list_item="configurationsList",
        )

    def delete(self) -> Response:
        """
        Deletes the ZIP file of this extension
        """
        return self._http_client.make_request(f"/api/config/v1/extensions/{self.id}", method="DELETE")
