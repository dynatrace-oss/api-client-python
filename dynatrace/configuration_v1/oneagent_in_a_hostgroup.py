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
from typing import Dict, Any, Optional, Union

from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.configuration_v1.schemas import AutoUpdateSetting, UpdateWindowsConfig, EffectiveSetting


class OneAgentInAHostGroupService:
    ENDPOINT = "/api/config/v1/hostgroups"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get(self, hostgroup_id: str) -> "OneAgentHostGroupConfig":
        """Gets the OneAgent configuration in the specified host group

        :param hostgroup_id: The Dynatrace entity ID of the required host group.

        :returns OneAgentHostGroupConfig: the full OneAgent configuration in this host group
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{hostgroup_id}").json()
        return OneAgentHostGroupConfig(response)

    def get_autoupdate(self, hostgroup_id: str) -> "HostGroupAutoUpdateConfig":
        """Gets the configuration of OneAgent auto-update in the specified host group

        :param hostgroup_id: The Dynatrace entity ID of the required host group.

        :returns HostGroupAutoUpdateConfig: The The auto-update configuration details in this host group
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{hostgroup_id}/autoupdate").json()
        return HostGroupAutoUpdateConfig(response)

    def put_autoupdate(self, hostgroup_id: str, config: "HostGroupAutoUpdateConfig") -> "Response":
        """Updates the configuration of OneAgent auto-update in the specified host group

        OneAgents are updated several minutes after the change of configuration.
        The process can take more time depending on number of OneAgents in the update queue.

        :param hostgroup_id: The Dynatrace entity ID of the required host group.
        :param config: he updated auto-update configuration object

        :returns Response: HTTP Response to the request
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{hostgroup_id}/autoupdate", method="PUT", params=config.to_json())

    def is_valid_autoupdate(self, hostgroup_id: str, config: "HostGroupAutoUpdateConfig") -> bool:
        """Validates the payload for the put_autoupdate function

        :param hostgroup_id: The Dynatrace entity ID of the required host group.
        :param config: the auto-update configuration object to validate

        :returns bool: True if valid, False otherwise
        """
        try:
            self.__http_client.make_request(path=f"{self.ENDPOINT}/{hostgroup_id}/autoupdate", method="POST", params=config.to_json())
        except Exception as e:
            print(e.args)
            return False
        else:
            return True


class OneAgentHostGroupConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.auto_update_config: HostGroupAutoUpdateConfig = HostGroupAutoUpdateConfig(raw_element=raw_element.get("autoUpdateConfig"))


class HostGroupAutoUpdateConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("configurationMetadata"))
        self.id: str = raw_element.get("id")
        self.setting: AutoUpdateSetting = AutoUpdateSetting(raw_element.get("setting"))
        self.version: Optional[Union[str, None]] = raw_element.get("version")
        self.update_windows: UpdateWindowsConfig = UpdateWindowsConfig(raw_element.get("updateWindows"))
        self.effective_setting: Optional[Union[EffectiveSetting, None]] = (
            EffectiveSetting(raw_element.get("effectiveSetting")) if raw_element.get("effectiveSetting") else None
        )
        self.effective_version: Optional[Union[str, None]] = raw_element.get("effectiveVersion")

    def to_json(self) -> Dict[str, Any]:
        return {
            "setting": str(self.setting),
            "version": self.version,
            "updateWindows": self.update_windows.to_json(),
            "effectiveSetting": str(self.effective_setting) if self.effective_setting else None,
            "effectiveVersion": self.effective_version,
        }
