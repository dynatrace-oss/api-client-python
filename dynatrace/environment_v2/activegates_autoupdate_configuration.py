from typing import Dict, Any

from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.http_client import HttpClient


class ActiveGateAutoUpdateConfigurationService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get_global(self) -> "ActiveGateGlobalAutoUpdateConfig":
        return ActiveGateGlobalAutoUpdateConfig(raw_element=self.__http_client.make_request("/api/v2/activeGates/autoUpdate").json())

    def put_global(self, setting: str) -> Response:
        """
        Puts the global auto-update configuration of environment ActiveGates

        :param setting: The state of auto-updates for all ActiveGates connected to the environment or Managed cluster. ENABLED or DISABLED
        """
        return self.__http_client.make_request("/api/v2/activeGates/autoUpdate", method="PUT", params={"globalSetting": setting})

    def validate_global(self, setting: str) -> Response:
        return self.__http_client.make_request("/api/v2/activeGates/autoUpdate/validator", method="POST", params={"globalSetting": setting})

    def get(self, activegate_id: str) -> "ActiveGateAutoUpdateConfig":
        return ActiveGateAutoUpdateConfig(raw_element=self.__http_client.make_request(f"/api/v2/activeGates/{activegate_id}/autoUpdate").json())

    def put(self, activegate_id: str, setting: str) -> Response:
        return self.__http_client.make_request(f"/api/v2/activeGates/{activegate_id}/autoUpdate", method="PUT", params={"setting": setting})

    def validate(self, activegate_id: str, setting: str) -> Response:
        return self.__http_client.make_request(f"/api/v2/activeGates/{activegate_id}/autoUpdate/validator", method="POST", params={"setting": setting})


class ActiveGateGlobalAutoUpdateConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.global_setting: str = raw_element.get("globalSetting")
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))


class ActiveGateAutoUpdateConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.setting: str = raw_element.get("setting")
        self.effective_setting: str = raw_element.get("effectiveSetting")
