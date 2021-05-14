from datetime import datetime

from dynatrace import Dynatrace
from dynatrace.configuration_v1.extensions import (
    ExtensionDto,
    ExtensionType,
    Extension,
    ExtensionProperty,
    GlobalExtensionConfiguration,
    ExtensionState,
    ExtensionStateEnum,
    ExtensionConfigurationDto,
)
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.pagination import PaginatedList


def test_list(dt: Dynatrace):
    extensions = dt.extensions.list()
    assert isinstance(extensions, PaginatedList)

    extensions_list = list(extensions)
    assert len(extensions_list) == 35
    first = extensions_list[0]

    assert isinstance(first, ExtensionDto)
    assert first.id == "custom.remote.python.certificates"
    assert first.name == "Certificates Plugin"
    assert first.type == ExtensionType.ACTIVEGATE


def test_get(dt: Dynatrace):
    extension = dt.extensions.get("custom.python.citrixAgent")
    assert isinstance(extension, Extension)
    assert extension.id == "custom.python.citrixAgent"
    assert extension.name == "Citrix Virtual Apps & Virtual Desktops"
    assert extension.version == "2.034"
    assert extension.type == ExtensionType.ONEAGENT
    assert extension.metric_group == "tech.Citrix"
    assert isinstance(extension.properties, list)

    first_property = extension.properties[0]
    assert isinstance(first_property, ExtensionProperty)
    assert first_property.key == "openkit_verify_certificates"
    assert first_property.type == "BOOLEAN"


def test_get_global_configuration(dt: Dynatrace):
    global_config = dt.extensions.get_global_configuration("custom.python.citrixAgent")
    assert isinstance(global_config, GlobalExtensionConfiguration)
    assert global_config.extension_id == "custom.python.citrixAgent"
    assert global_config.enabled
    assert not global_config.infraOnlyEnabled
    assert global_config.properties["log_level"] == "INFO"


def test_get_state(dt: Dynatrace):
    states = dt.extensions.list_states("custom.remote.python.salesforce_eventstream")
    assert isinstance(states, PaginatedList)

    list_states = list(states)
    assert isinstance(list_states, list)

    first = list_states[0]
    assert isinstance(first, ExtensionState)
    assert first.extension_id == "custom.remote.python.salesforce_eventstream"
    assert first.version == ""
    assert first.endpoint_id == "5649014104314746667"
    assert first.state == ExtensionStateEnum.ERROR_CONFIG
    assert first.state_description == "Extension doesn't exist on given host"
    assert first.timestamp == datetime.utcfromtimestamp(1620943873929 / 1000)
    assert first.host_id is None
    assert first.process_id is None


def test_get_instance_configuration(dt: Dynatrace):
    config = dt.extensions.get_instance_configuration("custom.remote.python.salesforce_eventstream", "5649014104314746667")
    assert isinstance(config, ExtensionConfigurationDto)

    # TODO - This is a bug on Dynatrace, watch for the fix, this is the configuration ID
    assert config.extension_id == "5649014104314746667"

    assert config.enabled
    assert config.active_gate.id == "-7885258652650793909"
    assert config.active_gate.name == "arch-david"
    assert config.endpoint_id == "5649014104314746667"
    assert config.endpoint_name == "curious-hawk"
    assert config.properties["openkit_application_id"] == "87eee414-9338-446b-988b-bbdbf495c4f4"


def test_list_activegate_extension_modules(dt: Dynatrace):
    modules = dt.extensions.list_activegate_extension_modules()
    assert isinstance(modules, PaginatedList)

    list_modules = list(modules)
    assert isinstance(list_modules, list)

    first = list_modules[0]
    assert isinstance(first, EntityShortRepresentation)
    assert first.id == "-7885258652650793909"
    assert first.name == "arch-david"
