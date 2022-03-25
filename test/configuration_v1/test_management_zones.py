from typing import List
from dynatrace import Dynatrace
from dynatrace.configuration_v1.management_zones import (
    ManagementZone,
    ManagementZoneRule,
    ManagementZoneShortRepresentation,
    ComparisonBasic,
    ComparisonBasicType,
    ConditionKey,
    ConditionKeyAttribute,
    EntityRuleEngineCondition,
    PropagationType,
)
from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.pagination import PaginatedList
from dynatrace.configuration_v1.auto_tags import ConditionKeyAttribute, RuleType


def test_list(dt: Dynatrace):
    management_zones = dt.management_zones.list()
    assert isinstance(management_zones, PaginatedList)

    for management_zone in management_zones:
        assert isinstance(management_zone, ManagementZoneShortRepresentation)
        assert management_zone.id == "6507829326603756920"
        assert management_zone.name == "Frontend Services"
        break


def test_get(dt: Dynatrace):
    management_zones = dt.management_zones.list()
    for management_zone in management_zones:
        print(management_zone.name)
        full_management_zone = management_zone.get_full_configuration()
        assert isinstance(full_management_zone, ManagementZone)
        assert isinstance(full_management_zone.metadata, ConfigurationMetadata)
        assert full_management_zone.metadata.cluster_version == "1.237.130.20220311-144350"
        assert full_management_zone.id == "6507829326603756920"
        assert full_management_zone.name == "Frontend Services"
        assert isinstance(full_management_zone.rules, List)
        for rule in full_management_zone.rules:
            print(rule)
            assert isinstance(rule, ManagementZoneRule)
            assert rule.type == RuleType.SERVICE
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
