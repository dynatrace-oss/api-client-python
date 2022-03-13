from typing import List
from dynatrace import Dynatrace
from dynatrace.configuration_v1.management_zones import (
    ManagementZone,
    ManagementZoneRule,
    ManagementZoneRuleType,
    ManagementZoneShortRepresentation,
    ComparisonBasic,
    ComparisonBasicType,
    ConditionKey,
    ConditionKeyAttribute,
    EntityRuleEngineCondition,
    PropagationType
)
from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.pagination import PaginatedList


def test_list(dt: Dynatrace):
    tags = dt.management_zones.list()
    assert isinstance(tags, PaginatedList)

    for tag in tags:
        assert isinstance(tag, ManagementZoneShortRepresentation)
        assert tag.id == "6507829326603756920"
        assert tag.name == "Frontend Services"
        break


def test_get(dt: Dynatrace):
    tags = dt.management_zones.list()
    for tag in tags:
        print(tag.name)
        full_tag = tag.get_full_configuration()
        assert isinstance(full_tag, ManagementZone)
        assert isinstance(full_tag.metadata, ConfigurationMetadata)
        assert full_tag.metadata.cluster_version == "1.237.130.20220311-144350"
        assert full_tag.id == "6507829326603756920"
        assert full_tag.name == "Frontend Services"
        assert isinstance(full_tag.rules, List)
        for rule in full_tag.rules:
            print(rule)
            assert isinstance(rule, ManagementZoneRule)
            assert rule.type == ManagementZoneRuleType.SERVICE
            assert rule.enabled == True
            assert rule.propagation_types == [PropagationType.SERVICE_TO_PROCESS_GROUP_LIKE]
            assert isinstance(rule.conditions, List)
            for condition in rule.conditions:
                assert isinstance(condition, EntityRuleEngineCondition)
                assert isinstance(condition.key, ConditionKey)
                assert condition.key.attribute == ConditionKeyAttribute.PROCESS_GROUP_CUSTOM_METADATA
                assert isinstance(condition.comparison_info, ComparisonBasic)
                assert condition.comparison_info.type == ComparisonBasicType.STRING
                assert condition.comparison_info.operator == "EQUALS"
                assert condition.comparison_info.value == "FRONTEND"
                assert condition.comparison_info.negate == False
                assert condition.comparison_info.case_sensitive == True
                break
            break
        break
