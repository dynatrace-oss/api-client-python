from datetime import datetime
from typing import List, Optional, Union, Dict, Any
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