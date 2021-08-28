from dynatrace import Dynatrace
from dynatrace.configuration_v1.oneagent_in_a_hostgroup import OneAgentHostGroupConfig, HostGroupAutoUpdateConfig
from dynatrace.configuration_v1.schemas import UpdateWindowsConfig, UpdateWindow, ConfigurationMetadata, EffectiveSetting, AutoUpdateSetting

HOST_GROUP_ID = "HOST_GROUP-ABC123DEF456GHI7"
CLUSTER_VERSION = "1.222.47.20210712-162143"


def test_get(dt: Dynatrace):
    oa_hostgroup_config = dt.oneagents_config_hostgroup.get(HOST_GROUP_ID)

    # type checks
    assert isinstance(oa_hostgroup_config, OneAgentHostGroupConfig)
    assert isinstance(oa_hostgroup_config.id, (str, type(None)))
    assert isinstance(oa_hostgroup_config.auto_update_config, HostGroupAutoUpdateConfig)

    # value checks
    assert oa_hostgroup_config.id == None


def test_get_audoupdate(dt: Dynatrace):
    oa_hostgroup_autoupdate = dt.oneagents_config_hostgroup.get_autoupdate(HOST_GROUP_ID)

    # type checks
    assert isinstance(oa_hostgroup_autoupdate, HostGroupAutoUpdateConfig)
    assert isinstance(oa_hostgroup_autoupdate.id, str)
    assert isinstance(oa_hostgroup_autoupdate.metadata, ConfigurationMetadata)
    assert isinstance(oa_hostgroup_autoupdate.setting, AutoUpdateSetting)
    assert isinstance(oa_hostgroup_autoupdate.update_windows, UpdateWindowsConfig)
    assert isinstance(oa_hostgroup_autoupdate.effective_setting, (EffectiveSetting, type(None)))
    assert isinstance(oa_hostgroup_autoupdate.version, (str, type(None)))
    assert isinstance(oa_hostgroup_autoupdate.effective_version, (str, type(None)))

    # value checks
    assert oa_hostgroup_autoupdate.metadata.cluster_version == CLUSTER_VERSION
    assert oa_hostgroup_autoupdate.id == HOST_GROUP_ID
    assert oa_hostgroup_autoupdate.setting == AutoUpdateSetting.DISABLED
    assert oa_hostgroup_autoupdate.version is None
    assert oa_hostgroup_autoupdate.update_windows.windows == []
    assert oa_hostgroup_autoupdate.effective_setting == EffectiveSetting.DISABLED
    assert oa_hostgroup_autoupdate.effective_version is None
