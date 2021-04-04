from typing import List, Optional

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList

OS_TYPE_LINUX = "LINUX"
OS_TYPE_WINDOWS = "WINDOWS"

TYPE_ENVIRONMENT = "ENVIRONMENT"
TYPE_ENVIRONMENT_MULTI = "ENVIRONMENT_MULTI"

UPDATE_STATUS_INCOMPATIBLE = "INCOMPATIBLE"
UPDATE_STATUS_OUTDATED = "OUTDATED"
UPDATE_STATUS_SUPPRESSED = "SUPPRESSED"
UPDATE_STATUS_UNKNOWN = "UNKNOWN"
UPDATE_STATUS_UP2DATE = "UP2DATE"
UPDATE_STATUS_UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
UPDATE_STATUS_UPDATE_PENDING = "UPDATE_PENDING"
UPDATE_STATUS_UPDATE_PROBLEM = "UPDATE_PROBLEM"

VERSION_COMPARE_TYPE_EQUAL = "EQUAL"
VERSION_COMPARE_TYPE_GREATER = "GREATER"
VERSION_COMPARE_TYPE_GREATER_EQUAL = "GREATER_EQUAL"
VERSION_COMPARE_TYPE_LOWER = "LOWER"
VERSION_COMPARE_TYPE_LOWER_EQUAL = "LOWER_EQUAL"

AUTO_UPDATE_ENABLED = "ENABLED"
AUTO_UPDATE_DISABLED = "DISABLED"

MODULE_AWS = "AWS"
MODULE_AZURE = "AZURE"
MODULE_BEACON_FORWARDER = "BEACON_FORWARDER"
MODULE_CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
MODULE_DB_INSIGHT = "DB_INSIGHT"
MODULE_EXTENSIONS_V1 = "EXTENSIONS_V1"
MODULE_EXTENSIONS_V2 = "EXTENSIONS_V2"
MODULE_KUBERNETES = "KUBERNETES"
MODULE_LOGS = "LOGS"
MODULE_MEMORY_DUMPS = "MEMORY_DUMPS"
MODULE_METRIC_API = "METRIC_API"
MODULE_ONE_AGENT_ROUTING = "ONE_AGENT_ROUTING"
MODULE_OTLP_INGEST = "OTLP_INGEST"
MODULE_REST_API = "REST_API"
MODULE_SYNTHETIC = "SYNTHETIC"


class ActiveGateService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        hostname: Optional[str] = None,
        os_type: Optional[str] = None,
        network_address: Optional[str] = None,
        activegate_type: Optional[str] = None,
        network_zone: Optional[str] = None,
        update_status: Optional[str] = None,
        version_compare_type: Optional[str] = None,
        version: Optional[str] = None,
        auto_update: Optional[str] = None,
        group: Optional[str] = None,
        online: Optional[bool] = None,
        enabled_modules: Optional[List[str]] = None,
        disabled_modules: Optional[List[str]] = None,
    ) -> PaginatedList["ActiveGate"]:
        """
        Lists all available ActiveGates
        :return: A list of ActiveGates.
        """
        params = {
            "hostname": hostname,
            "osType": os_type,
            "networkAddress": network_address,
            "ActivegateType": activegate_type,
            "networkZone": network_zone,
            "updateStatus": update_status,
            "versionCompareType": version_compare_type,
            "version": version,
            "autoUpdate": auto_update,
            "group": group,
            "online": online,
            "enabledModule": enabled_modules,
            "disabledModule": disabled_modules,
        }
        return PaginatedList(ActiveGate, self.__http_client, "/api/v2/activeGates", params, list_item="activeGates")

    def get(self, activegate_id: str) -> "ActiveGate":
        return ActiveGate(raw_element=self.__http_client.make_request(f"/api/v2/activeGates/{activegate_id}").json())


class ActiveGate(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        self.id: str = raw_element.get("id")
        self.network_addresses = raw_element.get("networkAddresses", [])
        self.os_type: str = raw_element.get("osType")
        self.auto_update_status: str = raw_element.get("autoUpdateStatus")
        self.offline_since: int = raw_element.get("offlineSince")
        self.version: str = raw_element.get("version")
        self.type: str = raw_element.get("type")
        self.hostname: str = raw_element.get("hostname")
        self.main_environment: str = raw_element.get("mainEnvironment")
        self.environments: str = raw_element.get("environments", [])
        self.network_zone: str = raw_element.get("networkZone")
        self.group: str = raw_element.get("group")
        self.modules: List["ActiveGateModule"] = [ActiveGateModule(raw_element=module) for module in raw_element.get("modules")]


class ActiveGateModule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        self.misconfigured: bool = raw_element.get("misconfigured")
        self.type: str = raw_element.get("type")
        self.attributes: bool = raw_element.get("attributes")
        self.enabled: bool = raw_element.get("enabled")
        self.version: str = raw_element.get("version")
