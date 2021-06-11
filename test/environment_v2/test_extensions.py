from dynatrace import Dynatrace
from dynatrace.pagination import PaginatedList

import dynatrace.environment_v2.extensions as extensionsv2

def test_list(dt: Dynatrace):
    extensions_list = dt.extensionsv2.list()
    e_list = list(extensions_list)

    # type checks 
    assert isinstance(extensions_list, PaginatedList)
    assert len(e_list) == 2
    assert all(isinstance(n , extensions.MinimalExtension) for n in extensions_list)

    # value checks
    for elt in e_list:
        assert elt.extension_name == "ibmmq"
        assert elt.version == "1.2.3"
        break

def test_get(dt: Dynatrace):
    e_name = "ibmmq"
    e_version = "2.1.3"
    extension = dt.extensionsv2.get(e_name, e_version)

    # type checks
    assert isinstance(extension, extensionsv2.Extension)
    assert isinstance(extension.author, extensionsv2.AuthorDTO)
    assert isinstance(extension.data_sources, list)
    assert isinstance(extension.feature_sets, list)
    assert isinstance(extension.variables, list)

    # value checks
    assert extension.extension_name == "ibmmq"
    assert extension.author.name == "Bilal Hashmi"
    assert extension.version == "2.1.3"
    assert extension.feature_sets[0] == "coolFeatures"


def test_get_active_extension_version(dt: Dynatrace):
    e_name = "ibmmq"

    elt = dt.extensionsv2.getActiveExtensionVersion(e_name)

    # type checks
    assert isinstance(elt, extensionsv2.ExtensionEnvironmentConfigurationVersion)

    # value checks
    assert elt.version == "1.2.3"