from datetime import datetime
from dynatrace import Dynatrace
from dynatrace.pagination import PaginatedList

import dynatrace.environment_v2.networkzones as nz

NETWORKZONE_ID = "default"

def test_list(dt: Dynatrace):
    network_zones = dt.network_zones.list()

    assert isinstance(network_zones, PaginatedList)
    assert all(isinstance(n , nz.NetworkZone) for n in network_zones)


def test_get(dt: Dynatrace):
    network_zone = dt.network_zones.get(networkzone_id=NETWORKZONE_ID)

    # type checks
    assert isinstance(network_zone, nz.NetworkZone)
    assert isinstance(network_zone.alternative_zones, list)