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
from typing import List, Dict, Any
from dynatrace.dynatrace_object import DynatraceObject

# Schemas that don't belong to a specific api tag


class ConfigurationMetadata(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.cluster_version: str = raw_element.get("clusterVersion")
        self.configuration_versions: List[int] = raw_element.get("configurationVersions")
        self.current_configuration_versions: List[int] = raw_element.get("currentConfigurationVersions")


class EntityType(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        # TODO - Implement other properties
        self.entity_type = raw_element.get("type")
        self.properties = raw_element.get("properties", [])


class VersionCompareType(Enum):
    EQUAL: str = "EQUAL"
    GREATER: str = "GREATER"
    GREATER_EQUAL: str = "GREATER_EQUAL"
    LOWER: str = "LOWER"
    LOWER_EQUAL: str = "LOWER_EQUAL"


class ManagementZone(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.name: str = raw_element.get("name")
        self.id: str = raw_element.get("id")
