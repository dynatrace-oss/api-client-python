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
from typing import Dict, Any, List, Optional

from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.configuration_v1 import schemas


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

    def post(self, management_zone: "ManagementZone") -> "schemas.EntityShortRepresentation":
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


class ManagementZoneStub(schemas.EntityShortRepresentation):
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
        self.metadata: Optional[schemas.ConfigurationMetadata] = schemas.ConfigurationMetadata(raw_element=raw_element.get("metadata"))
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

    def post(self) -> "schemas.EntityShortRepresentation":
        """Creates this Management Zone in Dynatrace (POST).

        :returns EntityShortRepresentation: basic detail of the created Management Zone

        :throws ValueError: if operation cannot be executed due to missing HTTP Client
        """
        if not self._http_client:
            raise ValueError("Object does not have HTTP Client. Use management_zones.post() instead.")
        response = self._http_client.make_request(path=ManagementZoneService.ENDPOINT, params=self.to_json(), method="POST")
        self.id = response.json().get("id")

        return schemas.EntityShortRepresentation(raw_element=response.json())

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
            schemas.ComparisonBasicType.APPLICATION_TYPE: schemas.ApplicationTypeComparison,
            schemas.ComparisonBasicType.AZURE_COMPUTE_MODE: schemas.AzureComputeModeComparison,
            schemas.ComparisonBasicType.AZURE_SKU: schemas.AzureSkuComparison,
            schemas.ComparisonBasicType.BITNESS: schemas.BitnessComparison,
            schemas.ComparisonBasicType.CLOUD_TYPE: schemas.CloudTypeComparison,
            schemas.ComparisonBasicType.CUSTOM_APPLICATION_TYPE: schemas.CustomApplicationTypeComparison,
            schemas.ComparisonBasicType.DATABASE_TOPOLOGY: schemas.DatabaseTopologyComparison,
            schemas.ComparisonBasicType.DCRUM_DECODER_TYPE: schemas.DcrumDecoderComparison,
            schemas.ComparisonBasicType.ENTITY_ID: schemas.EntityIdComparison,
            schemas.ComparisonBasicType.HYPERVISOR_TYPE: schemas.HypervisorTypeComparison,
            schemas.ComparisonBasicType.INDEXED_NAME: schemas.IndexedNameComparison,
            schemas.ComparisonBasicType.INDEXED_STRING: schemas.IndexedStringComparison,
            schemas.ComparisonBasicType.INDEXED_TAG: schemas.IndexedTagComparison,
            schemas.ComparisonBasicType.INTEGER: schemas.IntegerComparison,
            schemas.ComparisonBasicType.IP_ADDRESS: schemas.IpAddressComparison,
            schemas.ComparisonBasicType.MOBILE_PLATFORM: schemas.MobilePlatformComparison,
            schemas.ComparisonBasicType.OS_ARCHITECTURE: schemas.OsArchitectureComparison,
            schemas.ComparisonBasicType.OS_TYPE: schemas.OsTypeComparison,
            schemas.ComparisonBasicType.PAAS_TYPE: schemas.PaasTypeComparison,
            schemas.ComparisonBasicType.SERVICE_TOPOLOGY: schemas.ServiceTopologyComparison,
            schemas.ComparisonBasicType.SERVICE_TYPE: schemas.ServiceTypeComparison,
            schemas.ComparisonBasicType.SIMPLE_HOST_TECH: schemas.SimpleHostTechComparison,
            schemas.ComparisonBasicType.SIMPLE_TECH: schemas.SimpleTechComparison,
            schemas.ComparisonBasicType.STRING: schemas.StringComparison,
            schemas.ComparisonBasicType.SYNTHETIC_ENGINE_TYPE: schemas.SyntheticEngineTypeComparison,
            schemas.ComparisonBasicType.TAG: schemas.TagComparison,
        }

        self.key: ConditionKey = condition_key_types[MzConditionType(raw_element["key"]["type"])](raw_element=raw_element["key"])
        self.comparison_info: schemas.ComparisonBasic = comparison_types[schemas.ComparisonBasicType(raw_element["comparisonInfo"]["type"])](
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


class CustomProcessMetadataConditionKey(ConditionKey):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.dynamic_key: schemas.CustomProcessMetadataKey = schemas.CustomProcessMetadataKey(raw_element=raw_element["dynamicKey"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"dynamicKey": self.dynamic_key.to_json()})
        return details


class CustomHostMetadataConditionKey(ConditionKey):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.dynamic_key: schemas.CustomHostMetadataKey = schemas.CustomHostMetadataKey(raw_element=raw_element["dynamicKey"])

    def to_json(self) -> Dict[str, Any]:
        details = super().to_json()
        details.update({"dynamicKey": self.dynamic_key.to_json()})
        return details


class ProcessMetadataConditionKey(ConditionKey):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.dynamic_key: schemas.PredefinedProcessMetadataKeySource = schemas.PredefinedProcessMetadataKeySource(raw_element["dynamicKey"])

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
