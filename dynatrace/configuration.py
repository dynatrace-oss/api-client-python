from typing import List
from dynatrace.dynatrace_object import DynatraceObject


class ConfigurationMetadata(DynatraceObject):
    @property
    def cluster_version(self) -> str:
        return self._cluster_version

    @property
    def configuration_versions(self) -> List[str]:
        return self._configuration_versions

    @property
    def current_configuration_versions(self) -> List[str]:
        return self._current_configuration_versions

    def _create_from_raw_data(self, raw_element):
        self._cluster_version = raw_element.get("clusterVersion")
        self._configuration_versions = raw_element.get("configurationVersions")
        self._current_configuration_versions = raw_element.get("currentConfigurationVersions")
