from requests import Response
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.configuration_v1.endpoint import EndpointShortRepresentation
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject


class PluginService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList["PluginShortRepresentation"]:
        """
        List all uploaded plugins
        """
        return PaginatedList(PluginShortRepresentation, self.__http_client, "/api/config/v1/plugins", list_item="values")

    def list_states(self, plugin_id) -> PaginatedList["PluginState"]:
        """
        List the states of the specified plugin
        """
        return PaginatedList(PluginState, self.__http_client, f"/api/config/v1/plugins/{plugin_id}/states", list_item="states")

    def delete(self, plugin_id) -> Response:
        """
        Deletes the ZIP file of the specified plugin
        :param plugin_id: The ID of the plugin to be deleted
        """
        return self.__http_client.make_request(f"/api/config/v1/plugins/{plugin_id}/binary", method="DELETE")


class PluginState(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.plugin_id: str = raw_element.get("pluginId")
        self.version: str = raw_element.get("version")
        self.endpoint_id: str = raw_element.get("endpointId")
        self.state: str = raw_element.get("state")
        self.state_description: str = raw_element.get("stateDescription")
        self.timestamp: str = raw_element.get("timestamp")
        self.host_id: str = raw_element.get("hostId")
        self.process_id: str = raw_element.get("processId")


class PluginShortRepresentation(EntityShortRepresentation):
    def delete(self) -> Response:
        """
        Deletes the ZIP file of this plugin
        """
        return self._http_client.make_request(f"/api/config/v1/plugins/{self.id}/binary", method="DELETE")

    @property
    def endpoints(self) -> PaginatedList[EndpointShortRepresentation]:
        return PaginatedList(
            EndpointShortRepresentation,
            self._http_client,
            f"/api/config/v1/plugins/{self.id}/endpoints",
            None,
            list_item="values",
        )

    @property
    def states(self) -> PaginatedList[PluginState]:
        return PaginatedList(PluginState, self._http_client, f"/api/config/v1/plugins/{self.id}/states", None, list_item="states")
