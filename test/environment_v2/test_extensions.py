from dynatrace import Dynatrace
from dynatrace.environment_v2.extensions import MinimalExtension
from dynatrace.pagination import PaginatedList

import dynatrace.environment_v2.extensions as extensions_v2


def test_list(dt: Dynatrace):
    extensions = list(dt.extensions_v2.list())

    assert len(extensions) == 2

    for extension in extensions:
        assert isinstance(extension, MinimalExtension)
        assert extension.extension_name == "com.dynatrace.extension.snmp-generic"
        assert extension.version == "0.2.5"
        break


def test_list_name(dt: Dynatrace):
    extensions = list(dt.extensions_v2.list(name="custom"))

    assert len(extensions) == 1

    for extension in extensions:
        assert isinstance(extension, MinimalExtension)
        assert extension.extension_name == "custom:dynatrace.cisco.asa"
        assert extension.version == "0.1.0"
        break


def test_list_versions(dt: Dynatrace):
    extensions = list(dt.extensions_v2.list_versions("com.dynatrace.extension.snmp-generic"))

    assert len(extensions) == 1

    for extension in extensions:
        assert isinstance(extension, MinimalExtension)
        assert extension.extension_name == "com.dynatrace.extension.snmp-generic"
        assert extension.version == "0.2.5"
        break


def test_get(dt: Dynatrace):
    extension = dt.extensions_v2.get("com.dynatrace.extension.snmp-generic", "0.2.5")

    # type checks
    assert isinstance(extension, extensions_v2.Extension)
    assert isinstance(extension.author, extensions_v2.AuthorDTO)
    assert isinstance(extension.data_sources, list)
    assert isinstance(extension.feature_sets, list)
    assert isinstance(extension.variables, list)

    # value checks
    assert extension.extension_name == "com.dynatrace.extension.snmp-generic"
    assert extension.author.name == "Dynatrace"
    assert extension.version == "0.2.5"
    assert extension.variables[0] == "ext.activationtag"


def test_get_active_extension_version(dt: Dynatrace):
    environemnt_config = dt.extensions_v2.get_environment_config("ibmmq")

    # type checks
    assert isinstance(environemnt_config, extensions_v2.ExtensionEnvironmentConfigurationVersion)

    # value checks
    assert environemnt_config.version == "1.2.3"
