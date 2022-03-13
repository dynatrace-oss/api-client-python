"""
Copyright 2021 Dynatrace LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dynatrace import http_client

from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.configuration_v1.dt_enums import (
    ComparisonBasicType,
    ConditionKeyAttribute,
    ConditionKeyType,
    PropagationType,
    RuleType,
)


class AutoTagService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self, page_size: int = 200) -> PaginatedList["AutoTagShortRepresentation"]:
        """
        List all auto tag rules.

        :param page_size: The number of results per result page. Must be between 1 and 500
            Default value : 200
        """
        params = {"pageSize": page_size}
        return PaginatedList(AutoTagShortRepresentation, self.__http_client, f"/api/config/v1/autoTags", params, list_item="values")


class ComparisonBasic(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.operator: str = raw_element.get("operator")
        self.value: dict = raw_element.get("value")
        self.negate: bool = raw_element.get("negate")
        self.type: ComparisonBasicType = ComparisonBasicType(
            raw_element.get("type"))
        self.case_sensitive: bool = raw_element.get("caseSensitive")


class ConditionKey(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.attribute: ConditionKeyAttribute = ConditionKeyAttribute(
            raw_element.get("attribute"))
        self.type: ConditionKeyType = ConditionKeyType(raw_element.get("type"))


class EntityRuleEngineCondition(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.key: ConditionKey = ConditionKey(
            raw_element=raw_element.get("key"))
        self.comparison_info: ComparisonBasic = ComparisonBasic(
            raw_element=raw_element.get("comparisonInfo"))


class EntitySelectorBasedAutoTagRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: bool = raw_element.get("enabled")
        self.entity_selector: str = raw_element.get("entitySelector")
        self.value_format: str = raw_element.get("valueFormat")


class AutoTagRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: RuleType = RuleType(raw_element.get("type"))
        self.enabled: bool = raw_element.get("enabled")
        self.value_format: str = raw_element.get("valueFormat")
        self.propagation_types: List[PropagationType] = [PropagationType(
            prop_type) for prop_type in (raw_element.get("propagationTypes") or [])]
        self.conditions: List[EntityRuleEngineCondition] = [
            EntityRuleEngineCondition(raw_element=condition) for condition in (raw_element.get("conditions") or [])
        ]


class AutoTag(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(
            self._http_client, None, raw_element.get("metadata"))
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")
        self.rules: List[AutoTagRule] = [AutoTagRule(
            raw_element=rule) for rule in raw_element.get("rules")]
        self.entity_selector_based_rules: List[EntitySelectorBasedAutoTagRule] = [
            EntitySelectorBasedAutoTagRule(raw_element=rule) for rule in (raw_element.get("entitySelectorBasedRules") or [])
        ]


class AutoTagShortRepresentation(EntityShortRepresentation):
    def get_full_configuration(self):
        """
        Get the full configuration for this auto tag rule short representation.
        """
        response = self._http_client.make_request(
            f"/api/config/v1/autoTags/{self.id}").json()
        return AutoTag(http_client=self._http_client, raw_element=response)
