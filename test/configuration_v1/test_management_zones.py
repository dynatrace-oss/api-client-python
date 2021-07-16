from pprint import pprint
from dynatrace import Dynatrace

def test_get(dt: Dynatrace):
    mz = dt.management_zones.get()

    pprint(mz)
    print(type(mz.rules[0].conditions[0]))