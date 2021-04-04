from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.configuration import ConfigurationMetadata
from dynatrace.http_client import HttpClient


class ActiveGateAutoUpdateService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get_global(self) -> "ActiveGateGlobalAutoUpdateConfig":
        return ActiveGateGlobalAutoUpdateConfig(raw_element=self.__http_client.make_request("/api/v2/activeGates/autoUpdate").json())


class ActiveGateGlobalAutoUpdateConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.global_setting: str = raw_element.get("globalSetting")
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))
