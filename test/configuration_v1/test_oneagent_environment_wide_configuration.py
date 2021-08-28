from dynatrace import Dynatrace
from dynatrace.configuration_v1.oneagent_environment_wide_configuration import EnvironmentAutoUpdateConfig
from dynatrace.configuration_v1.schemas import (
    ConfigurationMetadata,
    AutoUpdateSetting,
    UpdateWindowsConfig,
    TechMonitoringList,
    Technology,
    TechnologyType,
    SettingScope,
)

CLUSTER_VERSION = "1.222.47.20210712-162143"


def test_get(dt: Dynatrace):
    oa_env_autoupdate_config = dt.oneagents_config_environment.get()

    # type checks
    assert isinstance(oa_env_autoupdate_config, EnvironmentAutoUpdateConfig)
    assert isinstance(oa_env_autoupdate_config.metadata, ConfigurationMetadata)
    assert isinstance(oa_env_autoupdate_config.setting, AutoUpdateSetting)
    assert isinstance(oa_env_autoupdate_config.version, (str, type(None)))
    assert isinstance(oa_env_autoupdate_config.update_windows, UpdateWindowsConfig)

    # value checks
    assert oa_env_autoupdate_config.metadata.cluster_version == CLUSTER_VERSION
    assert oa_env_autoupdate_config.setting == AutoUpdateSetting.DISABLED
    assert oa_env_autoupdate_config.version is None
    assert oa_env_autoupdate_config.update_windows.windows == []


def test_get_technologies(dt: Dynatrace):
    oa_env_technologies = dt.oneagents_config_environment.get_technologies()

    # type checks
    assert isinstance(oa_env_technologies, TechMonitoringList)
    assert isinstance(oa_env_technologies.metadata, ConfigurationMetadata)
    assert all(isinstance(t, Technology) for t in oa_env_technologies.technologies)
    for tech in oa_env_technologies.technologies:
        assert isinstance(tech.type, TechnologyType)
        assert isinstance(tech.monitoring_enabled, bool)
        assert isinstance(tech.scope, (SettingScope, type(None)))

    # value checks
    assert oa_env_technologies.metadata.cluster_version == CLUSTER_VERSION
    assert len(oa_env_technologies.technologies) == 4
    assert oa_env_technologies.technologies[0].type == TechnologyType.DOT_NET
    assert oa_env_technologies.technologies[0].monitoring_enabled == True
    assert oa_env_technologies.technologies[0].scope == SettingScope.ENVIRONMENT
