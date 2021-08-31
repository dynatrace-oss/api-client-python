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


from requests import Response
from typing import Dict, Any, Optional

from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.configuration_v1.schemas import UpdateWindowsConfig, AutoUpdateSetting, TechMonitoringList
from dynatrace.environment_v2.schemas import ConfigurationMetadata


class OneAgentEnvironmentWideConfigService:
    ENDPOINT = "/api/config/v1/hosts/autoupdate"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get(self) -> "EnvironmentAutoUpdateConfig":
        """Gets the environment-wide configuration of OneAgents auto-update.

        :returns EnvironmentAutoUpdateConfig: the auto-update configuration for this environment
        """
        response = self.__http_client.make_request(path=self.ENDPOINT).json()
        return EnvironmentAutoUpdateConfig(raw_element=response, http_client=self.__http_client)

    def get_technologies(self) -> "TechMonitoringList":
        """Gets the global monitoring configuration of technologies.

        :returns TechMonitoringList: the technologies monitoring configuration for this environment
        """
        response = self.__http_client.make_request(path="/api/config/v1/technologies").json()
        return TechMonitoringList(raw_element=response)

    def put(self, config: "EnvironmentAutoUpdateConfig") -> "Response":
        """Updates the environment-wide configuration of OneAgents auto-update

        OneAgents are updated several minutes after the change of configuration.
        The process can take more time depending on number of OneAgents in the update queue.

        :param config: the updated global auto-update configuration object

        :returns Response: HTTP Response to the Request
        """
        return config.put()

    def is_valid(self, config: "EnvironmentAutoUpdateConfig") -> bool:
        """Validates the payload for the put function

        :param config: a global auto-update configuration object

        :returns bool: True if valid, false otherwise.
        """
        try:
            self.__http_client.make_request(path=f"{self.ENDPOINT}/validator", method="POST", params=config.to_json())
        except Exception as e:
            print(e.args)
            return False
        else:
            return True


class EnvironmentAutoUpdateConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))
        self.setting: AutoUpdateSetting = AutoUpdateSetting(raw_element.get("setting"))
        self.version: Optional[str] = raw_element.get("version")
        self.update_windows: UpdateWindowsConfig = UpdateWindowsConfig(raw_element=raw_element.get("updateWindows"))

    def to_json(self) -> Dict[str, Any]:
        return {
            "setting": str(self.setting),
            "version": self.version,
            "updateWindows": self.update_windows.to_json(),
        }

    def put(self) -> "Response":
        return self._http_client.make_request(path=OneAgentEnvironmentWideConfigService.ENDPOINT, method="PUT", params=self.to_json())
