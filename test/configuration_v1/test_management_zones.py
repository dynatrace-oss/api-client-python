from dynatrace import Dynatrace
from dynatrace.configuration_v1.management_zones import (
    ManagementZoneStub,
    MzRule,
    EntitySelectorBasedMzRule,
    EntityRuleEngineCondition,
    PropagationType,
    MzDimensionalRule,
    ConditionKey,
    MzConditionAttribute,
    MzConditionType,
)
from dynatrace.configuration_v1.schemas import (
    ConfigurationMetadata,
    ComparisonBasic,
    ComparisonBasicType,
    ServiceTypeComparison,
    ServiceTypeComparisonValue,
    BasicComparisonOperator,
    ServiceTopologyComparisonValue,
    PredefinedProcessMetadataKeySource,
    StringComparisonOperator,
)

ID = "1234567890987654321"
NAME = "Test-Management-Zone"


def test_list(dt: Dynatrace):
    mz_stubs = dt.management_zones.list()

    # type checks
    assert isinstance(mz_stubs, list)
    assert all(isinstance(stub, ManagementZoneStub) for stub in mz_stubs)
    assert all(isinstance(stub.name, str) for stub in mz_stubs)
    assert all(isinstance(stub.id, str) for stub in mz_stubs)

    # value checks
    assert len(mz_stubs) == 3
    assert mz_stubs[0].id == ID
    assert mz_stubs[0].name == NAME


def test_get(dt: Dynatrace):
    mz = dt.management_zones.get(mz_id=ID)

    # type checks
    assert isinstance(mz.id, str)
    assert isinstance(mz.name, str)
    assert isinstance(mz.metadata, ConfigurationMetadata)
    assert isinstance(mz.description, str)
    assert isinstance(mz.rules, list)
    assert all(isinstance(rule, MzRule) for rule in mz.rules)
    for rule in mz.rules:
        assert isinstance(rule.type, str)
        assert isinstance(rule.enabled, bool)
        assert isinstance(rule.propagation_types, list)
        assert all(isinstance(pt, PropagationType) for pt in rule.propagation_types)
        assert isinstance(rule.conditions, list)
        assert all(isinstance(condition, EntityRuleEngineCondition) for condition in rule.conditions)
        for condition in rule.conditions:
            assert isinstance(condition.key, ConditionKey)
            assert isinstance(condition.comparison_info, ComparisonBasic)
    assert isinstance(mz.rules[0].conditions[0].comparison_info, ServiceTypeComparison)
    assert isinstance(mz.dimensional_rules, list)
    assert all(isinstance(rule, MzDimensionalRule) for rule in mz.dimensional_rules)
    assert isinstance(mz.entity_selector_based_rules, list)
    assert all(isinstance(rule, EntitySelectorBasedMzRule) for rule in mz.entity_selector_based_rules)
    for rule in mz.entity_selector_based_rules:
        assert isinstance(rule.enabled, bool)
        assert isinstance(rule.entity_selector, str)

    # value checks
    assert mz.id == ID
    assert mz.name == NAME
    assert mz.description == "All sorts of rules for testing"
    rule = mz.rules[0]
    assert rule.type == "SERVICE"
    assert rule.enabled == True
    assert rule.propagation_types == []
    condition = rule.conditions[0]
    assert condition.key.attribute == MzConditionAttribute.SERVICE_TYPE
    assert condition.key.type == MzConditionType.STATIC
    assert condition.comparison_info.type == ComparisonBasicType.SERVICE_TYPE
    assert condition.comparison_info.operator == BasicComparisonOperator.EQUALS
    assert condition.comparison_info.value == ServiceTypeComparisonValue.CUSTOM_SERVICE
    assert condition.comparison_info.negate == False
    rule = mz.rules[2]
    assert rule.type == "SERVICE"
    assert rule.enabled == True
    assert rule.propagation_types[0] == PropagationType.SERVICE_TO_HOST_LIKE
    assert rule.propagation_types[1] == PropagationType.SERVICE_TO_PROCESS_GROUP_LIKE
    condition = rule.conditions[0]
    assert condition.key.attribute == MzConditionAttribute.SERVICE_TOPOLOGY
    assert condition.key.type == MzConditionType.STATIC
    assert condition.comparison_info.type == ComparisonBasicType.SERVICE_TOPOLOGY
    assert condition.comparison_info.operator == BasicComparisonOperator.EQUALS
    assert condition.comparison_info.value == ServiceTopologyComparisonValue.FULLY_MONITORED
    assert condition.comparison_info.negate == False
    condition = rule.conditions[1]
    assert condition.key.attribute == MzConditionAttribute.PROCESS_GROUP_PREDEFINED_METADATA
    assert condition.key.type == MzConditionType.PROCESS_PREDEFINED_METADATA_KEY
    assert condition.key.dynamic_key == PredefinedProcessMetadataKeySource.EQUINOX_CONFIG_PATH
    assert condition.comparison_info.type == ComparisonBasicType.STRING
    assert condition.comparison_info.operator == StringComparisonOperator.CONTAINS
    assert condition.comparison_info.value == "something"
    assert condition.comparison_info.negate == True
    assert condition.comparison_info.case_sensitive == True
