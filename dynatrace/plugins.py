from datetime import datetime

from requests import Response
from dynatrace.entity import EntityShortRepresentation
from dynatrace.endpoint import EndpointShortRepresentation
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
    @property
    def plugin_id(self) -> str:
        """
        The ID of the plugin.
        """
        return self._plugin_id

    @property
    def version(self) -> str:
        """
        The version of the plugin (for example 1.0.0).
        """
        return self._version

    @property
    def endpoint_id(self) -> str:
        """
        The ID of the endpoint where the state is detected - Active Gate only.
        """
        return self._endpoint_id

    @property
    def state(self) -> str:
        """
        The state of the plugin.
        [ DISABLED, ERROR_AUTH, ERROR_COMMUNICATION_FAILURE, ERROR_CONFIG, ERROR_TIMEOUT, ERROR_UNKNOWN,
         INCOMPATIBLE, LIMIT_REACHED, NOTHING_TO_REPORT, OK, STATE_TYPE_UNKNOWN, UNINITIALIZED, UNSUPPORTED, WAITING_FOR_STATE ]
        """
        return self._state

    @property
    def state_description(self) -> str:
        """
        A short description of the state.
        """
        return self._state_description

    @property
    def timestamp(self) -> datetime:
        """
        The timestamp when the state was detected
        """
        return datetime.utcfromtimestamp(self._timestamp / 1000)

    @property
    def host_id(self) -> str:
        """
        The ID of the host on which the plugin runs.
        """
        return self._host_id

    @property
    def process_id(self) -> str:
        """
        The ID of the entity on which the plugin is active.
        """
        return self._process_id

    def _create_from_raw_data(self, raw_element):
        self._plugin_id = raw_element.get("pluginId")
        self._version = raw_element.get("version")
        self._endpoint_id = raw_element.get("endpointId")
        self._state = raw_element.get("state")
        self._state_description = raw_element.get("stateDescription")
        self._timestamp = raw_element.get("timestamp")
        self._host_id = raw_element.get("hostId")
        self._process_id = raw_element.get("processId")


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
