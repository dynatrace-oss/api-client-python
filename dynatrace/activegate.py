from typing import List

from dynatrace.dynatrace_object import DynatraceObject

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


class ActiveGate(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def network_addresses(self) -> List[str]:
        return self._network_addresses

    @property
    def os_type(self) -> str:
        return self._os_type

    @property
    def auto_update_status(self) -> str:
        return self._auto_update_status

    @property
    def type(self) -> str:
        return self._type

    @property
    def offline_since(self) -> str:
        return self._offline_since

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def main_environment(self) -> str:
        return self._main_environment

    @property
    def environments(self) -> List[str]:
        return self._environments

    @property
    def network_zone(self) -> List[str]:
        return self._network_zone

    def _create_from_raw_data(self, raw_element: dict):
        self._id = raw_element.get("id")
        self._network_addresses = raw_element.get("networkAddresses", [])
        self._os_type = raw_element.get("osType")
        self._auto_update_status = raw_element.get("autoUpdateStatus")
        self._offline_since = raw_element.get("offlineSince")
        self._version = raw_element.get("version")
        self._type = raw_element.get("type")
        self._hostname = raw_element.get("hostname")
        self._main_environment = raw_element.get("mainEnvironment")
        self._environments = raw_element.get("environments", [])
        self._network_zone = raw_element.get("networkZone")
