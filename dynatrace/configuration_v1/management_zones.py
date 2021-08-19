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
from enum import Enum
from requests import Response
from typing import Dict, Any, List, Optional, Union

from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation, EntityStub
from dynatrace.environment_v2.schemas import ConfigurationMetadata


class ManagementZoneService:
    ENDPOINT = "/api/config/v1/managementZones"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> "List[ManagementZoneStub]":
        """Lists all configured management zones.
        Management Zones are returned as short representations (id, name, and optional description).

        :returns: list of configured management zones
        """
        response = self.__http_client.make_request(path=self.ENDPOINT)
        return [ManagementZoneStub(raw_element=value, http_client=self.__http_client) for value in response.json().get("values", [])]

    def get(self, mz_id: str, include_process_group_references: bool = False) -> "ManagementZone":
        """Gets the details of the specified management zone.

        :param mz_id: The ID of the required management zone.
        :param include_process_group_references: Flag to include process group references to the response.
            Process group references aren't compatible across environments. When this flag is set to false,
            conditions with process group references will be removed. If that leads to a rule having no conditions,
            the entire rule will be removed.

        :returns: the details of the requested management zone
        """
        params = {"includeProcessGroupReferences": include_process_group_references}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{mz_id}", params=params)

        return ManagementZone(raw_element=response.json(), http_client=self.__http_client)

    def post(self, management_zone: "ManagementZone") -> "EntityShortRepresentation":
        """Create the given Management Zone configuration in Dynatrace (POST).

        :param management_zone: the Management Zone configuration details

        :returns EntityShortRepresentation: basic details of the created Management Zone
        """
        if not management_zone._http_client:
            management_zone._http_client = self.__http_client
        return management_zone.post()

    def put(self, management_zone: "ManagementZone") -> "Response":
        """Update the specified Management Zone in Dynatrace (PUT).
        If the ID does not exist in Dynatrace, a new Management Zone is created with the given ID.

        :param management_zone: the Management Zone configuration details

        :returns Response: HTTP Response to the request. Will contain basic details in JSON body if configuration is created.
        """
        if not management_zone._http_client:
            management_zone._http_client = self.__http_client
        return management_zone.put()

    def delete(self, mz_id: str) -> "Response":
        """Deletes the specified management zone.

        :param mz_id: The ID of the management zone to delete.

        :returns Response: HTTP Response for the request.
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{mz_id}", method="DELETE")


class ManagementZoneStub(EntityShortRepresentation):
    def get_details(self) -> "ManagementZone":
        """Gets the full details of this Management Zone configuration.

        :returns Management Zone: the Management Zone configuration

        :throws ValueError: operation cannot be executed due to missing HTTP Client
        """
        if not self._http_client:
            raise ValueError("Object does not have an HTTP Client implemented.")
        response = self._http_client.make_request(path=f"{ManagementZoneService.ENDPOINT}/{self.id}")
        return ManagementZone(raw_element=response.json(), http_client=self._http_client)


class ManagementZone(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.name: str = raw_element["name"]
        self.id: Optional[str] = raw_element.get("id")
        self.metadata: Optional[ConfigurationMetadata] = ConfigurationMetadata(raw_element=raw_element.get("metadata"))
        self.description: Optional[str] = raw_element.get("description")
        self.rules: Optional[List[MzRule]] = [MzRule(raw_element=rule) for rule in raw_element.get("rules", [])]
        self.dimensional_rules: Optional[List[MzDimensionalRule]] = [MzDimensionalRule(raw_element=rule) for rule in raw_element.get("dimensionalRules", [])]
        self.entity_selector_based_rules: Optional[List[EntitySelectorBasedMzRule]] = [
            EntitySelectorBasedMzRule(raw_element=rule) for rule in raw_element.get("entitySelectorBasedRules", [])
        ]

    def to_json(self) -> Dict[str, Any]:
        """Converts Management Zone details to JSON dictionary.

        :returns Dict[str, Any]: dictionary representing the Management Zone
        """
        details = {"name": self.name, "description": self.description}
        if self.rules:
            details["rules"] = [rule.to_json() for rule in self.rules]
        if self.dimensional_rules:
            details["dimensionalRules"] = [rule.to_json() for rule in self.dimensional_rules]
        if self.entity_selector_based_rules:
            details["entitySelectorBasedRules"] = [rule.to_json() for rule in self.entity_selector_based_rules]

        return details

    def post(self) -> "EntityShortRepresentation":
        """Creates this Management Zone in Dynatrace (POST).

        :returns EntityShortRepresentation: basic detail of the created Management Zone

        :throws ValueError: if operation cannot be executed due to missing HTTP Client
        """
        if not self._http_client:
            raise ValueError("Object does not have HTTP Client. Use management_zones.post() instead.")
        response = self._http_client.make_request(path=ManagementZoneService.ENDPOINT, params=self.to_json(), method="POST")
        self.id = response.json().get("id")

        return EntityShortRepresentation(raw_element=response.json())

    def put(self) -> "Response":
        """Updates this Management Zone in Dynatrace (PUT).
        If the ID does not exist in Dynatrace, a new Management Zone is created with the given ID.

        :returns Response: HTTP Response to the request. Will contain basic details in JSON body if configuration is created.

        :throws ValueError: if operation cannot be executed due to missing HTTP Client
        """
        if not self._http_client:
            raise ValueError("Object does not have HTTP Client. Use management_zones.put() instead.")
        response = self._http_client.make_request(path=f"{ManagementZoneService.ENDPOINT}/{self.id}", params=self.to_json(), method="PUT")
        if response.status_code == 201:
            self.id = response.json().get("id")

        return response


class MzRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: str = raw_element["type"]
        self.enabled: bool = raw_element["enabled"]
        self.conditions: List[EntityRuleEngineCondition] = [EntityRuleEngineCondition(raw_element=condition) for condition in raw_element.get("conditions", [])]
        self.propagation_types: Optional[List[PropagationType]] = [PropagationType(pt) for pt in raw_element.get("propagationTypes", [])]

    def to_json(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "enabled": self.enabled,
            "conditions": [condition.to_json() for condition in self.conditions],
            "propagationTypes": [str(pt) for pt in self.propagation_types] if self.propagation_types else None,
        }


class MzDimensionalRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: bool = raw_element["enabled"]
        self.applies_to: MzDimensionalRuleAppliesTo = MzDimensionalRuleAppliesTo(raw_element["appliesTo"])
        self.conditions: List[MzDimensionalRuleCondition] = [MzDimensionalRuleCondition(raw_element=condition) for condition in raw_element["conditions"]]

    def to_json(self) -> Dict[str, Any]:
        return {"enabled": self.enabled, "appliesTo": str(self.applies_to), "conditions": [condition.to_json() for condition in self.conditions]}


class EntitySelectorBasedMzRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: Optional[bool] = raw_element.get("enabled")
        self.entity_selector: str = raw_element["entitySelector"]

    def to_json(self) -> Dict[str, Any]:
        return {"enabled": self.enabled, "entitySelector": self.entity_selector}


class MzDimensionalRuleCondition(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.condition_type: MzDimensionalRuleConditionType = MzDimensionalRuleConditionType(raw_element["conditionType"])
        self.rule_matcher: MzDimensionalRuleMatcher = MzDimensionalRuleMatcher(raw_element["ruleMatcher"])
        self.key: str = raw_element["key"]
        self.value: Optional[str] = raw_element.get("value")

    def to_json(self) -> Dict[str, Any]:
        return {"conditionType": str(self.condition_type), "ruleMatcher": str(self.rule_matcher), "key": self.key, "value": self.value}


class EntityRuleEngineCondition(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        condition_key_types = {
            MzConditionType.HOST_CUSTOM_METADATA_KEY: CustomHostMetadataConditionKey,
            MzConditionType.PROCESS_CUSTOM_METADATA_KEY: CustomProcessMetadataConditionKey,
            MzConditionType.PROCESS_PREDEFINED_METADATA_KEY: ProcessMetadataConditionKey,
            MzConditionType.STRING: StringConditionKey,
            MzConditionType.STATIC: ConditionKey,
        }
        comparison_types = {
            ComparisonBasicType.APPLICATION_TYPE: ApplicationTypeComparison,
            ComparisonBasicType.AZURE_COMPUTE_MODE: AzureComputeModeComparison,
            ComparisonBasicType.AZURE_SKU: AzureSkuComparison,
            ComparisonBasicType.BITNESS: BitnessComparison,
            ComparisonBasicType.CLOUD_TYPE: CloudTypeComparison,
            ComparisonBasicType.CUSTOM_APPLICATION_TYPE: CustomApplicationTypeComparison,
            ComparisonBasicType.DATABASE_TOPOLOGY: DatabaseTopologyComparison,
            ComparisonBasicType.DCRUM_DECODER_TYPE: DcrumDecoderComparison,
            ComparisonBasicType.ENTITY_ID: EntityIdComparison,
            ComparisonBasicType.HYPERVISOR_TYPE: HypervisorTypeComparison,
            ComparisonBasicType.INDEXED_NAME: IndexedNameComparison,
            ComparisonBasicType.INDEXED_STRING: IndexedStringComparison,
            ComparisonBasicType.INDEXED_TAG: IndexedTagComparison,
            ComparisonBasicType.INTEGER: IntegerComparison,
            ComparisonBasicType.IP_ADDRESS: IpAddressComparison,
            ComparisonBasicType.MOBILE_PLATFORM: MobilePlatformComparison,
            ComparisonBasicType.OS_ARCHITECTURE: OsArchitectureComparison,
            ComparisonBasicType.OS_TYPE: OsTypeComparison,
            ComparisonBasicType.PAAS_TYPE: PaasTypeComparison,
            ComparisonBasicType.SERVICE_TOPOLOGY: ServiceTopologyComparison,
            ComparisonBasicType.SERVICE_TYPE: ServiceTypeComparison,
            ComparisonBasicType.SIMPLE_HOST_TECH: SimpleHostTechComparison,
            ComparisonBasicType.SIMPLE_TECH: SimpleTechComparison,
            ComparisonBasicType.STRING: StringComparison,
            ComparisonBasicType.SYNTHETIC_ENGINE_TYPE: SyntheticEngineTypeComparison,
            ComparisonBasicType.TAG: TagComparison,
        }

        self.key: ConditionKey = condition_key_types[MzConditionType(raw_element["key"]["type"])](raw_element=raw_element["key"])
        self.comparison_info: ComparisonBasic = comparison_types[ComparisonBasicType(raw_element["comparisonInfo"]["type"])](
            raw_element=raw_element["comparisonInfo"]
        )

    def to_json(self) -> Dict[str, Any]:
        return {"key": self.key.to_json(), "comparisonInfo": self.comparison_info.to_json()}


class ConditionKey(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.attribute: MzConditionAttribute = MzConditionAttribute(raw_element["attribute"])
        self.type: MzConditionType = MzConditionType(raw_element["type"])

    def to_json(self) -> Dict[str, Any]:
        return {"attribute": str(self.attribute), "type": str(self.type)}


class SimpleTech(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: Optional[SimpleTechType] = SimpleTechType(raw_element["type"]) if raw_element.get("type") else None
        self.verbatim_type: Optional[str] = raw_element.get("verbatimType")

    def to_json(self) -> Dict[str, Any]:
        return {"type": str(self.type) if self.type else None, "verbatimType": self.verbatim_type}


class SimpleHostTech(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: Optional[SimpleHostTechType] = SimpleHostTechType(raw_element["type"]) if raw_element.get("type") else None
        self.verbatim_type: Optional[str] = raw_element.get("verbatimType")

    def to_json(self) -> Dict[str, Any]:
        return {"type": str(self.type) if self.type else None, "verbatimType": self.verbatim_type}


class TagInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.context: str = raw_element["context"]
        self.key: str = raw_element["key"]
        self.value: Optional[str] = raw_element.get("value")

    def to_json(self) -> Dict[str, Any]:
        return {"context": self.context, "key": self.key, "value": self.value}


class CustomProcessMetadataKey(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.source: CustomProcessMetadataKeySource = CustomProcessMetadataKeySource(raw_element["source"])
        self.key: str = raw_element["key"]

    def to_json(self) -> Dict[str, Any]:
        return {"source": str(self.source), "key": self.key}


class CustomHostMetadataKey(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.source: HostMetadataKeySource = HostMetadataKeySource(raw_element["source"])
        self.key: str = raw_element["key"]

    def to_json(self) -> Dict[str, Any]:
        return {"source": str(self.source), "key": self.key}


class ComparisonBasic(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: ComparisonBasicType = ComparisonBasicType(raw_element["type"])
        self.negate: bool = raw_element["negate"]

    def to_json(self) -> Dict[str, Any]:
        return {"type": str(self.type), "negate": self.negate}


class CustomProcessMetadataConditionKey(ConditionKey):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.dynamic_key: CustomProcessMetadataKey = CustomProcessMetadataKey(raw_element=raw_element["dynamicKey"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"dynamicKey": self.dynamic_key.to_json()})
        return details


class CustomHostMetadataConditionKey(ConditionKey):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.dynamic_key: CustomHostMetadataKey = CustomHostMetadataKey(raw_element=raw_element["dynamicKey"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"dynamicKey": self.dynamic_key.to_json()})
        return details


class ProcessMetadataConditionKey(ConditionKey):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.dynamic_key: PredefinedProcessMetadataKeySource = PredefinedProcessMetadataKeySource(raw_element["dynamicKey"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"dynamicKey": str(self.dynamic_key)})
        return details


class StringConditionKey(ConditionKey):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.dynamic_key: str = raw_element["dynamicKey"]

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"dynamicKey": self.dynamic_key})
        return details


class StringComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[str] = raw_element.get("value")
        self.operator: StringComparisonOperator = StringComparisonOperator(raw_element["operator"])
        self.case_sensitive: Optional[bool] = raw_element.get("caseSensitive")

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value, "operator": str(self.operator), "caseSensitive": self.case_sensitive})
        return details


class IndexedNameComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[str] = raw_element.get("value")
        self.operator: IndexedNameComparisonOperator = IndexedNameComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value, "operator": str(self.operator)})
        return details


class IndexedStringComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[str] = raw_element.get("value")
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value, "operator": str(self.operator)})
        return details


class IntegerComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[int] = raw_element.get("value")
        self.operator: IntegerComparisonOperator = IntegerComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value, "operator": str(self.operator)})
        return details


class ServiceTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[ServiceTypeComparisonValue] = ServiceTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class PaasTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[PaasTypeComparisonValue] = PaasTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class CloudTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[CloudTypeComparisonValue] = CloudTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class AzureSkuComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[AzureSkuComparisonValue] = AzureSkuComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class AzureComputeModeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[AzureComputeModeComparisonValue] = AzureComputeModeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class EntityIdComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[str] = raw_element.get("value")
        self.operator: EqualsComparisonOperator = EqualsComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value, "operator": str(self.operator)})
        return details


class SimpleTechComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[SimpleTech] = SimpleTech(raw_element=raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value.to_json() if self.value else None, "operator": str(self.operator)})
        return details


class SimpleHostTechComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[SimpleHostTech] = SimpleHostTech(raw_element=raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value.to_json() if self.value else None, "operator": str(self.operator)})
        return details


class ServiceTopologyComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[ServiceTopologyComparisonValue] = ServiceTopologyComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class DatabaseTopologyComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[DatabaseTopologyComparisonValue] = DatabaseTopologyComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class OsTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[OsTypeComparisonValue] = OsTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class HypervisorTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[HypervisorTypeComparisonValue] = HypervisorTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class IpAddressComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[str] = raw_element.get("value")
        self.operator: IpAddressComparisonOperator = IpAddressComparisonOperator(raw_element["operator"])
        self.case_sensitive: Optional[bool] = raw_element.get("caseSensitive")

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value, "operator": str(self.operator), "caseSensitive": self.case_sensitive})
        return details


class OsArchitectureComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[OsArchitectureComparisonValue] = OsArchitectureComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class BitnessComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[BitnessComparisonValue] = BitnessComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class ApplicationTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[ApplicationTypeComparisonValue] = ApplicationTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class CustomApplicationTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[CustomApplicationTypeComparisonValue] = (
            CustomApplicationTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        )
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class MobilePlatformComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[MobilePlatformComparisonValue] = MobilePlatformComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class DcrumDecoderComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[DcrumDecoderComparisonValue] = DcrumDecoderComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class SyntheticEngineTypeComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[SyntheticEngineTypeComparisonValue] = (
            SyntheticEngineTypeComparisonValue(raw_element["value"]) if raw_element.get("value") else None
        )
        self.operator: BasicComparisonOperator = BasicComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": str(self.value) if self.value else None, "operator": str(self.operator)})
        return details


class TagComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[TagInfo] = TagInfo(raw_element=raw_element["value"]) if raw_element.get("value") else None
        self.operator: TagComparisonOperator = TagComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value.to_json() if self.value else None, "operator": str(self.operator)})
        return details


class IndexedTagComparison(ComparisonBasic):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value: Optional[TagInfo] = TagInfo(raw_element=raw_element["value"]) if raw_element.get("value") else None
        self.operator: IndexedTagComparisonOperator = IndexedTagComparisonOperator(raw_element["operator"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"value": self.value.to_json() if self.value else None, "operator": str(self.operator)})
        return details


### MZ SPECIFIC ENUMS ####
##########################


class CustomProcessMetadataKeySource(Enum):
    CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
    ENVIRONMENT = "ENVIRONMENT"
    GOOGLE_CLOUD = "GOOGLE_CLOUD"
    KUBERNETES = "KUBERNETES"
    PLUGIN = "PLUGIN"

    def __str__(self) -> str:
        return self.value


class PredefinedProcessMetadataKeySource(Enum):
    AMAZON_ECR_IMAGE_ACCOUNT_ID = "AMAZON_ECR_IMAGE_ACCOUNT_ID"
    AMAZON_ECR_IMAGE_REGION = "AMAZON_ECR_IMAGE_REGION"
    AMAZON_LAMBDA_FUNCTION_NAME = "AMAZON_LAMBDA_FUNCTION_NAME"
    AMAZON_REGION = "AMAZON_REGION"
    APACHE_CONFIG_PATH = "APACHE_CONFIG_PATH"
    APACHE_SPARK_MASTER_IP_ADDRESS = "APACHE_SPARK_MASTER_IP_ADDRESS"
    ASP_DOT_NET_CORE_APPLICATION_PATH = "ASP_DOT_NET_CORE_APPLICATION_PATH"
    AWS_ECS_CLUSTER = "AWS_ECS_CLUSTER"
    AWS_ECS_CONTAINERNAME = "AWS_ECS_CONTAINERNAME"
    AWS_ECS_FAMILY = "AWS_ECS_FAMILY"
    AWS_ECS_REVISION = "AWS_ECS_REVISION"
    CASSANDRA_CLUSTER_NAME = "CASSANDRA_CLUSTER_NAME"
    CATALINA_BASE = "CATALINA_BASE"
    CATALINA_HOME = "CATALINA_HOME"
    CLOUD_FOUNDRY_APP_ID = "CLOUD_FOUNDRY_APP_ID"
    CLOUD_FOUNDRY_APP_NAME = "CLOUD_FOUNDRY_APP_NAME"
    CLOUD_FOUNDRY_INSTANCE_INDEX = "CLOUD_FOUNDRY_INSTANCE_INDEX"
    CLOUD_FOUNDRY_SPACE_ID = "CLOUD_FOUNDRY_SPACE_ID"
    CLOUD_FOUNDRY_SPACE_NAME = "CLOUD_FOUNDRY_SPACE_NAME"
    COLDFUSION_JVM_CONFIG_FILE = "COLDFUSION_JVM_CONFIG_FILE"
    COLDFUSION_SERVICE_NAME = "COLDFUSION_SERVICE_NAME"
    COMMAND_LINE_ARGS = "COMMAND_LINE_ARGS"
    DECLARATIVE_ID = "DECLARATIVE_ID"
    DOTNET_COMMAND = "DOTNET_COMMAND"
    DOTNET_COMMAND_PATH = "DOTNET_COMMAND_PATH"
    DYNATRACE_CLUSTER_ID = "DYNATRACE_CLUSTER_ID"
    DYNATRACE_NODE_ID = "DYNATRACE_NODE_ID"
    ELASTICSEARCH_CLUSTER_NAME = "ELASTICSEARCH_CLUSTER_NAME"
    ELASTICSEARCH_NODE_NAME = "ELASTICSEARCH_NODE_NAME"
    EQUINOX_CONFIG_PATH = "EQUINOX_CONFIG_PATH"
    EXE_NAME = "EXE_NAME"
    EXE_PATH = "EXE_PATH"
    GLASS_FISH_DOMAIN_NAME = "GLASS_FISH_DOMAIN_NAME"
    GLASS_FISH_INSTANCE_NAME = "GLASS_FISH_INSTANCE_NAME"
    GOOGLE_APP_ENGINE_INSTANCE = "GOOGLE_APP_ENGINE_INSTANCE"
    GOOGLE_APP_ENGINE_SERVICE = "GOOGLE_APP_ENGINE_SERVICE"
    GOOGLE_CLOUD_PROJECT = "GOOGLE_CLOUD_PROJECT"
    HYBRIS_BIN_DIRECTORY = "HYBRIS_BIN_DIRECTORY"
    HYBRIS_CONFIG_DIRECTORY = "HYBRIS_CONFIG_DIRECTORY"
    HYBRIS_DATA_DIRECTORY = "HYBRIS_DATA_DIRECTORY"
    IBM_CICS_REGION = "IBM_CICS_REGION"
    IBM_CTG_NAME = "IBM_CTG_NAME"
    IBM_IMS_CONNECT_REGION = "IBM_IMS_CONNECT_REGION"
    IBM_IMS_CONTROL_REGION = "IBM_IMS_CONTROL_REGION"
    IBM_IMS_MESSAGE_PROCESSING_REGION = "IBM_IMS_MESSAGE_PROCESSING_REGION"
    IBM_IMS_SOAP_GW_NAME = "IBM_IMS_SOAP_GW_NAME"
    IBM_INTEGRATION_NODE_NAME = "IBM_INTEGRATION_NODE_NAME"
    IBM_INTEGRATION_SERVER_NAME = "IBM_INTEGRATION_SERVER_NAME"
    IIS_APP_POOL = "IIS_APP_POOL"
    IIS_ROLE_NAME = "IIS_ROLE_NAME"
    JAVA_JAR_FILE = "JAVA_JAR_FILE"
    JAVA_JAR_PATH = "JAVA_JAR_PATH"
    JAVA_MAIN_CLASS = "JAVA_MAIN_CLASS"
    JAVA_MAIN_MODULE = "JAVA_MAIN_MODULE"
    JBOSS_HOME = "JBOSS_HOME"
    JBOSS_MODE = "JBOSS_MODE"
    JBOSS_SERVER_NAME = "JBOSS_SERVER_NAME"
    KUBERNETES_BASE_POD_NAME = "KUBERNETES_BASE_POD_NAME"
    KUBERNETES_CONTAINER_NAME = "KUBERNETES_CONTAINER_NAME"
    KUBERNETES_FULL_POD_NAME = "KUBERNETES_FULL_POD_NAME"
    KUBERNETES_NAMESPACE = "KUBERNETES_NAMESPACE"
    KUBERNETES_POD_UID = "KUBERNETES_POD_UID"
    MSSQL_INSTANCE_NAME = "MSSQL_INSTANCE_NAME"
    NODE_JS_APP_BASE_DIRECTORY = "NODE_JS_APP_BASE_DIRECTORY"
    NODE_JS_APP_NAME = "NODE_JS_APP_NAME"
    NODE_JS_SCRIPT_NAME = "NODE_JS_SCRIPT_NAME"
    ORACLE_SID = "ORACLE_SID"
    PG_ID_CALC_INPUT_KEY_LINKAGE = "PG_ID_CALC_INPUT_KEY_LINKAGE"
    PHP_SCRIPT_PATH = "PHP_SCRIPT_PATH"
    PHP_WORKING_DIRECTORY = "PHP_WORKING_DIRECTORY"
    RUBY_APP_ROOT_PATH = "RUBY_APP_ROOT_PATH"
    RUBY_SCRIPT_PATH = "RUBY_SCRIPT_PATH"
    RULE_RESULT = "RULE_RESULT"
    SOFTWAREAG_INSTALL_ROOT = "SOFTWAREAG_INSTALL_ROOT"
    SOFTWAREAG_PRODUCTPROPNAME = "SOFTWAREAG_PRODUCTPROPNAME"
    SPRINGBOOT_APP_NAME = "SPRINGBOOT_APP_NAME"
    SPRINGBOOT_PROFILE_NAME = "SPRINGBOOT_PROFILE_NAME"
    SPRINGBOOT_STARTUP_CLASS = "SPRINGBOOT_STARTUP_CLASS"
    TIBCO_BUSINESSWORKS_CE_APP_NAME = "TIBCO_BUSINESSWORKS_CE_APP_NAME"
    TIBCO_BUSINESSWORKS_CE_VERSION = "TIBCO_BUSINESSWORKS_CE_VERSION"
    TIBCO_BUSINESS_WORKS_APP_NODE_NAME = "TIBCO_BUSINESS_WORKS_APP_NODE_NAME"
    TIBCO_BUSINESS_WORKS_APP_SPACE_NAME = "TIBCO_BUSINESS_WORKS_APP_SPACE_NAME"
    TIBCO_BUSINESS_WORKS_DOMAIN_NAME = "TIBCO_BUSINESS_WORKS_DOMAIN_NAME"
    TIBCO_BUSINESS_WORKS_ENGINE_PROPERTY_FILE = "TIBCO_BUSINESS_WORKS_ENGINE_PROPERTY_FILE"
    TIBCO_BUSINESS_WORKS_ENGINE_PROPERTY_FILE_PATH = "TIBCO_BUSINESS_WORKS_ENGINE_PROPERTY_FILE_PATH"
    TIBCO_BUSINESS_WORKS_HOME = "TIBCO_BUSINESS_WORKS_HOME"
    VARNISH_INSTANCE_NAME = "VARNISH_INSTANCE_NAME"
    WEB_LOGIC_CLUSTER_NAME = "WEB_LOGIC_CLUSTER_NAME"
    WEB_LOGIC_DOMAIN_NAME = "WEB_LOGIC_DOMAIN_NAME"
    WEB_LOGIC_HOME = "WEB_LOGIC_HOME"
    WEB_LOGIC_NAME = "WEB_LOGIC_NAME"
    WEB_SPHERE_CELL_NAME = "WEB_SPHERE_CELL_NAME"
    WEB_SPHERE_CLUSTER_NAME = "WEB_SPHERE_CLUSTER_NAME"
    WEB_SPHERE_NODE_NAME = "WEB_SPHERE_NODE_NAME"
    WEB_SPHERE_SERVER_NAME = "WEB_SPHERE_SERVER_NAME"

    def __str__(self) -> str:
        return self.value


class HostMetadataKeySource(Enum):
    ENVIRONMENT = "ENVIRONMENT"
    GOOGLE_COMPUTE_ENGINE = "GOOGLE_COMPUTE_ENGINE"
    PLUGIN = "PLUGIN"

    def __str__(self) -> str:
        return self.value


class PropagationType(Enum):
    AZURE_TO_PG = "AZURE_TO_PG"
    AZURE_TO_SERVICE = "AZURE_TO_SERVICE"
    CUSTOM_DEVICE_GROUP_TO_CUSTOM_DEVICE = "CUSTOM_DEVICE_GROUP_TO_CUSTOM_DEVICE"
    HOST_TO_PROCESS_GROUP_INSTANCE = "HOST_TO_PROCESS_GROUP_INSTANCE"
    PROCESS_GROUP_TO_HOST = "PROCESS_GROUP_TO_HOST"
    PROCESS_GROUP_TO_SERVICE = "PROCESS_GROUP_TO_SERVICE"
    SERVICE_TO_HOST_LIKE = "SERVICE_TO_HOST_LIKE"
    SERVICE_TO_PROCESS_GROUP_LIKE = "SERVICE_TO_PROCESS_GROUP_LIKE"

    def __str__(self) -> str:
        return self.value


class MzConditionType(Enum):
    HOST_CUSTOM_METADATA_KEY = "HOST_CUSTOM_METADATA_KEY"
    PROCESS_CUSTOM_METADATA_KEY = "PROCESS_CUSTOM_METADATA_KEY"
    PROCESS_PREDEFINED_METADATA_KEY = "PROCESS_PREDEFINED_METADATA_KEY"
    STATIC = "STATIC"
    STRING = "STRING"

    def __str__(self) -> str:
        return self.value


class MzConditionAttribute(Enum):
    APPMON_SERVER_NAME = "APPMON_SERVER_NAME"
    APPMON_SYSTEM_PROFILE_NAME = "APPMON_SYSTEM_PROFILE_NAME"
    AWS_ACCOUNT_ID = "AWS_ACCOUNT_ID"
    AWS_ACCOUNT_NAME = "AWS_ACCOUNT_NAME"
    AWS_APPLICATION_LOAD_BALANCER_NAME = "AWS_APPLICATION_LOAD_BALANCER_NAME"
    AWS_APPLICATION_LOAD_BALANCER_TAGS = "AWS_APPLICATION_LOAD_BALANCER_TAGS"
    AWS_AUTO_SCALING_GROUP_NAME = "AWS_AUTO_SCALING_GROUP_NAME"
    AWS_AUTO_SCALING_GROUP_TAGS = "AWS_AUTO_SCALING_GROUP_TAGS"
    AWS_AVAILABILITY_ZONE_NAME = "AWS_AVAILABILITY_ZONE_NAME"
    AWS_CLASSIC_LOAD_BALANCER_FRONTEND_PORTS = "AWS_CLASSIC_LOAD_BALANCER_FRONTEND_PORTS"
    AWS_CLASSIC_LOAD_BALANCER_NAME = "AWS_CLASSIC_LOAD_BALANCER_NAME"
    AWS_CLASSIC_LOAD_BALANCER_TAGS = "AWS_CLASSIC_LOAD_BALANCER_TAGS"
    AWS_NETWORK_LOAD_BALANCER_NAME = "AWS_NETWORK_LOAD_BALANCER_NAME"
    AWS_NETWORK_LOAD_BALANCER_TAGS = "AWS_NETWORK_LOAD_BALANCER_TAGS"
    AWS_RELATIONAL_DATABASE_SERVICE_DB_NAME = "AWS_RELATIONAL_DATABASE_SERVICE_DB_NAME"
    AWS_RELATIONAL_DATABASE_SERVICE_ENDPOINT = "AWS_RELATIONAL_DATABASE_SERVICE_ENDPOINT"
    AWS_RELATIONAL_DATABASE_SERVICE_ENGINE = "AWS_RELATIONAL_DATABASE_SERVICE_ENGINE"
    AWS_RELATIONAL_DATABASE_SERVICE_INSTANCE_CLASS = "AWS_RELATIONAL_DATABASE_SERVICE_INSTANCE_CLASS"
    AWS_RELATIONAL_DATABASE_SERVICE_NAME = "AWS_RELATIONAL_DATABASE_SERVICE_NAME"
    AWS_RELATIONAL_DATABASE_SERVICE_PORT = "AWS_RELATIONAL_DATABASE_SERVICE_PORT"
    AWS_RELATIONAL_DATABASE_SERVICE_TAGS = "AWS_RELATIONAL_DATABASE_SERVICE_TAGS"
    AZURE_ENTITY_NAME = "AZURE_ENTITY_NAME"
    AZURE_ENTITY_TAGS = "AZURE_ENTITY_TAGS"
    AZURE_MGMT_GROUP_NAME = "AZURE_MGMT_GROUP_NAME"
    AZURE_MGMT_GROUP_UUID = "AZURE_MGMT_GROUP_UUID"
    AZURE_REGION_NAME = "AZURE_REGION_NAME"
    AZURE_SCALE_SET_NAME = "AZURE_SCALE_SET_NAME"
    AZURE_SUBSCRIPTION_NAME = "AZURE_SUBSCRIPTION_NAME"
    AZURE_SUBSCRIPTION_UUID = "AZURE_SUBSCRIPTION_UUID"
    AZURE_TENANT_NAME = "AZURE_TENANT_NAME"
    AZURE_TENANT_UUID = "AZURE_TENANT_UUID"
    AZURE_VM_NAME = "AZURE_VM_NAME"
    BROWSER_MONITOR_NAME = "BROWSER_MONITOR_NAME"
    BROWSER_MONITOR_TAGS = "BROWSER_MONITOR_TAGS"
    CLOUD_APPLICATION_LABELS = "CLOUD_APPLICATION_LABELS"
    CLOUD_APPLICATION_NAME = "CLOUD_APPLICATION_NAME"
    CLOUD_APPLICATION_NAMESPACE_LABELS = "CLOUD_APPLICATION_NAMESPACE_LABELS"
    CLOUD_APPLICATION_NAMESPACE_NAME = "CLOUD_APPLICATION_NAMESPACE_NAME"
    CLOUD_FOUNDRY_FOUNDATION_NAME = "CLOUD_FOUNDRY_FOUNDATION_NAME"
    CLOUD_FOUNDRY_ORG_NAME = "CLOUD_FOUNDRY_ORG_NAME"
    CUSTOM_APPLICATION_NAME = "CUSTOM_APPLICATION_NAME"
    CUSTOM_APPLICATION_PLATFORM = "CUSTOM_APPLICATION_PLATFORM"
    CUSTOM_APPLICATION_TAGS = "CUSTOM_APPLICATION_TAGS"
    CUSTOM_APPLICATION_TYPE = "CUSTOM_APPLICATION_TYPE"
    CUSTOM_DEVICE_DETECTED_NAME = "CUSTOM_DEVICE_DETECTED_NAME"
    CUSTOM_DEVICE_DNS_ADDRESS = "CUSTOM_DEVICE_DNS_ADDRESS"
    CUSTOM_DEVICE_GROUP_NAME = "CUSTOM_DEVICE_GROUP_NAME"
    CUSTOM_DEVICE_GROUP_TAGS = "CUSTOM_DEVICE_GROUP_TAGS"
    CUSTOM_DEVICE_IP_ADDRESS = "CUSTOM_DEVICE_IP_ADDRESS"
    CUSTOM_DEVICE_METADATA = "CUSTOM_DEVICE_METADATA"
    CUSTOM_DEVICE_NAME = "CUSTOM_DEVICE_NAME"
    CUSTOM_DEVICE_PORT = "CUSTOM_DEVICE_PORT"
    CUSTOM_DEVICE_TAGS = "CUSTOM_DEVICE_TAGS"
    CUSTOM_DEVICE_TECHNOLOGY = "CUSTOM_DEVICE_TECHNOLOGY"
    DATA_CENTER_SERVICE_DECODER_TYPE = "DATA_CENTER_SERVICE_DECODER_TYPE"
    DATA_CENTER_SERVICE_IP_ADDRESS = "DATA_CENTER_SERVICE_IP_ADDRESS"
    DATA_CENTER_SERVICE_METADATA = "DATA_CENTER_SERVICE_METADATA"
    DATA_CENTER_SERVICE_NAME = "DATA_CENTER_SERVICE_NAME"
    DATA_CENTER_SERVICE_PORT = "DATA_CENTER_SERVICE_PORT"
    DATA_CENTER_SERVICE_TAGS = "DATA_CENTER_SERVICE_TAGS"
    DOCKER_CONTAINER_NAME = "DOCKER_CONTAINER_NAME"
    DOCKER_FULL_IMAGE_NAME = "DOCKER_FULL_IMAGE_NAME"
    DOCKER_IMAGE_VERSION = "DOCKER_IMAGE_VERSION"
    DOCKER_STRIPPED_IMAGE_NAME = "DOCKER_STRIPPED_IMAGE_NAME"
    EC2_INSTANCE_AMI_ID = "EC2_INSTANCE_AMI_ID"
    EC2_INSTANCE_AWS_INSTANCE_TYPE = "EC2_INSTANCE_AWS_INSTANCE_TYPE"
    EC2_INSTANCE_AWS_SECURITY_GROUP = "EC2_INSTANCE_AWS_SECURITY_GROUP"
    EC2_INSTANCE_BEANSTALK_ENV_NAME = "EC2_INSTANCE_BEANSTALK_ENV_NAME"
    EC2_INSTANCE_ID = "EC2_INSTANCE_ID"
    EC2_INSTANCE_NAME = "EC2_INSTANCE_NAME"
    EC2_INSTANCE_PRIVATE_HOST_NAME = "EC2_INSTANCE_PRIVATE_HOST_NAME"
    EC2_INSTANCE_PUBLIC_HOST_NAME = "EC2_INSTANCE_PUBLIC_HOST_NAME"
    EC2_INSTANCE_TAGS = "EC2_INSTANCE_TAGS"
    ENTERPRISE_APPLICATION_DECODER_TYPE = "ENTERPRISE_APPLICATION_DECODER_TYPE"
    ENTERPRISE_APPLICATION_IP_ADDRESS = "ENTERPRISE_APPLICATION_IP_ADDRESS"
    ENTERPRISE_APPLICATION_METADATA = "ENTERPRISE_APPLICATION_METADATA"
    ENTERPRISE_APPLICATION_NAME = "ENTERPRISE_APPLICATION_NAME"
    ENTERPRISE_APPLICATION_PORT = "ENTERPRISE_APPLICATION_PORT"
    ENTERPRISE_APPLICATION_TAGS = "ENTERPRISE_APPLICATION_TAGS"
    ESXI_HOST_CLUSTER_NAME = "ESXI_HOST_CLUSTER_NAME"
    ESXI_HOST_HARDWARE_MODEL = "ESXI_HOST_HARDWARE_MODEL"
    ESXI_HOST_HARDWARE_VENDOR = "ESXI_HOST_HARDWARE_VENDOR"
    ESXI_HOST_NAME = "ESXI_HOST_NAME"
    ESXI_HOST_PRODUCT_NAME = "ESXI_HOST_PRODUCT_NAME"
    ESXI_HOST_PRODUCT_VERSION = "ESXI_HOST_PRODUCT_VERSION"
    ESXI_HOST_TAGS = "ESXI_HOST_TAGS"
    EXTERNAL_MONITOR_ENGINE_DESCRIPTION = "EXTERNAL_MONITOR_ENGINE_DESCRIPTION"
    EXTERNAL_MONITOR_ENGINE_NAME = "EXTERNAL_MONITOR_ENGINE_NAME"
    EXTERNAL_MONITOR_ENGINE_TYPE = "EXTERNAL_MONITOR_ENGINE_TYPE"
    EXTERNAL_MONITOR_NAME = "EXTERNAL_MONITOR_NAME"
    EXTERNAL_MONITOR_TAGS = "EXTERNAL_MONITOR_TAGS"
    GEOLOCATION_SITE_NAME = "GEOLOCATION_SITE_NAME"
    GOOGLE_CLOUD_PLATFORM_ZONE_NAME = "GOOGLE_CLOUD_PLATFORM_ZONE_NAME"
    GOOGLE_COMPUTE_INSTANCE_ID = "GOOGLE_COMPUTE_INSTANCE_ID"
    GOOGLE_COMPUTE_INSTANCE_MACHINE_TYPE = "GOOGLE_COMPUTE_INSTANCE_MACHINE_TYPE"
    GOOGLE_COMPUTE_INSTANCE_NAME = "GOOGLE_COMPUTE_INSTANCE_NAME"
    GOOGLE_COMPUTE_INSTANCE_PROJECT = "GOOGLE_COMPUTE_INSTANCE_PROJECT"
    GOOGLE_COMPUTE_INSTANCE_PROJECT_ID = "GOOGLE_COMPUTE_INSTANCE_PROJECT_ID"
    GOOGLE_COMPUTE_INSTANCE_PUBLIC_IP_ADDRESSES = "GOOGLE_COMPUTE_INSTANCE_PUBLIC_IP_ADDRESSES"
    HOST_AIX_LOGICAL_CPU_COUNT = "HOST_AIX_LOGICAL_CPU_COUNT"
    HOST_AIX_SIMULTANEOUS_THREADS = "HOST_AIX_SIMULTANEOUS_THREADS"
    HOST_AIX_VIRTUAL_CPU_COUNT = "HOST_AIX_VIRTUAL_CPU_COUNT"
    HOST_ARCHITECTURE = "HOST_ARCHITECTURE"
    HOST_AWS_NAME_TAG = "HOST_AWS_NAME_TAG"
    HOST_AZURE_COMPUTE_MODE = "HOST_AZURE_COMPUTE_MODE"
    HOST_AZURE_SKU = "HOST_AZURE_SKU"
    HOST_AZURE_WEB_APPLICATION_HOST_NAMES = "HOST_AZURE_WEB_APPLICATION_HOST_NAMES"
    HOST_AZURE_WEB_APPLICATION_SITE_NAMES = "HOST_AZURE_WEB_APPLICATION_SITE_NAMES"
    HOST_BITNESS = "HOST_BITNESS"
    HOST_BOSH_AVAILABILITY_ZONE = "HOST_BOSH_AVAILABILITY_ZONE"
    HOST_BOSH_DEPLOYMENT_ID = "HOST_BOSH_DEPLOYMENT_ID"
    HOST_BOSH_INSTANCE_ID = "HOST_BOSH_INSTANCE_ID"
    HOST_BOSH_INSTANCE_NAME = "HOST_BOSH_INSTANCE_NAME"
    HOST_BOSH_NAME = "HOST_BOSH_NAME"
    HOST_BOSH_STEMCELL_VERSION = "HOST_BOSH_STEMCELL_VERSION"
    HOST_CLOUD_TYPE = "HOST_CLOUD_TYPE"
    HOST_CPU_CORES = "HOST_CPU_CORES"
    HOST_CUSTOM_METADATA = "HOST_CUSTOM_METADATA"
    HOST_DETECTED_NAME = "HOST_DETECTED_NAME"
    HOST_GROUP_ID = "HOST_GROUP_ID"
    HOST_GROUP_NAME = "HOST_GROUP_NAME"
    HOST_HYPERVISOR_TYPE = "HOST_HYPERVISOR_TYPE"
    HOST_IP_ADDRESS = "HOST_IP_ADDRESS"
    HOST_KUBERNETES_LABELS = "HOST_KUBERNETES_LABELS"
    HOST_LOGICAL_CPU_CORES = "HOST_LOGICAL_CPU_CORES"
    HOST_NAME = "HOST_NAME"
    HOST_ONEAGENT_CUSTOM_HOST_NAME = "HOST_ONEAGENT_CUSTOM_HOST_NAME"
    HOST_OS_TYPE = "HOST_OS_TYPE"
    HOST_OS_VERSION = "HOST_OS_VERSION"
    HOST_PAAS_MEMORY_LIMIT = "HOST_PAAS_MEMORY_LIMIT"
    HOST_PAAS_TYPE = "HOST_PAAS_TYPE"
    HOST_TAGS = "HOST_TAGS"
    HOST_TECHNOLOGY = "HOST_TECHNOLOGY"
    HTTP_MONITOR_NAME = "HTTP_MONITOR_NAME"
    HTTP_MONITOR_TAGS = "HTTP_MONITOR_TAGS"
    KUBERNETES_CLUSTER_NAME = "KUBERNETES_CLUSTER_NAME"
    KUBERNETES_NODE_NAME = "KUBERNETES_NODE_NAME"
    MOBILE_APPLICATION_NAME = "MOBILE_APPLICATION_NAME"
    MOBILE_APPLICATION_PLATFORM = "MOBILE_APPLICATION_PLATFORM"
    MOBILE_APPLICATION_TAGS = "MOBILE_APPLICATION_TAGS"
    NAME_OF_COMPUTE_NODE = "NAME_OF_COMPUTE_NODE"
    OPENSTACK_ACCOUNT_NAME = "OPENSTACK_ACCOUNT_NAME"
    OPENSTACK_ACCOUNT_PROJECT_NAME = "OPENSTACK_ACCOUNT_PROJECT_NAME"
    OPENSTACK_AVAILABILITY_ZONE_NAME = "OPENSTACK_AVAILABILITY_ZONE_NAME"
    OPENSTACK_PROJECT_NAME = "OPENSTACK_PROJECT_NAME"
    OPENSTACK_REGION_NAME = "OPENSTACK_REGION_NAME"
    OPENSTACK_VM_INSTANCE_TYPE = "OPENSTACK_VM_INSTANCE_TYPE"
    OPENSTACK_VM_NAME = "OPENSTACK_VM_NAME"
    OPENSTACK_VM_SECURITY_GROUP = "OPENSTACK_VM_SECURITY_GROUP"
    PROCESS_GROUP_AZURE_HOST_NAME = "PROCESS_GROUP_AZURE_HOST_NAME"
    PROCESS_GROUP_AZURE_SITE_NAME = "PROCESS_GROUP_AZURE_SITE_NAME"
    PROCESS_GROUP_CUSTOM_METADATA = "PROCESS_GROUP_CUSTOM_METADATA"
    PROCESS_GROUP_DETECTED_NAME = "PROCESS_GROUP_DETECTED_NAME"
    PROCESS_GROUP_ID = "PROCESS_GROUP_ID"
    PROCESS_GROUP_LISTEN_PORT = "PROCESS_GROUP_LISTEN_PORT"
    PROCESS_GROUP_NAME = "PROCESS_GROUP_NAME"
    PROCESS_GROUP_PREDEFINED_METADATA = "PROCESS_GROUP_PREDEFINED_METADATA"
    PROCESS_GROUP_TAGS = "PROCESS_GROUP_TAGS"
    PROCESS_GROUP_TECHNOLOGY = "PROCESS_GROUP_TECHNOLOGY"
    PROCESS_GROUP_TECHNOLOGY_EDITION = "PROCESS_GROUP_TECHNOLOGY_EDITION"
    PROCESS_GROUP_TECHNOLOGY_VERSION = "PROCESS_GROUP_TECHNOLOGY_VERSION"
    SERVICE_AKKA_ACTOR_SYSTEM = "SERVICE_AKKA_ACTOR_SYSTEM"
    SERVICE_CTG_SERVICE_NAME = "SERVICE_CTG_SERVICE_NAME"
    SERVICE_DATABASE_HOST_NAME = "SERVICE_DATABASE_HOST_NAME"
    SERVICE_DATABASE_NAME = "SERVICE_DATABASE_NAME"
    SERVICE_DATABASE_TOPOLOGY = "SERVICE_DATABASE_TOPOLOGY"
    SERVICE_DATABASE_VENDOR = "SERVICE_DATABASE_VENDOR"
    SERVICE_DETECTED_NAME = "SERVICE_DETECTED_NAME"
    SERVICE_ESB_APPLICATION_NAME = "SERVICE_ESB_APPLICATION_NAME"
    SERVICE_IBM_CTG_GATEWAY_URL = "SERVICE_IBM_CTG_GATEWAY_URL"
    SERVICE_IIB_APPLICATION_NAME = "SERVICE_IIB_APPLICATION_NAME"
    SERVICE_MESSAGING_LISTENER_CLASS_NAME = "SERVICE_MESSAGING_LISTENER_CLASS_NAME"
    SERVICE_NAME = "SERVICE_NAME"
    SERVICE_PORT = "SERVICE_PORT"
    SERVICE_PUBLIC_DOMAIN_NAME = "SERVICE_PUBLIC_DOMAIN_NAME"
    SERVICE_REMOTE_ENDPOINT = "SERVICE_REMOTE_ENDPOINT"
    SERVICE_REMOTE_SERVICE_NAME = "SERVICE_REMOTE_SERVICE_NAME"
    SERVICE_TAGS = "SERVICE_TAGS"
    SERVICE_TECHNOLOGY = "SERVICE_TECHNOLOGY"
    SERVICE_TECHNOLOGY_EDITION = "SERVICE_TECHNOLOGY_EDITION"
    SERVICE_TECHNOLOGY_VERSION = "SERVICE_TECHNOLOGY_VERSION"
    SERVICE_TOPOLOGY = "SERVICE_TOPOLOGY"
    SERVICE_TYPE = "SERVICE_TYPE"
    SERVICE_WEB_APPLICATION_ID = "SERVICE_WEB_APPLICATION_ID"
    SERVICE_WEB_CONTEXT_ROOT = "SERVICE_WEB_CONTEXT_ROOT"
    SERVICE_WEB_SERVER_ENDPOINT = "SERVICE_WEB_SERVER_ENDPOINT"
    SERVICE_WEB_SERVER_NAME = "SERVICE_WEB_SERVER_NAME"
    SERVICE_WEB_SERVICE_NAME = "SERVICE_WEB_SERVICE_NAME"
    SERVICE_WEB_SERVICE_NAMESPACE = "SERVICE_WEB_SERVICE_NAMESPACE"
    VMWARE_DATACENTER_NAME = "VMWARE_DATACENTER_NAME"
    VMWARE_VM_NAME = "VMWARE_VM_NAME"
    WEB_APPLICATION_NAME = "WEB_APPLICATION_NAME"
    WEB_APPLICATION_NAME_PATTERN = "WEB_APPLICATION_NAME_PATTERN"
    WEB_APPLICATION_TAGS = "WEB_APPLICATION_TAGS"
    WEB_APPLICATION_TYPE = "WEB_APPLICATION_TYPE"

    def __str__(self) -> str:
        return self.value


class MzDimensionalRuleAppliesTo(Enum):
    ANY = "ANY"
    LOG = "LOG"
    METRIC = "METRIC"

    def __str__(self) -> str:
        return self.value


class MzDimensionalRuleConditionType(Enum):
    DIMENSION = "DIMENSION"
    LOG_FILE_NAME = "LOG_FILE_NAME"
    METRIC_KEY = "METRIC_KEY"

    def __str__(self) -> str:
        return self.value


class MzDimensionalRuleMatcher(Enum):
    BEGINS_WITH = "BEGINS_WITH"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


### MISC ENUMS ###
##################


class SimpleTechType(Enum):
    ACTIVE_MQ = "ACTIVE_MQ"
    ACTIVE_MQ_ARTEMIS = "ACTIVE_MQ_ARTEMIS"
    ADO_NET = "ADO_NET"
    AIX = "AIX"
    AKKA = "AKKA"
    AMAZON_REDSHIFT = "AMAZON_REDSHIFT"
    AMQP = "AMQP"
    APACHE_CAMEL = "APACHE_CAMEL"
    APACHE_CASSANDRA = "APACHE_CASSANDRA"
    APACHE_COUCH_DB = "APACHE_COUCH_DB"
    APACHE_DERBY = "APACHE_DERBY"
    APACHE_HTTP_CLIENT_ASYNC = "APACHE_HTTP_CLIENT_ASYNC"
    APACHE_HTTP_CLIENT_SYNC = "APACHE_HTTP_CLIENT_SYNC"
    APACHE_HTTP_SERVER = "APACHE_HTTP_SERVER"
    APACHE_KAFKA = "APACHE_KAFKA"
    APACHE_SOLR = "APACHE_SOLR"
    APACHE_STORM = "APACHE_STORM"
    APACHE_SYNAPSE = "APACHE_SYNAPSE"
    APACHE_TOMCAT = "APACHE_TOMCAT"
    APPARMOR = "APPARMOR"
    APPLICATION_INSIGHTS_SDK = "APPLICATION_INSIGHTS_SDK"
    ASP_DOTNET = "ASP_DOTNET"
    ASP_DOTNET_CORE = "ASP_DOTNET_CORE"
    ASP_DOTNET_CORE_SIGNALR = "ASP_DOTNET_CORE_SIGNALR"
    ASP_DOTNET_SIGNALR = "ASP_DOTNET_SIGNALR"
    ASYNC_HTTP_CLIENT = "ASYNC_HTTP_CLIENT"
    AWS_LAMBDA = "AWS_LAMBDA"
    AWS_RDS = "AWS_RDS"
    AWS_SERVICE = "AWS_SERVICE"
    AXIS = "AXIS"
    AZURE_FUNCTIONS = "AZURE_FUNCTIONS"
    AZURE_SERVICE_BUS = "AZURE_SERVICE_BUS"
    AZURE_SERVICE_FABRIC = "AZURE_SERVICE_FABRIC"
    AZURE_STORAGE = "AZURE_STORAGE"
    BOSHBPM = "BOSHBPM"
    CITRIX = "CITRIX"
    CITRIX_COMMON = "CITRIX_COMMON"
    CITRIX_DESKTOP_DELIVERY_CONTROLLERS = "CITRIX_DESKTOP_DELIVERY_CONTROLLERS"
    CITRIX_DIRECTOR = "CITRIX_DIRECTOR"
    CITRIX_LICENSE_SERVER = "CITRIX_LICENSE_SERVER"
    CITRIX_PROVISIONING_SERVICES = "CITRIX_PROVISIONING_SERVICES"
    CITRIX_STOREFRONT = "CITRIX_STOREFRONT"
    CITRIX_VIRTUAL_DELIVERY_AGENT = "CITRIX_VIRTUAL_DELIVERY_AGENT"
    CITRIX_WORKSPACE_ENVIRONMENT_MANAGEMENT = "CITRIX_WORKSPACE_ENVIRONMENT_MANAGEMENT"
    CITRIX_XEN = "CITRIX_XEN"
    CLOUDFOUNDRY = "CLOUDFOUNDRY"
    CLOUDFOUNDRY_AUCTIONEER = "CLOUDFOUNDRY_AUCTIONEER"
    CLOUDFOUNDRY_BOSH = "CLOUDFOUNDRY_BOSH"
    CLOUDFOUNDRY_GOROUTER = "CLOUDFOUNDRY_GOROUTER"
    COLDFUSION = "COLDFUSION"
    CONFLUENT_KAFKA_CLIENT = "CONFLUENT_KAFKA_CLIENT"
    CONTAINERD = "CONTAINERD"
    CORE_DNS = "CORE_DNS"
    COUCHBASE = "COUCHBASE"
    CRIO = "CRIO"
    CXF = "CXF"
    DATASTAX = "DATASTAX"
    DB2 = "DB2"
    DIEGO_CELL = "DIEGO_CELL"
    DOCKER = "DOCKER"
    DOTNET = "DOTNET"
    DOTNET_REMOTING = "DOTNET_REMOTING"
    ELASTIC_SEARCH = "ELASTIC_SEARCH"
    ENVOY = "ENVOY"
    ERLANG = "ERLANG"
    ETCD = "ETCD"
    F5_LTM = "F5_LTM"
    FSHARP = "FSHARP"
    GARDEN = "GARDEN"
    GLASSFISH = "GLASSFISH"
    GO = "GO"
    GRAAL_TRUFFLE = "GRAAL_TRUFFLE"
    GRPC = "GRPC"
    GRSECURITY = "GRSECURITY"
    HADOOP = "HADOOP"
    HADOOP_HDFS = "HADOOP_HDFS"
    HADOOP_YARN = "HADOOP_YARN"
    HAPROXY = "HAPROXY"
    HEAT = "HEAT"
    HESSIAN = "HESSIAN"
    HORNET_Q = "HORNET_Q"
    IBM_CICS_REGION = "IBM_CICS_REGION"
    IBM_CICS_TRANSACTION_GATEWAY = "IBM_CICS_TRANSACTION_GATEWAY"
    IBM_IMS_CONNECT_REGION = "IBM_IMS_CONNECT_REGION"
    IBM_IMS_CONTROL_REGION = "IBM_IMS_CONTROL_REGION"
    IBM_IMS_MESSAGE_PROCESSING_REGION = "IBM_IMS_MESSAGE_PROCESSING_REGION"
    IBM_IMS_SOAP_GATEWAY = "IBM_IMS_SOAP_GATEWAY"
    IBM_INTEGRATION_BUS = "IBM_INTEGRATION_BUS"
    IBM_MQ = "IBM_MQ"
    IBM_MQ_CLIENT = "IBM_MQ_CLIENT"
    IBM_WEBSHPRERE_APPLICATION_SERVER = "IBM_WEBSHPRERE_APPLICATION_SERVER"
    IBM_WEBSHPRERE_LIBERTY = "IBM_WEBSHPRERE_LIBERTY"
    IIS = "IIS"
    IIS_APP_POOL = "IIS_APP_POOL"
    ISTIO = "ISTIO"
    JAVA = "JAVA"
    JAX_WS = "JAX_WS"
    JBOSS = "JBOSS"
    JBOSS_EAP = "JBOSS_EAP"
    JDK_HTTP_SERVER = "JDK_HTTP_SERVER"
    JERSEY = "JERSEY"
    JETTY = "JETTY"
    JRUBY = "JRUBY"
    JYTHON = "JYTHON"
    KUBERNETES = "KUBERNETES"
    LIBC = "LIBC"
    LIBVIRT = "LIBVIRT"
    LINKERD = "LINKERD"
    MARIADB = "MARIADB"
    MEMCACHED = "MEMCACHED"
    MICROSOFT_SQL_SERVER = "MICROSOFT_SQL_SERVER"
    MONGODB = "MONGODB"
    MSSQL_CLIENT = "MSSQL_CLIENT"
    MULE_ESB = "MULE_ESB"
    MYSQL = "MYSQL"
    MYSQL_CONNECTOR = "MYSQL_CONNECTOR"
    NETFLIX_SERVO = "NETFLIX_SERVO"
    NETTY = "NETTY"
    NGINX = "NGINX"
    NODE_JS = "NODE_JS"
    OK_HTTP_CLIENT = "OK_HTTP_CLIENT"
    ONEAGENT_SDK = "ONEAGENT_SDK"
    OPENCENSUS = "OPENCENSUS"
    OPENSHIFT = "OPENSHIFT"
    OPENSTACK_COMPUTE = "OPENSTACK_COMPUTE"
    OPENSTACK_CONTROLLER = "OPENSTACK_CONTROLLER"
    OPENTELEMETRY = "OPENTELEMETRY"
    OPENTRACING = "OPENTRACING"
    OPEN_LIBERTY = "OPEN_LIBERTY"
    ORACLE_DATABASE = "ORACLE_DATABASE"
    ORACLE_WEBLOGIC = "ORACLE_WEBLOGIC"
    OWIN = "OWIN"
    PERL = "PERL"
    PHP = "PHP"
    PHP_FPM = "PHP_FPM"
    PLAY = "PLAY"
    POSTGRE_SQL = "POSTGRE_SQL"
    POSTGRE_SQL_DOTNET_DATA_PROVIDER = "POSTGRE_SQL_DOTNET_DATA_PROVIDER"
    POWER_DNS = "POWER_DNS"
    PROGRESS = "PROGRESS"
    PYTHON = "PYTHON"
    RABBIT_MQ = "RABBIT_MQ"
    REACTOR_CORE = "REACTOR_CORE"
    REDIS = "REDIS"
    RESTEASY = "RESTEASY"
    RESTLET = "RESTLET"
    RIAK = "RIAK"
    RUBY = "RUBY"
    SAG_WEBMETHODS_IS = "SAG_WEBMETHODS_IS"
    SAP = "SAP"
    SAP_HANADB = "SAP_HANADB"
    SAP_HYBRIS = "SAP_HYBRIS"
    SAP_MAXDB = "SAP_MAXDB"
    SAP_SYBASE = "SAP_SYBASE"
    SCALA = "SCALA"
    SELINUX = "SELINUX"
    SHAREPOINT = "SHAREPOINT"
    SPARK = "SPARK"
    SPRING = "SPRING"
    SQLITE = "SQLITE"
    THRIFT = "THRIFT"
    TIBCO = "TIBCO"
    TIBCO_BUSINESS_WORKS = "TIBCO_BUSINESS_WORKS"
    TIBCO_EMS = "TIBCO_EMS"
    UNDERTOW_IO = "UNDERTOW_IO"
    VARNISH_CACHE = "VARNISH_CACHE"
    VIM2 = "VIM2"
    VIRTUAL_MACHINE_KVM = "VIRTUAL_MACHINE_KVM"
    VIRTUAL_MACHINE_QEMU = "VIRTUAL_MACHINE_QEMU"
    WILDFLY = "WILDFLY"
    WINDOWS_CONTAINERS = "WINDOWS_CONTAINERS"
    WINK = "WINK"
    ZERO_MQ = "ZERO_MQ"
    ZOS_CONNECT = "ZOS_CONNECT"

    def __str__(self) -> str:
        return self.value


class SimpleHostTechType(Enum):
    APPARMOR = "APPARMOR"
    BOSH = "BOSH"
    BOSHBPM = "BOSHBPM"
    CLOUDFOUNDRY = "CLOUDFOUNDRY"
    CONTAINERD = "CONTAINERD"
    CRIO = "CRIO"
    DIEGO_CELL = "DIEGO_CELL"
    DOCKER = "DOCKER"
    GARDEN = "GARDEN"
    GRSECURITY = "GRSECURITY"
    KUBERNETES = "KUBERNETES"
    OPENSHIFT = "OPENSHIFT"
    OPENSTACK_COMPUTE = "OPENSTACK_COMPUTE"
    OPENSTACK_CONTROLLER = "OPENSTACK_CONTROLLER"
    SELINUX = "SELINUX"

    def __str__(self) -> str:
        return self.value


class ComparisonBasicType(Enum):
    APPLICATION_TYPE = "APPLICATION_TYPE"
    AZURE_COMPUTE_MODE = "AZURE_COMPUTE_MODE"
    AZURE_SKU = "AZURE_SKU"
    BITNESS = "BITNESS"
    CLOUD_TYPE = "CLOUD_TYPE"
    CUSTOM_APPLICATION_TYPE = "CUSTOM_APPLICATION_TYPE"
    DATABASE_TOPOLOGY = "DATABASE_TOPOLOGY"
    DCRUM_DECODER_TYPE = "DCRUM_DECODER_TYPE"
    ENTITY_ID = "ENTITY_ID"
    HYPERVISOR_TYPE = "HYPERVISOR_TYPE"
    INDEXED_NAME = "INDEXED_NAME"
    INDEXED_STRING = "INDEXED_STRING"
    INDEXED_TAG = "INDEXED_TAG"
    INTEGER = "INTEGER"
    IP_ADDRESS = "IP_ADDRESS"
    MOBILE_PLATFORM = "MOBILE_PLATFORM"
    OS_ARCHITECTURE = "OS_ARCHITECTURE"
    OS_TYPE = "OS_TYPE"
    PAAS_TYPE = "PAAS_TYPE"
    SERVICE_TOPOLOGY = "SERVICE_TOPOLOGY"
    SERVICE_TYPE = "SERVICE_TYPE"
    SIMPLE_HOST_TECH = "SIMPLE_HOST_TECH"
    SIMPLE_TECH = "SIMPLE_TECH"
    STRING = "STRING"
    SYNTHETIC_ENGINE_TYPE = "SYNTHETIC_ENGINE_TYPE"
    TAG = "TAG"

    def __str__(self) -> str:
        return self.value


### COMPARISON OPERATOR ENUMS ###
#################################


class EqualsComparisonOperator(Enum):
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


class TagComparisonOperator(Enum):
    TAG_KEY_EQUALS = "TAG_KEY_EQUALS"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


class IndexedTagComparisonOperator(Enum):
    EXISTS = "EXISTS"
    TAG_KEY_EQUALS = "TAG_KEY_EQUALS"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


class BasicComparisonOperator(Enum):
    EXISTS = "EXISTS"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


class StringComparisonOperator(Enum):
    BEGINS_WITH = "BEGINS_WITH"
    CONTAINS = "CONTAINS"
    ENDS_WITH = "ENDS_WITH"
    REGEX_MATCHES = "REGEX_MATCHES"
    EXISTS = "EXISTS"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


class IpAddressComparisonOperator(Enum):
    IS_IP_IN_RANGE = "IS_IP_IN_RANGE"
    BEGINS_WITH = "BEGINS_WITH"
    CONTAINS = "CONTAINS"
    ENDS_WITH = "ENDS_WITH"
    REGEX_MATCHES = "REGEX_MATCHES"
    EXISTS = "EXISTS"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


class IndexedNameComparisonOperator(Enum):
    CONTAINS = "CONTAINS"
    EXISTS = "EXISTS"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


class IntegerComparisonOperator(Enum):
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LOWER_THAN = "LOWER_THAN"
    LOWER_THAN_OR_EQUAL = "LOWER_THAN_OR_EQUAL"
    EXISTS = "EXISTS"
    EQUALS = "EQUALS"

    def __str__(self) -> str:
        return self.value


### COMPARISON VALUE ENUMS ###
##############################


class ServiceTypeComparisonValue(Enum):
    BACKGROUND_ACTIVITY = "BACKGROUND_ACTIVITY"
    CICS_SERVICE = "CICS_SERVICE"
    CUSTOM_SERVICE = "CUSTOM_SERVICE"
    DATABASE_SERVICE = "DATABASE_SERVICE"
    ENTERPRISE_SERVICE_BUS_SERVICE = "ENTERPRISE_SERVICE_BUS_SERVICE"
    EXTERNAL = "EXTERNAL"
    IBM_INTEGRATION_BUS_SERVICE = "IBM_INTEGRATION_BUS_SERVICE"
    IMS_SERVICE = "IMS_SERVICE"
    MESSAGING_SERVICE = "MESSAGING_SERVICE"
    QUEUE_LISTENER_SERVICE = "QUEUE_LISTENER_SERVICE"
    RMI_SERVICE = "RMI_SERVICE"
    RPC_SERVICE = "RPC_SERVICE"
    WEB_REQUEST_SERVICE = "WEB_REQUEST_SERVICE"
    WEB_SERVICE = "WEB_SERVICE"

    def __str__(self) -> str:
        return self.value


class PaasTypeComparisonValue(Enum):
    AWS_ECS_EC2 = "AWS_ECS_EC2"
    AWS_ECS_FARGATE = "AWS_ECS_FARGATE"
    AWS_LAMBDA = "AWS_LAMBDA"
    AZURE_FUNCTIONS = "AZURE_FUNCTIONS"
    AZURE_WEBSITES = "AZURE_WEBSITES"
    CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
    GOOGLE_APP_ENGINE = "GOOGLE_APP_ENGINE"
    HEROKU = "HEROKU"
    KUBERNETES = "KUBERNETES"
    OPENSHIFT = "OPENSHIFT"

    def __str__(self) -> str:
        return self.value


class CloudTypeComparisonValue(Enum):
    AZURE = "AZURE"
    EC2 = "EC2"
    GOOGLE_CLOUD_PLATFORM = "GOOGLE_CLOUD_PLATFORM"
    OPENSTACK = "OPENSTACK"
    ORACLE = "ORACLE"
    UNRECOGNIZED = "UNRECOGNIZED"

    def __str__(self) -> str:
        return self.value


class AzureSkuComparisonValue(Enum):
    BASIC = "BASIC"
    DYNAMIC = "DYNAMIC"
    FREE = "FREE"
    PREMIUM = "PREMIUM"
    SHARED = "SHARED"
    STANDARD = "STANDARD"

    def __str__(self) -> str:
        return self.value


class AzureComputeModeComparisonValue(Enum):
    DEDICATED = "DEDICATED"
    SHARED = "SHARED"

    def __str__(self) -> str:
        return self.value


class ServiceTopologyComparisonValue(Enum):
    EXTERNAL_SERVICE = "EXTERNAL_SERVICE"
    FULLY_MONITORED = "FULLY_MONITORED"
    OPAQUE_SERVICE = "OPAQUE_SERVICE"

    def __str__(self) -> str:
        return self.value


class DatabaseTopologyComparisonValue(Enum):
    CLUSTER = "CLUSTER"
    EMBEDDED = "EMBEDDED"
    FAILOVER = "FAILOVER"
    IPC = "IPC"
    LOAD_BALANCING = "LOAD_BALANCING"
    SINGLE_SERVER = "SINGLE_SERVER"
    UNSPECIFIED = "UNSPECIFIED"

    def __str__(self) -> str:
        return self.value


class OsTypeComparisonValue(Enum):
    AIX = "AIX"
    DARWIN = "DARWIN"
    HPUX = "HPUX"
    LINUX = "LINUX"
    SOLARIS = "SOLARIS"
    WINDOWS = "WINDOWS"
    ZOS = "ZOS"

    def __str__(self) -> str:
        return self.value


class HypervisorTypeComparisonValue(Enum):
    AHV = "AHV"
    HYPER_V = "HYPER_V"
    KVM = "KVM"
    LPAR = "LPAR"
    QEMU = "QEMU"
    UNRECOGNIZED = "UNRECOGNIZED"
    VIRTUAL_BOX = "VIRTUAL_BOX"
    VMWARE = "VMWARE"
    WPAR = "WPAR"
    XEN = "XEN"

    def __str__(self) -> str:
        return self.value


class OsArchitectureComparisonValue(Enum):
    ARM = "ARM"
    IA64 = "IA64"
    PARISC = "PARISC"
    PPC = "PPC"
    PPCLE = "PPCLE"
    S390 = "S390"
    SPARC = "SPARC"
    X86 = "X86"
    ZOS = "ZOS"

    def __str__(self) -> str:
        return self.value


class BitnessComparisonValue(Enum):
    _32 = "32"
    _64 = "64"

    def __str__(self) -> str:
        return self.value


class ApplicationTypeComparisonValue(Enum):
    AGENTLESS_MONITORING = "AGENTLESS_MONITORING"
    AMP = "AMP"
    AUTO_INJECTED = "AUTO_INJECTED"
    DEFAULT = "DEFAULT"
    SAAS_VENDOR = "SAAS_VENDOR"

    def __str__(self) -> str:
        return self.value


class CustomApplicationTypeComparisonValue(Enum):
    AMAZON_ECHO = "AMAZON_ECHO"
    DESKTOP = "DESKTOP"
    EMBEDDED = "EMBEDDED"
    IOT = "IOT"
    MICROSOFT_HOLOLENS = "MICROSOFT_HOLOLENS"
    UFO = "UFO"

    def __str__(self) -> str:
        return self.value


class MobilePlatformComparisonValue(Enum):
    ANDROID = "ANDROID"
    IOS = "IOS"
    LINUX = "LINUX"
    MAC_OS = "MAC_OS"
    OTHER = "OTHER"
    TVOS = "TVOS"
    WINDOWS = "WINDOWS"

    def __str__(self) -> str:
        return self.value


class DcrumDecoderComparisonValue(Enum):
    ALL_OTHER = "ALL_OTHER"
    CITRIX_APPFLOW = "CITRIX_APPFLOW"
    CITRIX_ICA = "CITRIX_ICA"
    CITRIX_ICA_OVER_SSL = "CITRIX_ICA_OVER_SSL"
    DB2_DRDA = "DB2_DRDA"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    HTTP_EXPRESS = "HTTP_EXPRESS"
    INFORMIX = "INFORMIX"
    MYSQL = "MYSQL"
    ORACLE = "ORACLE"
    SAP_GUI = "SAP_GUI"
    SAP_GUI_OVER_HTTP = "SAP_GUI_OVER_HTTP"
    SAP_GUI_OVER_HTTPS = "SAP_GUI_OVER_HTTPS"
    SAP_HANA_DB = "SAP_HANA_DB"
    SAP_RFC = "SAP_RFC"
    SSL = "SSL"
    TDS = "TDS"

    def __str__(self) -> str:
        return self.value


class SyntheticEngineTypeComparisonValue(Enum):
    CLASSIC = "CLASSIC"
    CUSTOM = "CUSTOM"

    def __str__(self) -> str:
        return self.value
