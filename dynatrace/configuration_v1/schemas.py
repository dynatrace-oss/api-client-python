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
from typing import List, Dict, Any, Optional

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.schemas import ConfigurationMetadata

# Schemas that don't belong to a specific API tag.


class UpdateWindowsConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.windows: List[UpdateWindow] = [UpdateWindow(raw_element=uw) for uw in raw_element.get("windows", [])]

    def to_json(self) -> Optional[Dict[str, Any]]:
        if not self.windows:
            return None

        return {"windows": [w.to_json for w in self.windows]}


class UpdateWindow(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id", "")
        self.name: Optional[str] = raw_element.get("name", "")

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
        }


class TechMonitoringList(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.technologies: List[Technology] = [Technology(raw_element=t) for t in raw_element.get("technologies", [])]
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))


class Technology(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: TechnologyType = TechnologyType(raw_element.get("type"))
        self.monitoring_enabled: bool = raw_element.get("monitoringEnabled", False)
        self.scope: Optional[SettingScope] = SettingScope(raw_element.get("scope")) if raw_element.get("scope") else None


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


class AutoUpdateSetting(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    INHERITED = "INHERITED"

    def __str__(self):
        return self.value


class EffectiveSetting(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"

    def __str__(self):
        return self.value


class TagContext(Enum):
    AWS = "AWS"
    AWS_GENERIC = "AWS_GENERIC"
    AZURE = "AZURE"
    CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
    CONTEXTLESS = "CONTEXTLESS"
    ENVIRONMENT = "ENVIRONMENT"
    GOOGLE_CLOUD = "GOOGLE_CLOUD"
    KUBERNETES = "KUBERNETES"

    def __str__(self) -> str:
        return self.value


class StringComparisonOperator(Enum):
    BEGINS_WITH = "BEGINS_WITH"
    CONTAINS = "CONTAINS"
    CONTAINS_REGEX = "CONTAINS_REGEX"
    ENDS_WITH = "ENDS_WITH"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value
