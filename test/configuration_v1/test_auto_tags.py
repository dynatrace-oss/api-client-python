from typing import List
from dynatrace import Dynatrace
from dynatrace.configuration_v1.auto_tags import (
    AutoTag,
    AutoTagRule,
    AutoTagRuleType,
    AutoTagShortRepresentation,
    ComparisonBasic,
    ComparisonBasicType,
    ConditionKey,
    ConditionKeyAttribute,
    EntityRuleEngineCondition,
)
from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.pagination import PaginatedList


def test_list(dt: Dynatrace):
    tags = dt.auto_tags.list()
    assert isinstance(tags, PaginatedList)

    for tag in tags:
        assert isinstance(tag, AutoTagShortRepresentation)
        assert tag.id == "403e033b-7324-4bfe-bef1-b3f367de42f2"
        assert tag.name == "frontend"
        break


def test_get(dt: Dynatrace):
    tags = dt.auto_tags.list()
    for tag in tags:
        print(tag.name)
        full_tag = tag.get_full_configuration()
        assert isinstance(full_tag, AutoTag)
        assert isinstance(full_tag.metadata, ConfigurationMetadata)
        assert full_tag.metadata.cluster_version == "1.214.112.20210409-064503"
        assert full_tag.id == "403e033b-7324-4bfe-bef1-b3f367de42f2"
        assert full_tag.name == "frontend"
        assert isinstance(full_tag.rules, List)
        for rule in full_tag.rules:
            print(rule)
            assert isinstance(rule, AutoTagRule)
            assert rule.type == AutoTagRuleType.SERVICE
            assert rule.enabled == True
            assert rule.value_format == ""
            assert rule.propagation_types == []
            assert isinstance(rule.conditions, List)
            for condition in rule.conditions:
                assert isinstance(condition, EntityRuleEngineCondition)
                assert isinstance(condition.key, ConditionKey)
                assert condition.key.attribute == ConditionKeyAttribute.PROCESS_GROUP_NAME
                assert isinstance(condition.comparison_info, ComparisonBasic)
                assert condition.comparison_info.type == ComparisonBasicType.STRING
                assert condition.comparison_info.operator == "CONTAINS"
                assert condition.comparison_info.value == "frontend"
                assert condition.comparison_info.negate == False
                assert condition.comparison_info.case_sensitive == False
                break
            break
        break
