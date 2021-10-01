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
from typing import List, Dict, Any, Optional

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.schemas import ConfigurationMetadata

# Schemas and Enums that don't belong to a specific API tag.

#######################################################
###                   SCHEMAS                       ###
#######################################################
class ConfigurationMetadata(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.cluster_version: str = raw_element.get("clusterVersion")
        self.configuration_versions: List[int] = raw_element.get("configurationVersions")
        self.current_configuration_versions: List[str] = raw_element.get("currentConfigurationVersions")


class EntityShortRepresentation(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id = raw_element.get("id")
        self.name = raw_element.get("name")
        self.description = raw_element.get("description")

    def to_json(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "description": self.description}


class UpdateWindowsConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.windows: List[UpdateWindow] = [UpdateWindow(raw_element=uw) for uw in raw_element.get("windows", [])]

    def to_json(self) -> Optional[Dict[str, Any]]:
        if not self.windows:
            return None

        return {"windows": [w.to_json for w in self.windows]}


class UpdateWindow(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id", "")
        self.name: Optional[str] = raw_element.get("name", "")

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
        }


class TechMonitoringList(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.technologies: List[Technology] = [Technology(raw_element=t) for t in raw_element.get("technologies", [])]
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(raw_element=raw_element.get("metadata"))


class Technology(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: TechnologyType = TechnologyType(raw_element.get("type"))
        self.monitoring_enabled: bool = raw_element.get("monitoringEnabled", False)
        self.scope: Optional[SettingScope] = SettingScope(raw_element.get("scope")) if raw_element.get("scope") else None


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


#######################################################
###                    ENUMS                        ###
#######################################################


class SettingScope(Enum):
    ENVIRONMENT = "ENVIRONMENT"
    HOST = "HOST"

    def __str__(self):
        return self.value


class TechnologyType(Enum):
    AIX_KERNEL_EXT = "AIX_KERNEL_EXT"
    APACHE = "APACHE"
    CIM_V2 = "CIM_V2"
    DOCKER = "DOCKER"
    DOCKER_WIN = "DOCKER_WIN"
    DOT_NET = "DOT_NET"
    DOT_NET_CORE = "DOT_NET_CORE"
    EXTENSIONS = "EXTENSIONS"
    EXTENSIONS_DS_GENERIC = "EXTENSIONS_DS_GENERIC"
    EXTENSIONS_STATSD = "EXTENSIONS_STATSD"
    GARDEN = "GARDEN"
    GO = "GO"
    GO_STATIC = "GO_STATIC"
    IBM_INTEGRATION_BUS = "IBM_INTEGRATION_BUS"
    IIS = "IIS"
    JAVA = "JAVA"
    LOG_ANALYTICS = "LOG_ANALYTICS"
    NETTRACER = "NETTRACER"
    NETWORK = "NETWORK"
    NGINX = "NGINX"
    NODE_JS = "NODE_JS"
    OPENTRACINGNATIVE = "OPENTRACINGNATIVE"
    PHP = "PHP"
    PHP_80_EA = "PHP_80_EA"
    PHP_CGI = "PHP_CGI"
    PHP_CLI = "PHP_CLI"
    PHP_WIN = "PHP_WIN"
    PROCESS = "PROCESS"
    RUBY = "RUBY"
    SDK = "SDK"
    VARNISH = "VARNISH"
    Z_OS = "Z_OS"

    def __str__(self):
        return self.value


class AutoUpdateSetting(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    INHERITED = "INHERITED"

    def __str__(self):
        return self.value


class EffectiveSetting(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"

    def __str__(self):
        return self.value


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

class TagContext(Enum):
    AWS = "AWS"
    AWS_GENERIC = "AWS_GENERIC"
    AZURE = "AZURE"
    CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
    CONTEXTLESS = "CONTEXTLESS"
    ENVIRONMENT = "ENVIRONMENT"
    GOOGLE_CLOUD = "GOOGLE_CLOUD"
    KUBERNETES = "KUBERNETES"

    def __str__(self) -> str:
        return self.value


class StringComparisonOperator(Enum):
    BEGINS_WITH = "BEGINS_WITH"
    CONTAINS = "CONTAINS"
    ENDS_WITH = "ENDS_WITH"
    REGEX_MATCHES = "REGEX_MATCHES"
    EXISTS = "EXISTS"
    CONTAINS_REGEX = "CONTAINS_REGEX"
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
