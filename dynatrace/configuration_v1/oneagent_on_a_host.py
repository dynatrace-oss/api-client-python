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


from enum import Enum
from requests import Response
from typing import Dict, Any, Optional, List, Union

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.configuration_v1.schemas import AutoUpdateSetting, UpdateWindowsConfig, EffectiveSetting


class OneAgentOnAHostService:
    ENDPOINT = "/api/config/v1/hosts"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get(self, host_id: str) -> "HostConfig":
        """Gets the full OneAgent configuration on the specified host

        :param host_id: The Dynatrace entity ID of the required host.

        :returns HostConfig: The full OneAgent configuration details on this host
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}").json()
        return HostConfig(raw_element=response)

    def get_autoupdate(self, host_id: str) -> "HostAutoUpdateConfig":
        """Gets the configuration of OneAgent auto-update on the specified host

        :param host_id: The Dynatrace entity ID of the required host.

        :returns HostAutoUpdateConfig: The auto-update configuration details on this host
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}/autoupdate").json()
        return HostAutoUpdateConfig(raw_element=response)

    def get_monitoring(self, host_id: str) -> "MonitoringConfig":
        """Gets the monitoring configuration of OneAgent on the specified host

        :param host_id: The Dynatrace entity ID of the required host.

        :returns MonitoringConfig: The monitoring configuration details on this host
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}/monitoring").json()
        return MonitoringConfig(raw_element=response)

    def get_technologies(self, host_id: str) -> "TechMonitoringList":
        """Gets the configuration of monitored technologies on the specified host

        :param host_id: The Dynatrace entity ID of the required host.

        :returns TechMonitoringList: The monitored technologies configuration details on this host
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}/technologies").json()
        return TechMonitoringList(raw_element=response)

    def put_autoupdate(self, host_id: str, config: "HostAutoUpdateConfig") -> "Response":
        """Updates the configuration of OneAgent auto-update on the specified host.

        OneAgent is updated several minutes after the change of configuration.
        The process can take more time depending on number of OneAgents in the update queue.

        :param host_id: The Dynatrace entity ID of the required host.
        :param config: the updated auto-update configuration object

        :returns Response: HTTP Response to the request
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}/autoupdate", method="PUT", params=config.to_json())

    def put_monitoring(self, host_id: str, config: "MonitoringConfig") -> "Response":
        """Updates the monitoring configuration of OneAgent on the specified host.

        The monitoring mode of OneAgent is updated several minutes after the change of configuration.

        :param host_id: The Dynatrace entity ID of the required host.
        :param config: the updated monitoring configuration object

        :returns Response: HTTP Response to the request
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}/monitoring", method="PUT", params=config.to_json())

    def is_valid_autoupdate(self, host_id: str, config: "HostAutoUpdateConfig") -> bool:
        """Validates the payload for the put_autoupdate function

        :param host_id: The Dynatrace entity ID of the required host.
        :param config: the auto-update configuration object to validate

        :returns bool: True if valid, False otherwise
        """
        try:
            self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}/autoupdate/validator", method="POST", params=config.to_json())
        except Exception as e:
            print(e.args)
            return False
        else:
            return True

    def is_valid_monitoring(self, host_id: str, config: "MonitoringConfig") -> bool:
        """Validates the payload for the put_monitoring function

        :param host_id: The Dynatrace entity ID of the required host.
        :param config: the monitoring configuration object to validate

        :returns bool: :returns bool: True if valid, False otherwise
        """
        try:
            self.__http_client.make_request(path=f"{self.ENDPOINT}/{host_id}/monitoring/validator", method="POST", params=config.to_json())
        except Exception as e:
            print(e.args)
            return False
        else:
            return True


class HostConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.monitoring_config: MonitoringConfig = MonitoringConfig(raw_element=raw_element.get("monitoringConfig"))
        self.auto_update_config: HostAutoUpdateConfig = HostAutoUpdateConfig(raw_element=raw_element.get("autoUpdateConfig"))
        self.tech_monitoring_config_list: TechMonitoringList = TechMonitoringList(raw_element=raw_element.get("techMonitoringConfigList"))


class MonitoringConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.monitoring_enabled: bool = raw_element.get("monitoringEnabled", False)
        self.monitoring_mode: MonitoringMode = MonitoringMode(raw_element.get("monitoringMode"))
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))

    def to_json(self) -> Dict[str, Any]:
        return {
            "monitoringEnabled": str(self.monitoring_enabled),
            "monitoringMode": str(self.monitoring_mode),
        }


class HostAutoUpdateConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.setting: AutoUpdateSetting = AutoUpdateSetting(raw_element.get("setting"))
        self.version: str = raw_element.get("version", "")
        self.update_windows: UpdateWindowsConfig = UpdateWindowsConfig(raw_element=raw_element.get("updateWindows"))
        self.effective_setting: Optional[Union[EffectiveSetting, None]] = (
            EffectiveSetting(raw_element.get("effectiveSetting")) if raw_element.get("effectiveSetting") else None
        )
        self.effective_version: Optional[Union[str, None]] = raw_element.get("effectiveVersion")
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))

    def to_json(self) -> Dict[str, Any]:
        return {
            "setting": str(self.setting),
            "version": self.version,
            "updateWindows": self.update_windows.to_json(),
            "effectiveSetting": str(self.effective_setting) if self.effective_setting else None,
            "effectiveVersion": self.effective_version,
        }


class TechMonitoringList(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.technologies: List[Technology] = [Technology(raw_element=t) for t in raw_element.get("technologies", [])]
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))


class Technology(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: TechnologyType = TechnologyType(raw_element.get("type"))
        self.monitoring_enabled: bool = raw_element.get("monitoringEnabled", False)
        self.scope: Optional[Union[SettingScope, None]] = SettingScope(raw_element.get("scope")) if raw_element.get("scope") else None


class MonitoringMode(Enum):
    """Already exists in environment_v1.oneagents.
    TODO: decide if reuse
    """

    CLOUD_INFRASTRUCTURE = "CLOUD_INFRASTRUCTURE"
    FULL_STACK = "FULL_STACK"

    def __str__(self):
        return self.value


class SettingScope(Enum):
    ENVIRONMENT = "ENVIRONMENT"
    HOST = "HOST"

    def __str__(self):
        return self.value


class TechnologyType(Enum):
    AIX_KERNEL_EXT = "AIX_KERNEL_EXT"
    APACHE = "APACHE"
    CIM_V2 = "CIM_V2"
    DOCKER = "DOCKER"
    DOCKER_WIN = "DOCKER_WIN"
    DOT_NET = "DOT_NET"
    DOT_NET_CORE = "DOT_NET_CORE"
    EXTENSIONS = "EXTENSIONS"
    EXTENSIONS_DS_GENERIC = "EXTENSIONS_DS_GENERIC"
    EXTENSIONS_STATSD = "EXTENSIONS_STATSD"
    GARDEN = "GARDEN"
    GO = "GO"
    GO_STATIC = "GO_STATIC"
    IBM_INTEGRATION_BUS = "IBM_INTEGRATION_BUS"
    IIS = "IIS"
    JAVA = "JAVA"
    LOG_ANALYTICS = "LOG_ANALYTICS"
    NETTRACER = "NETTRACER"
    NETWORK = "NETWORK"
    NGINX = "NGINX"
    NODE_JS = "NODE_JS"
    OPENTRACINGNATIVE = "OPENTRACINGNATIVE"
    PHP = "PHP"
    PHP_80_EA = "PHP_80_EA"
    PHP_CGI = "PHP_CGI"
    PHP_CLI = "PHP_CLI"
    PHP_WIN = "PHP_WIN"
    PROCESS = "PROCESS"
    RUBY = "RUBY"
    SDK = "SDK"
    VARNISH = "VARNISH"
    Z_OS = "Z_OS"

    def __str__(self):
        return self.value
