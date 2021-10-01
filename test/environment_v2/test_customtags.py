from datetime import datetime
from typing import List, Optional, Union, Dict, Any
from dynatrace import Dynatrace
from dynatrace.environment_v2.custom_tags import AddEntityTags, METag
from dynatrace.pagination import PaginatedList

import dynatrace.environment_v2.custom_tags as customtags

ENTITY_SELECTOR = "bilalhosts"


def test_list(dt: Dynatrace):
    _tags = dt.custom_tags.list(entity_selector=ENTITY_SELECTOR)

    # type checks
    assert isinstance(_tags, PaginatedList)
    assert len(list(_tags)) == 2
    assert all(isinstance(n, METag) for n in _tags)

    # value checks
    for t in _tags:
        assert t.key == "mainApp"
        assert t.string_representation == "mainApp"
        assert str(t.context) == "CONTEXTLESS"
        break


def test_post_no_value(dt: Dynatrace):
    tags = dt.custom_tags.post("entityId(CUSTOM_DEVICE-3B7788FE910B0F42)", [AddEntityTags("test-tag-no-value")])
    for tag in tags.applied_tags:
        assert str(tag.context) == "CONTEXTLESS"
        assert tag.key == "test-tag-no-value"
        assert tag.value is None
        assert tag.string_representation == "test-tag-no-value"


def test_post_value(dt: Dynatrace):
    tags = dt.custom_tags.post("entityId(CUSTOM_DEVICE-3B7788FE910B0F42)", [AddEntityTags("test-tag-value", "tag-value")])
    for tag in tags.applied_tags:
        assert str(tag.context) == "CONTEXTLESS"
        assert tag.key == "test-tag-value"
        assert tag.value == "tag-value"
        assert tag.string_representation == "test-tag-value:tag-value"


def test_delete(dt: Dynatrace):
    deleted_tags = dt.custom_tags.delete("test-tag-value", "entityId(CUSTOM_DEVICE-3B7788FE910B0F42)", delete_all_with_key=True)
    assert deleted_tags.matched_entities_count == 1
