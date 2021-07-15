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
from typing import Optional, Dict, List, Any
from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient


class DeploymentService:
    ENDPOINT_INSTALLER_AGENT = "/api/v1/deployment/installer/agent"
    ENDPOINT_INSTALLER_GATEWAY = "/api/v1/deployment/installer/gateway"
    ENDPOINT_BOSHRELEASE = "/api/v1/deployment/boshrelease"
    ENDPOINT_LAMBDA = "/api/v1/deployment/lambda/agent/latest"
    ENDPOINT_ORCHESTRATION = "/api/v1/deployment/orchestration/agent"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def get_agent_installer_latest_metainfo(
        self, os_type: str, installer_type: str, flavor: Optional[str] = None, arch: Optional[str] = None, bitness: Optional[str] = None
    ) -> "InstallerMetaInfoDto":
        """Returns the OneAgent version of the installer of the specified type.
        Non-required parameters are only applicable to the paas and paas-sh installer types.

        :param os_type: The operating system of the installer. Use one of: windows, unix, aix, solaris
        :param installer_type: The type of installer. Use one of:
            - default: Self-extracting installer for manual installation. Downloads an .exe file for Windows or an .sh file for Unix.
            - paas: Code modules installer. Downloads a *.zip archive, containing the manifest.json file with meta information or a .jar file for z/OS.
            - paas-sh: Code modules installer. Downloads a self-extracting shell script with the embedded tar.gz archive. \n
        :param flavor: (only for paas and paas-sh) the flavor of your Linux distribution. Use one of:
            - musl: for Linux distributions, which are using the musl C standard library, for example Alpine Linux.
            - multidistro: for all Linux distributions which are using musl C and glibc standard library. \n
        :param arch: (only for paas and paas-sh) the architecture of your OS. Use one of:
            - all: Use this value for AIX and z/OS. Defaults to x86 for other OS types.
            - x86: x86 architecture.
            - ppc: PowerPC architecture, only supported for AIX and Linux.
            - ppcle: PowerPC Little Endian architecture, only supported for Linux.
            - sparc: Sparc architecture, only supported for Solaris.
            - arm: ARM architecture, only supported for Linux.
            - s390: S/390 architecture, only supported for Linux. \n
        :param bitness: (only for paas and paas-sh) the bitness of your OS. Must be supported by the OS. Use one of:
            - 32
            - 64
            - all \n

        :returns InstallerMetaInfo: the latest version of the installer of that type
        """
        params = {"flavor": flavor, "arch": arch, "bitness": bitness}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_AGENT}/{os_type}/{installer_type}/latest/metainfo", params=params)
        return InstallerMetaInfoDto(raw_element=response.json())

    def get_agent_installer(
        self,
        os_type: str,
        installer_type: str,
        version: str = "latest",
        flavor: Optional[str] = None,
        arch: Optional[str] = None,
        bitness: Optional[str] = None,
        include: Optional[List[str]] = None,
        skip_metadata: Optional[bool] = None,
        network_zone: Optional[str] = None,
        if_none_match: Optional[str] = None,
    ) -> "Response":
        """Downloads OneAgent installer of the specified version.
        The installer is avaialable in the "content" attribute of the response.

        :param os_type: The operating system of the installer. Use one of: windows, unix, aix, solaris
        :param installer_type: The type of installer. Use one of:
            - default: Self-extracting installer for manual installation. Downloads an .exe file for Windows or an .sh file for Unix.
            - paas: Code modules installer. Downloads a *.zip archive, containing the manifest.json file with meta information or a .jar file for z/OS.
            - paas-sh: Code modules installer. Downloads a self-extracting shell script with the embedded tar.gz archive. \n
        :param version: The exact version of the OneAgent installer. If none is provided, latest available is used.
        :param flavor: (only for paas and paas-sh) the flavor of your Linux distribution. Use one of:
            - musl: for Linux distributions, which are using the musl C standard library, for example Alpine Linux.
            - multidistro: for all Linux distributions which are using musl C and glibc standard library. \n
        :param arch: (only for paas and paas-sh) the architecture of your OS. Use one of:
            - all: Use this value for AIX and z/OS. Defaults to x86 for other OS types.
            - x86: x86 architecture.
            - ppc: PowerPC architecture, only supported for AIX and Linux.
            - ppcle: PowerPC Little Endian architecture, only supported for Linux.
            - sparc: Sparc architecture, only supported for Solaris.
            - arm: ARM architecture, only supported for Linux.
            - s390: S/390 architecture, only supported for Linux. \n
        :param bitness: (only for paas and paas-sh) the bitness of your OS. Must be supported by the OS. Use one of:
            - 32
            - 64
            - all \n
        :param include: (only for paas and paas-sh) the code modules to be included to the installer (e.g. ['java', 'apache'])
        :param skip_metadata: (only for paas and paas-sh) set true to omit the OneAgent connectivity information from the installer.
        :param network_zone: the network zone you want the result to be configured with.
        :param if_none_match: The ETag of the previous request. Do not download if it matches the ETag of the installer.
            The ETag is available in the headers of the response.

        :returns Response: HTTP Response to the request. Can be written to file from the "content" attribute.
        """
        if version != "latest":
            version = "version/" + version
        params = {
            "flavor": flavor,
            "arch": arch,
            "bitness": bitness,
            "include": "&include=".join(include) if include else None,
            "skipMetadata": skip_metadata,
            "networkZone": network_zone,
        }
        headers = {"If-None-Match": if_none_match} if if_none_match else None
        return self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_AGENT}/{os_type}/{installer_type}/{version}", params=params, headers=headers)

    def get_agent_installer_connection_info(self, network_zone: Optional[str] = "default", version: Optional[str] = None) -> "ConnectionInfo":
        """Gets the connectivity information for OneAgent.

        :param network_zone: The network zone you want the result to be configured with.
        :param version: The version of the OneAgent to which the result will be applied.

        :returns ConnectionInfo: connectivity information
        """
        params = {"networkZone": network_zone, "version": version}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_AGENT}/connectioninfo", params=params)

        return ConnectionInfo(raw_element=response.json())

    def get_agent_installer_connection_endpoints(self, network_zone: Optional[str] = "default") -> str:
        """Gets the list of the ActiveGate-Endpoints to be used for Agents.
        Ordered by networkzone-priorities. Highest priority first, separated by a semicolon.
        Responds with 404 if network zone is not known.

        :param network_zone: The network zone you want the result to be configured with.

        :returns str: ActiveGate Endpoints separated by semicolons
        """
        params = {"networkZone": network_zone}
        return self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_AGENT}/connectioninfo/endpoints", params=params).text

    def list_agent_installer_versions(
        self, os_type: str, installer_type: str, flavor: Optional[str] = None, arch: Optional[str] = None
    ) -> "AgentInstallerVersions":
        """Lists all available versions of OneAgent installer

        :param os_type: The operating system of the installer. Use one of: windows, unix, aix, solaris
        :param installer_type: The type of installer. Use one of:
            - default: Self-extracting installer for manual installation. Downloads an .exe file for Windows or an .sh file for Unix.
            - paas: Code modules installer. Downloads a *.zip archive, containing the manifest.json file with meta information or a .jar file for z/OS.
            - paas-sh: Code modules installer. Downloads a self-extracting shell script with the embedded tar.gz archive. \n
        :param flavor: (only for paas and paas-sh) the flavor of your Linux distribution. Use one of:
            - musl: for Linux distributions, which are using the musl C standard library, for example Alpine Linux.
            - multidistro: for all Linux distributions which are using musl C and glibc standard library. \n
        :param arch: (only for paas and paas-sh) the architecture of your OS. Use one of:
            - all: Use this value for AIX and z/OS. Defaults to x86 for other OS types.
            - x86: x86 architecture.
            - ppc: PowerPC architecture, only supported for AIX and Linux.
            - ppcle: PowerPC Little Endian architecture, only supported for Linux.
            - sparc: Sparc architecture, only supported for Solaris.
            - arm: ARM architecture, only supported for Linux.
            - s390: S/390 architecture, only supported for Linux. \n

        :returns AgentInstallerVersions: list of available versions of the OneAgent installer
        """
        params = {"flavor": flavor, "arch": arch}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_AGENT}/versions/{os_type}/{installer_type}", params=params)

        return AgentInstallerVersions(raw_element=response.json())

    def get_gateway_installer_connection_info(self, network_zone: Optional[str] = "default") -> "ActiveGateConnectionInfo":
        """Gets the connectivity information for Environment ActiveGate.

        :param network_zone: The network zone you want the result to be configured with.

        :returns ActiveGateConnectionInfo: connectivity information
        """
        params = {"networkZone": network_zone}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_GATEWAY}/connectioninfo", params=params)

        return ActiveGateConnectionInfo(raw_element=response.json())

    def list_gateway_installer_versions(self, os_type: str) -> "ActiveGateInstallerVersions":
        """Lists all available versions of ActiveGate installer.

        :param os_type: The operating system of the installer. Use one of:
            - windows
            - unix

        :returns ActiveGateInstallerVersions: all available versions of the installer
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_GATEWAY}/versions/{os_type}")
        return ActiveGateInstallerVersions(raw_element=response.json())

    def get_gateway_installer(self, os_type: str, version: str = "latest", if_none_match: Optional[str] = None) -> "Response":
        """Downloads the configured standard ActiveGate installer.

        :param os_type: The operating system of the installer. Use one of:
            - windows
            - unix \n
        :param version: The required version of the ActiveGate installer, in 1.155.275.20181112-084458 format.
            If none is specified, latest available version is used.
        :param if_none_match: The ETag of the previous request. Do not download if it matches the ETag of the installer.
            The ETag is available in the headers of the response.

        :returns Response: HTTP Response to the request. Can be written to file from the "content" attribute.
        """
        if version != "latest":
            version = "version/" + version
        headers = {"If-None-Match": if_none_match} if if_none_match else None
        return self.__http_client.make_request(path=f"{self.ENDPOINT_INSTALLER_GATEWAY}/{os_type}/{version}", headers=headers)

    def list_boshrelease_agent_versions(self, os_type: str) -> "BoshReleaseAvailableVersions":
        """Lists available OneAgent versions for BOSH release tarballs.

        :param os_type: The operating system of the installer. Use one of:
            - windows
            - unix \n

        :returns BoshReleaseAvailableVersions: available versions
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_BOSHRELEASE}/versions/{os_type}")
        return BoshReleaseAvailableVersions(raw_element=response.json())

    def get_boshrelease_agent_checksum(
        self, os_type: str, version: str, skip_metadata: Optional[bool] = None, network_zone: Optional[str] = None
    ) -> "BoshReleaseChecksum":
        """Gets the checksum of the specified BOSH release tarball.
        The checksum is the sha256 hash of the installer file. For SaaS only works on environment ActiveGates version 1.176 or higher

        :param os_type: The operating system of the installer. Use one of:
            - windows
            - unix \n
        :param version: The required version of the OneAgent in the 1.155.275.20181112-084458 format.
        :param skip_metadata: Set true to omit the OneAgent connectivity information from the installer. If not set, false is used.
        :param network_zone: The network zone you want the result to be configured with.

        :returns BoshReleaseChecksum: checksum of the BOSH release tarball
        """
        params = {"skipMetadata": skip_metadata, "networkZone": network_zone}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_BOSHRELEASE}/agent/{os_type}/version/{version}/checksum", params=params)

        return BoshReleaseChecksum(raw_element=response.json())

    def get_boshrelease_agent(self, os_type: str, version: str, skip_metadata: Optional[bool] = None, network_zone: Optional[str] = None) -> "Response":
        """Downloads the BOSH release tarballs of the specified version, OneAgent included.
        For SaaS, the call is executed on an Environment ActiveGate. *Be sure to use the base URL of an ActiveGate, not the environment*

        :param os_type: The operating system of the installer. Use one of:
            - windows
            - unix \n
        :param version: The required version of the OneAgent in the 1.155.275.20181112-084458 format.
        :param skip_metadata: Set true to omit the OneAgent connectivity information from the installer. If not set, false is used.
        :param network_zone: The network zone you want the result to be configured with.

        :returns Response: HTTP Response to the request. Can be written to file from the "content" attribute.
        """
        params = {"skipMetadata": skip_metadata, "networkZone": network_zone}
        return self.__http_client.make_request(path=f"{self.ENDPOINT_BOSHRELEASE}/agent/{os_type}/version/{version}", params=params)

    def get_lambda_agent_versions(self) -> "LatestLambdaLayerNames":
        """Get the latest version names of the OneAgent for AWS Lambda.
        Version names include Java, Node.js, and Python AWS Lambda runtime.

        :returns LatestLambdaLayerNames: version names
        """
        return LatestLambdaLayerNames(raw_element=self.__http_client.make_request(path=f"{self.ENDPOINT_LAMBDA}").json())

    def get_orchestration_agent(self, orchestration_type: str, version: str = "latest") -> "Response":
        """Downloads the OneAgent deployment orchestration tarball.

        :param orchestration_type: The Orchestration Type of the orchestration deployment script. Use one of:
            - ansible
            - puppet \n
        :param version: The requested version of the OneAgent orchestration deployment tarball in 0.1.0.20200925-120822 format.
            If none is provided, the latest available is used.

        :returns Response: HTTP Response to the request. Can be written to file from the "content" attribute.
        """
        if version != "latest":
            version = "version/" + version
        return self.__http_client.make_request(path=f"{self.ENDPOINT_ORCHESTRATION}/{orchestration_type}/{version}")

    def get_orchestration_agent_signature(self, orchestration_type: str, version: str = "latest") -> "Response":
        """ ""Downloads the signature matching the OneAgent deployment orchestration tarball.

        :param orchestration_type: The Orchestration Type of the orchestration deployment script. Use one of:
            - ansible
            - puppet \n
        :param version: The requested version of the OneAgent orchestration deployment tarball in 0.1.0.20200925-120822 format.
            If none is provided, the latest available is used.

        :returns Response: HTTP Response to the request. Can be written to file from the "content" attribute.
        """
        if version != "latest":
            version = "version/" + version
        return self.__http_client.make_request(path=f"{self.ENDPOINT_ORCHESTRATION}/{orchestration_type}/{version}/signature")


class ConnectionInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.tenant_uuid: str = raw_element["tenantUUID"]
        self.tenant_token: str = raw_element["tenantToken"]
        self.communication_endpoints: List[str] = raw_element.get("communicationEndpoints", [])
        self.formatted_communication_endpoints: str = raw_element["formattedCommunicationEndpoints"]


class InstallerMetaInfoDto(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.latest_agent_version: str = raw_element["latestAgentVersion"]


class AgentInstallerVersions(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.available_versions: List[str] = raw_element["availableVersions"]


class ActiveGateConnectionInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.tenant_uuid: str = raw_element["tenantUUID"]
        self.tenant_token: str = raw_element["tenantToken"]
        self.communication_endpoints: str = raw_element["communicationEndpoints"]


class ActiveGateInstallerVersions(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.available_versions: List[str] = raw_element["availableVersions"]


class BoshReleaseChecksum(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.sha_256: str = raw_element["sha256"]


class BoshReleaseAvailableVersions(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.available_versions: List[str] = raw_element["availableVersions"]


class LatestLambdaLayerNames(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.java: str = raw_element["java"]
        self.python: str = raw_element["python"]
        self.nodejs: str = raw_element["nodejs"]
