from typing import List
from dynatrace.dynatrace_object import DynatraceObject


class ConfigurationMetadata(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.cluster_version: str = raw_element.get("clusterVersion")
        self.configuration_versions: List[int] = raw_element.get("configurationVersions")
        self.current_configuration_versions: List[int] = raw_element.get("currentConfigurationVersions")
