from dynatrace import Dynatrace
from dynatrace.environment_v1.smartscape_hosts import Host, MonitoringMode, OSArchitecture
from dynatrace.pagination import HeaderPaginatedList
from dynatrace.environment_v1.smartscape_hosts import Host


def test_list(dt: Dynatrace):
    hosts = dt.smartscape_hosts.list(page_size=20)
    assert isinstance(hosts, HeaderPaginatedList)
    for host in hosts:
        assert isinstance(host, Host)
        assert host.entity_id == "HOST-7EC661999923A6B9"
        assert host.discovered_name == "TAG009444368559.clients.example.com"
        assert host.last_seen_timestamp == 1621519976487
        for tag in host.tags:
            assert tag.context == "CONTEXTLESS"
            assert tag.key == "APP1234567"
            break
        assert host.os_version == "Windows 10 Enterprise 20H2 2009, ver. 10.0.19042"
        assert host.monitoring_mode == MonitoringMode.FULL_STACK
        assert host.consumed_host_units == 2.0
        assert host.os_architecture == OSArchitecture.X_EIGHTY_SIX
        assert host.cpu_cores == 8
        break
