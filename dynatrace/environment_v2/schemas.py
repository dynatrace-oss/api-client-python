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
