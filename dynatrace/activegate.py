from typing import List

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.entity import EntityShortRepresentation
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


class ActiveGateService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        hostname: str = None,
        os_type: str = None,
        network_address: str = None,
        activegate_type: str = None,
        network_zone: str = None,
        update_status: str = None,
        version_compare_type: str = None,
        version: str = None,
    ) -> PaginatedList["ActiveGate"]:
        """
        Lists all available ActiveGates

        :param hostname: Filters the resulting set of ActiveGates by the name of the host it's running on.
            You can specify a partial name. In that case, the CONTAINS operator is used.

        :param os_type: Filters the resulting set of ActiveGates by the OS type of the host it's running on.
            Available values : LINUX, WINDOWS

        :param network_address: Filters the resulting set of ActiveGates by the network address.
            You can specify a partial address. In that case, the CONTAINS operator is used.

        :param activegate_type: Filters the resulting set of ActiveGates by the ActiveGate type.
            Available values : ENVIRONMENT, ENVIRONMENT_MULTI

        :param network_zone: Filters the resulting set of ActiveGates by the network zone.
            You can specify a partial name. In that case, the CONTAINS operator is used.

        :param update_status: Filters the resulting set of ActiveGates by the auto-update status.
            Available values : INCOMPATIBLE, OUTDATED, SUPPRESSED, UNKNOWN, UP2DATE, UPDATE_IN_PROGRESS, UPDATE_PENDING, UPDATE_PROBLEM

        :param version_compare_type: Filters the resulting set of ActiveGates by the specified version.
            Specify the comparison operator here.
            Available values : EQUAL, GREATER, GREATER_EQUAL, LOWER, LOWER_EQUAL
            Default value : EQUAL

        :param version: Filters the resulting set of ActiveGates by the specified version.
            Specify the version in <major>.<minor>.<revision> format (for example, 1.195.0) here.

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
        }
        return PaginatedList(ActiveGate, self.__http_client, "/api/v2/activeGates", params, list_item="activeGates")


class ActiveGate(EntityShortRepresentation):
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
