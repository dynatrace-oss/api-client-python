from dynatrace import Dynatrace
from dynatrace.configuration_v1.oneagent_on_a_host import (
    HostConfig,
    HostAutoUpdateConfig,
    MonitoringConfig,
    AutoUpdateSetting,
    TechMonitoringList,
    EffectiveSetting,
    MonitoringMode,
)
from dynatrace.configuration_v1.schemas import UpdateWindowsConfig, UpdateWindow, ConfigurationMetadata, Technology, TechnologyType, SettingScope

HOST_ID = "HOST-abcd123457"
CLUSTER_VERSION = "1.222.47.20210712-162143"


def test_get(dt: Dynatrace):
    oa_host_config = dt.oneagents_config_host.get(HOST_ID)

    # type checks
    assert isinstance(oa_host_config, HostConfig)
    assert isinstance(oa_host_config.id, str)
    assert isinstance(oa_host_config.auto_update_config, HostAutoUpdateConfig)
    assert isinstance(oa_host_config.monitoring_config, MonitoringConfig)
    assert isinstance(oa_host_config.tech_monitoring_config_list, TechMonitoringList)

    # value checks
    assert oa_host_config.id == HOST_ID


def test_get_autoupdate(dt: Dynatrace):
    oa_autoupdate = dt.oneagents_config_host.get_autoupdate(HOST_ID)

    # type checks
    assert isinstance(oa_autoupdate, HostAutoUpdateConfig)
    assert isinstance(oa_autoupdate.id, str)
    assert isinstance(oa_autoupdate.setting, AutoUpdateSetting)
    assert isinstance(oa_autoupdate.version, (str, type(None)))
    assert isinstance(oa_autoupdate.effective_setting, EffectiveSetting)
    assert isinstance(oa_autoupdate.effective_version, (str, type(None)))
    assert isinstance(oa_autoupdate.update_windows, UpdateWindowsConfig)
    assert isinstance(oa_autoupdate.metadata, ConfigurationMetadata)
    assert all(isinstance(uw, UpdateWindow) for uw in oa_autoupdate.update_windows.windows)

    # value checks
    assert oa_autoupdate.id == HOST_ID
    assert oa_autoupdate.setting == AutoUpdateSetting.DISABLED
    assert oa_autoupdate.version is None
    assert oa_autoupdate.effective_setting == EffectiveSetting.DISABLED
    assert oa_autoupdate.effective_version is None
    assert oa_autoupdate.update_windows.windows == []
    assert oa_autoupdate.metadata.cluster_version == CLUSTER_VERSION


def test_get_monitoring(dt: Dynatrace):
    oa_monitoring = dt.oneagents_config_host.get_monitoring(HOST_ID)

    # type checks
    assert isinstance(oa_monitoring, MonitoringConfig)
    assert isinstance(oa_monitoring.id, str)
    assert isinstance(oa_monitoring.monitoring_enabled, bool)
    assert isinstance(oa_monitoring.monitoring_mode, MonitoringMode)
    assert isinstance(oa_monitoring.metadata, ConfigurationMetadata)

    # value checks
    assert oa_monitoring.id == HOST_ID
    assert oa_monitoring.monitoring_enabled == True
    assert oa_monitoring.monitoring_mode == MonitoringMode.FULL_STACK
    assert oa_monitoring.metadata.cluster_version == CLUSTER_VERSION


def test_get_technologies(dt: Dynatrace):
    oa_technologies = dt.oneagents_config_host.get_technologies(HOST_ID)

    # type checks
    assert isinstance(oa_technologies.metadata, ConfigurationMetadata)
    assert isinstance(oa_technologies, TechMonitoringList)
    assert all(isinstance(t, Technology) for t in oa_technologies.technologies)
    for tech in oa_technologies.technologies:
        assert isinstance(tech.type, TechnologyType)
        assert isinstance(tech.monitoring_enabled, bool)
        assert isinstance(tech.scope, (SettingScope, type(None)))

    # value checks
    assert len(oa_technologies.technologies) == 4
    assert oa_technologies.technologies[0].type == TechnologyType.LOG_ANALYTICS
    assert oa_technologies.technologies[0].monitoring_enabled == True
    assert oa_technologies.technologies[0].scope == SettingScope.ENVIRONMENT
    assert oa_technologies.metadata.cluster_version == CLUSTER_VERSION
