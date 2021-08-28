from dynatrace import Dynatrace
from dynatrace.environment_v1.deployment import (
    InstallerMetaInfoDto,
    ConnectionInfo,
    AgentInstallerVersions,
    BoshReleaseAvailableVersions,
    ActiveGateInstallerVersions,
    ActiveGateConnectionInfo,
    BoshReleaseChecksum,
    LatestLambdaLayerNames,
)


VERSION = "1.215.159.20210428-145534"


def test_get_agent_installer_latest_metainfo(dt: Dynatrace):
    metainfo = dt.deployment.get_agent_installer_latest_metainfo(os_type="unix", installer_type="paas", flavor="musl", arch="x86", bitness="64")

    # type checks
    assert isinstance(metainfo, InstallerMetaInfoDto)
    assert isinstance(metainfo.latest_agent_version, str)

    # value checks
    assert metainfo.latest_agent_version == VERSION


def test_get_agent_installer_connection_info(dt: Dynatrace):
    info = dt.deployment.get_agent_installer_connection_info(version=VERSION)

    # type checks
    assert isinstance(info, ConnectionInfo)
    assert isinstance(info.tenant_uuid, str)
    assert isinstance(info.tenant_token, str)
    assert isinstance(info.communication_endpoints, list)
    assert all(isinstance(ce, str) for ce in info.communication_endpoints)
    assert isinstance(info.formatted_communication_endpoints, str)

    # value checks
    assert info.tenant_uuid == "abc12345"
    assert info.tenant_token == "4BcD3fGh1JkLmN0p"
    assert len(info.communication_endpoints) == 4
    assert info.communication_endpoints[0] == "https://host.docker.internal:9999/communication"
    assert info.formatted_communication_endpoints.startswith("{https://host.docker.internal:9999/communication")


def test_list_agent_installer_versions(dt: Dynatrace):
    versions = dt.deployment.list_agent_installer_versions(os_type="unix", installer_type="paas", flavor="musl", arch="x86")

    # type checks
    assert isinstance(versions, AgentInstallerVersions)
    assert isinstance(versions.available_versions, list)
    assert all(isinstance(av, str) for av in versions.available_versions)

    # value checks
    assert len(versions.available_versions) == 6
    assert versions.available_versions[0] == VERSION


def test_get_gateway_installer_connection_info(dt: Dynatrace):
    info = dt.deployment.get_gateway_installer_connection_info()

    # type checks
    assert isinstance(info, ActiveGateConnectionInfo)
    assert isinstance(info.tenant_token, str)
    assert isinstance(info.tenant_uuid, str)
    assert isinstance(info.communication_endpoints, str)

    # value checks
    assert info.tenant_uuid == "abc12345"
    assert info.tenant_token == "4BcD3fGh1JkLmN0p"
    assert info.communication_endpoints.startswith("https://sg-eu-west-1234.domain.com")


def test_list_gateway_installer_versions(dt: Dynatrace):
    versions = dt.deployment.list_gateway_installer_versions(os_type="unix")

    # type checks
    assert isinstance(versions, ActiveGateInstallerVersions)
    assert isinstance(versions.available_versions, list)
    assert all(isinstance(av, str) for av in versions.available_versions)

    # value checks
    assert len(versions.available_versions) == 6
    assert versions.available_versions[0] == VERSION


def test_list_boshrelease_agent_versions(dt: Dynatrace):
    versions = dt.deployment.list_boshrelease_agent_versions(os_type="unix")

    # type checks
    assert isinstance(versions, BoshReleaseAvailableVersions)
    assert isinstance(versions.available_versions, list)
    assert all(isinstance(av, str) for av in versions.available_versions)

    # value checks
    assert len(versions.available_versions) == 6
    assert versions.available_versions[0] == VERSION


def test_get_boshrelease_agent_checksum(dt: Dynatrace):
    checksum = dt.deployment.get_boshrelease_agent_checksum(os_type="unix", version=VERSION)

    # type checks
    assert isinstance(checksum, BoshReleaseChecksum)
    assert isinstance(checksum.sha_256, str)

    # value checks
    assert checksum.sha_256 == "8747793999922D34666A26F48C2061E598B164159015D12103A5D55A4F05225C"


def test_get_lambda_agent_versions(dt: Dynatrace):
    versions = dt.deployment.get_lambda_agent_versions()

    # type checks
    assert isinstance(versions, LatestLambdaLayerNames)
    assert isinstance(versions.java, str)
    assert isinstance(versions.nodejs, str)
    assert isinstance(versions.python, str)

    # value checks
    assert versions.java == "Dynatrace_OneAgent_1_221_103_20210713-172057"
    assert versions.python == "Dynatrace_OneAgent_1_221_3_20210624-164237"
    assert versions.nodejs == "Dynatrace_OneAgent_1_221_1_20210618-040655"
