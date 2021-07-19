from datetime import datetime
from dynatrace import Dynatrace
from dynatrace.configuration_v1.metag import METag
from dynatrace.pagination import PaginatedList

import dynatrace.environment_v2.custom_tags as customtags

ENTITY_SELECTOR = "bilalhosts"


def test_list(dt: Dynatrace):
    _tags = dt.custom_tags.list(entity_selector=ENTITY_SELECTOR)

    # type checks 
    assert isinstance(_tags, PaginatedList)
    assert len(list(_tags)) == 2
    assert all(isinstance(n , METag) for n in _tags)

    # value checks
    for t in _tags:
        assert t.key == "mainApp"
        assert t.string_representation == "mainApp"
        assert t.context == "CONTEXTLESS"

# def test_get(dt: Dynatrace):
#     network_zone = dt.network_zones.get(networkzone_id=NETWORKZONE_ID)

#     # type checks
#     assert isinstance(network_zone, nz.NetworkZone)
#     assert isinstance(network_zone.alternative_zones, list)

#     # value checks
#     assert network_zone.description == "The default network zone. This is the network zone for OneAgents or ActiveGates that do not have any network zone configured."
#     assert network_zone.id == "default"
#     assert network_zone.num_configured_activegates == 0
#     assert network_zone.num_oneagents_configured == 141
#     assert network_zone.num_oneagents_using == 141
#     assert network_zone.num_oneagents_from_other_zones == 0