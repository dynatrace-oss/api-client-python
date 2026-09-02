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
from typing import List, Optional, Union
from datetime import datetime

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.utils import datetime_to_int64

from dynatrace.environment_v1.smartscape_hosts import AgentVersion, HostGroup, MonitoringMode, OSArchitecture, TagInfo
from dynatrace.environment_v2.custom_tags import METag
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation


class UpdateStatus(Enum):
    INCOMPATIBLE = "INCOMPATIBLE"
    OUTDATED = "OUTDATED"
    SCHEDULED = "SCHEDULED"
    SUPPRESSED = "SUPPRESSED"
    UNKNOWN = "UNKNOWN"
    UP2DATE = "UP2DATE"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_PENDING = "UPDATE_PENDING"
    UPDATE_PROBLEM = "UPDATE_PROBLEM"
    NONE = None


class MonitoringType(Enum):
    CLOUD_INFRASTRUCTURE = "CLOUD_INFRASTRUCTURE"
    DISCOVERY = "DISCOVERY"
    FULL_STACK = "FULL_STACK"
    STANDALONE = "STANDALONE"


class AvailabilityState(Enum):
    MONITORED = "MONITORED"
    UNMONITORED = "UNMONITORED"
    CRASHED = "CRASHED"
    LOST = "LOST"
    PRE_MONITORED = "PRE_MONITORED"
    SHUTDOWN = "SHUTDOWN"
    UNEXPECTED_SHUTDOWN = "UNEXPECTED_SHUTDOWN"
    UNKNOWN = "UNKNOWN"


class AutoUpdate(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class OsType(Enum):
    AIX = "AIX"
    LINUX = "LINUX"
    WINDOWS = "WINDOWS"
    SOLARIS = "SOLARIS"
    ZOS = "ZOS"


class CloudType(Enum):
    AZURE = "AZURE"
    EC2 = "EC2"
    GOOGLE_CLOUD_PLATFORM = "GOOGLE_CLOUD_PLATFORM"
    OPENSTACK = "OPENSTACK"
    ORACLE = "ORACLE"
    UNRECOGNIZED = "UNRECOGNIZED"


class AutoInjection(Enum):
    DISABLED_MANUALLY = "DISABLED_MANUALLY"
    DISABLED_ON_INSTALLATION = "DISABLED_ON_INSTALLATION"
    DISABLED_ON_SANITY_CHECK = "DISABLED_ON_SANITY_CHECK"
    ENABLED = "ENABLED"
    FAILED_ON_INSTALLATION = "FAILED_ON_INSTALLATION"


class DetailedAvailabilityState(Enum):
    CRASHED_FAILURE = "CRASHED_FAILURE"
    CRASHED_UNKNOWN = "CRASHED_UNKNOWN"
    LOST_AGENT_UPGRADE_FAILED = "LOST_AGENT_UPGRADE_FAILED"
    LOST_CONNECTION = "LOST_CONNECTION"
    LOST_UNKNOWN = "LOST_UNKNOWN"
    MONITORED = "MONITORED"
    MONITORED_AGENT_ENABLED = "MONITORED_AGENT_ENABLED"
    MONITORED_AGENT_REGISTERED = "MONITORED_AGENT_REGISTERED"
    MONITORED_AGENT_UPGRADE_STARTED = "MONITORED_AGENT_UPGRADE_STARTED"
    MONITORED_AGENT_VERSION_ACCEPTED = "MONITORED_AGENT_VERSION_ACCEPTED"
    MONITORED_ENABLED = "MONITORED_ENABLED"
    PRE_MONITORED = "PRE_MONITORED"
    SHUTDOWN_AGENT_LOST = "SHUTDOWN_AGENT_LOST"
    SHUTDOWN_GRACEFUL = "SHUTDOWN_GRACEFUL"
    SHUTDOWN_K8S_NODE_SHUTDOWN = "SHUTDOWN_K8S_NODE_SHUTDOWN"
    SHUTDOWN_SPOT_INSTANCE = "SHUTDOWN_SPOT_INSTANCE"
    SHUTDOWN_STOPPED = "SHUTDOWN_STOPPED"
    SHUTDOWN_UNKNOWN = "SHUTDOWN_UNKNOWN"
    SHUTDOWN_UNKNOWN_UNEXPECTED = "SHUTDOWN_UNKNOWN_UNEXPECTED"
    UNKNOWN = "UNKNOWN"
    UNMONITORED_AGENT_DISABLED = "UNMONITORED_AGENT_DISABLED"
    UNMONITORED_AGENT_LOST = "UNMONITORED_AGENT_LOST"
    UNMONITORED_AGENT_MIGRATED = "UNMONITORED_AGENT_MIGRATED"
    UNMONITORED_AGENT_RESTART_TRIGGERED = "UNMONITORED_AGENT_RESTART_TRIGGERED"
    UNMONITORED_AGENT_STOPPED = "UNMONITORED_AGENT_STOPPED"
    UNMONITORED_AGENT_UNINSTALLED = "UNMONITORED_AGENT_UNINSTALLED"
    UNMONITORED_AGENT_UNREGISTERED = "UNMONITORED_AGENT_UNREGISTERED"
    UNMONITORED_AGENT_UPGRADE_FAILED = "UNMONITORED_AGENT_UPGRADE_FAILED"
    UNMONITORED_AGENT_VERSION_REJECTED = "UNMONITORED_AGENT_VERSION_REJECTED"
    UNMONITORED_DISABLED = "UNMONITORED_DISABLED"
    UNMONITORED_ID_CHANGED = "UNMONITORED_ID_CHANGED"
    UNMONITORED_TERMINATED = "UNMONITORED_TERMINATED"
    UNMONITORED_UNKNOWN = "UNMONITORED_UNKNOWN"


class VersionIs(Enum):
    EQUAL = "EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LOWER = "LOWER"
    LOWER_EQUAL = "LOWER_EQUAL"


class TechnologyModuleType(Enum):
    APACHE = "APACHE"
    DOT_NET = "DOT_NET"
    DUMPPROC = "DUMPPROC"
    GO = "GO"
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
    PROCESS = "PROCESS"
    PYTHON = "PYTHON"
    RUBY = "RUBY"
    SDK = "SDK"
    UPDATER = "UPDATER"
    VARNISH = "VARNISH"
    Z_OS = "Z_OS"


class PluginState(Enum):
    DISABLED = "DISABLED"
    ERROR_AUTH = "ERROR_AUTH"
    ERROR_COMMUNICATION_FAILURE = "ERROR_COMMUNICATION_FAILURE"
    ERROR_CONFIG = "ERROR_CONFIG"
    ERROR_TIMEOUT = "ERROR_TIMEOUT"
    ERROR_UNKNOWN = "ERROR_UNKNOWN"
    INCOMPATIBLE = "INCOMPATIBLE"
    LIMIT_REACHED = "LIMIT_REACHED"
    NOTHING_TO_REPORT = "NOTHING_TO_REPORT"
    OK = "OK"
    STATE_TYPE_UNKNOWN = "STATE_TYPE_UNKNOWN"
    UNINITIALIZED = "UNINITIALIZED"
    UNSUPPORTED = "UNSUPPORTED"
    WAITING_FOR_STATE = "WAITING_FOR_STATE"


class AzureComputeModeName(Enum):
    DEDICATED = "DEDICATED"
    SHARED = "SHARED"


class AzureSku(Enum):
    BASIC = "BASIC"
    DYNAMIC = "DYNAMIC"
    FREE = "FREE"
    PREMIUM = "PREMIUM"
    SHARED = "SHARED"
    STANDARD = "STANDARD"


class Bitness(Enum):
    x32bit = "32bit"
    x64bit = "64bit"


class HypervisorType(Enum):
    AHV = "AHV"
    AWS_NITRO = "AWS_NITRO"
    GVISOR = "GVISOR"
    HYPERV = "HYPERV"
    KVM = "KVM"
    LPAR = "LPAR"
    QEMU = "QEMU"
    UNRECOGNIZED = "UNRECOGNIZED"
    VIRTUALBOX = "VIRTUALBOX"
    VMWARE = "VMWARE"
    WPAR = "WPAR"
    XEN = "XEN"


class PaasType(Enum):
    AWS_ECS_EC2 = "AWS_ECS_EC2"
    AWS_ECS_FARGATE = "AWS_ECS_FARGATE"
    AWS_LAMBDA = "AWS_LAMBDA"
    AZURE_FUNCTIONS = "AZURE_FUNCTIONS"
    AZURE_WEBSITES = "AZURE_WEBSITES"
    CLOUD_FOUNDRY = "CLOUD_FOUNDRY"
    GOOGLE_APP_ENGINE = "GOOGLE_APP_ENGINE"
    GOOGLE_CLOUD_RUN = "GOOGLE_CLOUD_RUN"
    HEROKU = "HEROKU"
    KUBERNETES = "KUBERNETES"
    OPENSHIFT = "OPENSHIFT"


class UserLevel(Enum):
    NON_SUPERUSER = "NON_SUPERUSER"
    NON_SUPERUSER_STRICT = "NON_SUPERUSER_STRICT"
    SUPERUSER = "SUPERUSER"


# https://docs.dynatrace.com/docs/dynatrace-api/environment-api/oneagent-on-a-host/get-all-hosts-with-oneagents
class OneAgentOnAHostService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        include_details: Optional[bool] = None,
        start_timestamp: Optional[Union[datetime, int]] = None,
        end_timestamp: Optional[Union[datetime, int]] = None,
        relative_time: Optional[str] = None,
        tag: Optional[List[str]] = None,
        entity: Optional[List[str]] = None,
        mz_id: Optional[str] = None, # must be parseable as integer
        management_zone: Optional[str] = None,
        network_zone_id: Optional[str] = None,
        host_group_id: Optional[str] = None,
        host_group_name: Optional[str] = None,
        os_type: Optional[Union[OsType, str]] = None,
        cloud_type: Optional[Union[CloudType, str]] = None,
        auto_injection: Optional[Union[AutoInjection, str]] = None,
        availability_state: Optional[Union[AvailabilityState, str]] = None,
        detailed_availability_state: Optional[Union[DetailedAvailabilityState, str]] = None,
        monitoring_type: Optional[Union[MonitoringType, str]] = None,
        agent_version_is: Optional[Union[VersionIs, str]] = None,
        agent_version_number: Optional[str] = None,
        auto_update: Optional[Union[AutoUpdate, str]] = None,
        update_status: Optional[Union[UpdateStatus, str]] = None,
        faulty_version: Optional[bool] = None,
        unlicensed: Optional[bool] = None,
        activegate_id: Optional[str] = None, # Use "DIRECT_COMMUNICATION" keyword to find the hosts not connected to any ActiveGate.
        technology_module_type: Optional[Union[TechnologyModuleType, str]] = None,
        technology_module_version_is: Optional[Union[VersionIs, str]] = None,
        technology_module_version_number: Optional[str] = None,
        technology_module_faulty_version: Optional[bool] = None,
        plugin_name: Optional[str] = None,
        plugin_version_is: Optional[Union[VersionIs, str]] = None,
        plugin_version_number: Optional[str] = None,
        plugin_state: Optional[Union[PluginState, str]] = None,
    ) -> PaginatedList["HostAgentInfo"]:
        """
        Lists OneAgents on a Host. Older API - timestamps are of type integer and therefore require conversion
        """
        params = {
            "includeDetails": include_details,
            "startTimestamp": datetime_to_int64(start_timestamp),
            "endTimestamp": datetime_to_int64(end_timestamp),
            "relativeTime": relative_time,
            "tag": tag,
            "entity": entity,
            "managementZoneId": mz_id,
            "managementZone": management_zone,
            "networkZoneId": network_zone_id,
            "hostGroupId": host_group_id,
            "hostGroupName": host_group_name,
            "osType": OsType(os_type).value if os_type else None,
            "cloudType": CloudType(cloud_type).value if cloud_type else None,
            "autoInjection": AutoInjection(auto_injection).value if auto_injection else None,
            "availabilityState": AvailabilityState(availability_state).value if availability_state else None,
            "detailedAvailabilityState": DetailedAvailabilityState(detailed_availability_state).value if detailed_availability_state else None,
            "monitoringType": MonitoringType(monitoring_type).value if monitoring_type else None,
            "agentVersionIs": VersionIs(agent_version_is).value if agent_version_is else None,
            "agentVersionNumber": agent_version_number,
            "autoUpdateSetting": AutoUpdate(auto_update).value if auto_update else None,
            "updateStatus": UpdateStatus(update_status).value if update_status else None,
            "faultyVersion": faulty_version,
            "unlicensed": unlicensed,
            "activeGateId": activegate_id,
            "technologyModuleType": TechnologyModuleType(technology_module_type).value if technology_module_type else None,
            "technologyModuleVersionIs": VersionIs(technology_module_version_is).value if technology_module_version_is else None,
            "technologyModuleVersionNumber": technology_module_version_number,
            "technologyModuleFaultyVersion": technology_module_faulty_version,
            "pluginName": plugin_name,
            "pluginVersionIs": VersionIs(plugin_version_is).value if plugin_version_is else None,
            "pluginVersionNumber": plugin_version_number,
            "pluginState": plugin_state,
        }
        return PaginatedList(HostAgentInfo, self.__http_client, "/api/v1/oneagents", params, list_item="hosts")


class HostAgentInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.active: bool = raw_element.get("active")
        self.auto_update: AutoUpdate = AutoUpdate(raw_element.get("autoUpdateSetting"))
        self.availability_state: AvailabilityState = AvailabilityState(raw_element.get("availabilityState"))
        self.available_versions: str = raw_element.get("availableVersions", [])
        self.config_monitoring_enabled: bool = raw_element.get("configuredMonitoringEnabled")
        self.configured_monitoring_mode: MonitoringType = MonitoringType(raw_element.get("configuredMonitoringMode"))
        self.activegate_id: Optional[int] = raw_element.get("currentActiveGateId") # DEPRECATED
        self.current_activegate_ids: List[str] = raw_element.get("currentActiveGateIds")
        self.networkzone_id: str = raw_element.get("currentNetworkZoneId")
        self.detailed_availability_state: DetailedAvailabilityState = DetailedAvailabilityState(raw_element.get("detailedAvailabilityState"))
        self.faulty_version: bool = raw_element.get("faultyVersion")
        self.host_info: HostInfo = HostInfo(raw_element=raw_element.get("hostInfo"))
        self.modules: List[ModuleInfo] = [ModuleInfo(raw_element=mi) for mi in raw_element.get("modules",[])]
        self.monitoring_type: Optional[MonitoringType] = MonitoringType(raw_element.get("monitoringType"))  if raw_element.get("monitoringType") else None
        self.plugins: List[PluginInfo] = [PluginInfo(raw_element=pi) for pi in raw_element.get("plugins",[])]
        self.unlicensed: bool = raw_element.get("unlicensed")
        self.update_status: UpdateStatus = UpdateStatus(raw_element.get("updateStatus"))


class HostInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.agent_version: AgentVersion = AgentVersion(raw_element.get("agentVersion"))
        self.ami_id: Optional[str] = raw_element.get("amiId")
        self.auto_injection: Optional[AutoInjection] = AutoInjection(raw_element.get("autoInjection")) if raw_element.get("autoInjection") else None 
        self.auto_scaling_group: Optional[str] = raw_element.get("autoScalingGroup")
        self.aws_instance_id: Optional[str] = raw_element.get("awsInstanceId")
        self.aws_instance_type: Optional[str] = raw_element.get("awsInstanceType")
        self.aws_name_tag: Optional[str] = raw_element.get("awsNameTag")
        self.aws_security_group: Optional[List[str]] = raw_element.get("awsSecurityGroup")
        self.azure_compute_mode_name: Optional[AzureComputeModeName] = AzureComputeModeName(raw_element.get("azureComputeModeName")) if raw_element.get("azureComputeModeName") else None
        self.azure_environment: Optional[str] = raw_element.get("azureEnvironment")
        self.azure_host_names: Optional[List[str]] = raw_element.get("azureHostNames")
        self.azure_resource_group_namet: Optional[str] = raw_element.get("azureResourceGroupName")
        self.azure_resourceId: Optional[str] = raw_element.get("azureResourceId")
        self.azure_site_names: Optional[List[str]] = raw_element.get("azureSiteNames")
        self.azure_sku: Optional[AzureSku] = AzureSku(raw_element.get("azureSku")) if raw_element.get("azureSku") else None
        self.azure_vm_name: Optional[str] = raw_element.get("azureVmName")
        self.azure_vm__scale_set_name: Optional[str] = raw_element.get("azureVmScaleSetName")
        self.azure_vm_size_label: Optional[str] = raw_element.get("azureVmSizeLabel")
        self.azure_zone: Optional[str] = raw_element.get("azureZone")

        self.beanstalk_environment_name: Optional[str] = raw_element.get("beanstalkEnvironmentName")
        self.bitness: Optional[Bitness] = Bitness(raw_element.get("bitness")) if raw_element.get("bitness") else None
        self.bosh_availability_zone: Optional[str] = raw_element.get("boshAvailabiityZone")
        self.bosh_deployment_id: Optional[str] = raw_element.get("boshDeploymentId")
        self.bosh_instance_id: Optional[str] = raw_element.get("boshInstanceId")
        self.bosh_instance_name: Optional[str] = raw_element.get("boshInstanceName")
        self.bosh_name: Optional[str] = raw_element.get("boshName")
        self.bosh_stem_cell_version: Optional[str] = raw_element.get("boshStemCellVersion")

        self.cloud_platform_verndorversion: Optional[str] = raw_element.get("cloudPlatformVendorVersion")
        self.cloud_type: Optional[CloudType] = CloudType(raw_element.get("cloudType")) if raw_element.get("cloudTupe") else None
        self.consumed_host_units: str = raw_element.get("consumedHostUnits")
        self.cpu_cores: int = raw_element.get("cpuCores")
        self.customized_name: str = raw_element.get("customizedName")

        self.discovered_name: str = raw_element.get("discoveredName")
        self.display_name: str = raw_element.get("displayName")

        self.entity_id: str = raw_element.get("entityId")
        self.esxi_host_name: Optional[str] = raw_element.get("esxiHostName")

        self.first_seen_timestamp: int = raw_element.get("firstSeenTimestamp")
        self.from_relationships: Optional[any] = raw_element.get("fromRelationships")

        self.gce_instance_id: Optional[str] = raw_element.get("gceInstanceId")
        self.gce_instance_name: Optional[str] = raw_element.get("gceInstanceName")
        self.gce_machine_type: Optional[str] = raw_element.get("gceMachineType")
        self.gce_project: Optional[str] = raw_element.get("gceProject")
        self.gce_project_id: Optional[str] = raw_element.get("gceProjectId")
        self.gce_public_ipaddresses: Optional[List[str]] = raw_element.get("gcePublicIpAddresses")
        self.gcp_zone: Optional[str] = raw_element.get("gcpZone")

        self.host_group: HostGroup = HostGroup(raw_element=raw_element.get("hostGroup"))
        self.hypervisor_type: Optiona[HypervisorType] = HypervisorType(raw_element.get("hypervisorType")) if raw_element.get("hypervisorType") else None

        self.ip_addresses: Optional[List[str]] = raw_element.get("ipAddresses")
        self.is_monitoring_candidate: bool = raw_element.get("isMonitoringCandidate")

        self.kubernetes_cluster: Optional[str] = raw_element.get("kubernetesCluster")
        self.kubernetes_labels: Optional[any] = raw_element.get("kubernetesLabels")
        self.kubernetes_node: Optional[str] = raw_element.get("kubernetesNode")

        self.last_seen_timestamp: int = raw_element.get("lastSeenTimestamp")
        self.local_host_name: str = raw_element.get("localHostName")
        self.local_ip: str = raw_element.get("localIp")

        self.logical_cpu_cores: int = raw_element.get("logicalCpuCores")
        self.logical_cpus: int = raw_element.get("logicalCpus")

        self.management_zones: List[EntityShortRepresentation] = [EntityShortRepresentation(raw_element=esr) for esr in raw_element.get("managementZones",[])]
        self.monitoring_mode: MonitoringMode = MonitoringMode(raw_element.get("monitoringMode"))

        self.network_zone_id: str = raw_element.get("networkZoneId")

        self.one_agent_custom_host_name: str = raw_element.get("oneAgentCustomHostName")
        self.openstack_instance_type: str = raw_element.get("openStackInstanceType")
        self.openstack_av_zone: str = raw_element.get("openstackAvZone")
        self.openstack_compute_node_name: str = raw_element.get("openstackComputeNodeName")
        self.openstack_project_name: str = raw_element.get("openstackProjectName")
        self.openstack_security_groups: str = raw_element.get("openstackSecurityGroups")
        self.openstack_vm_name: str = raw_element.get("openstackVmName")
        self.os_architecture: Optional[OSArchitecture] = OSArchitecture(raw_element.get("osArchitecture")) if raw_element.get("osArchitecture") else None
        self.os_type: Optional[OsType] = OsType(raw_element.get("osType")) if raw_element.get("osType") else None
        self.os_version: str = raw_element.get("osVersion")

        self.paas_agent_versions : List[AgentVersion] = [AgentVersion(raw_element=pav) for pav in raw_element.get("paasAgentVersions",[])]
        self.paas_memory_limit: Optional[int] = raw_element.get("paasMemoryLimit")
        self.paas_type: Optional[PaasType] = PaasType(raw_element.get("paasType")) if raw_element.get("paasType") else None
        self.public_host_name: str = raw_element.get("publicHostName")
        self.public_ip: str = raw_element.get("publicIp")

        self.scale_set_name: str = raw_element.get("scaleSetName")
        self.simultaneous_multi_threading: Optional[int] = raw_element.get("simultaneousMultiThreading")
        self.software_technologies: List[TechnologyInfo] = [TechnologyInfo(raw_element=ti) for ti in raw_element.get("softwareTechnologies",[])]

        self.tags: List[METag] = [METag(raw_element=t) for t in raw_element.get("tags", [])]
        self.to_relationships: Optional[any] = raw_element.get("toRelationships")

        self.user_level: Optional[UserLevel] =  UserLevel(raw_element.get("userLevel")) if raw_element.get("userLevel") else None

        self.virtual_cpus: Optional[int] = raw_element.get("virtualCpus")
        self.vmware_name: Optional[str] = raw_element.get("vmwareName")

        self.zos_cpu_model_number: Optional[str] = raw_element.get("zosCPUModelNumber")
        self.zos_cpu_serial_number: Optional[str] = raw_element.get("zosCPUSerialNumber")
        self.zos_lpa_name: Optional[str] = raw_element.get("zosLpaName")
        self.zos_system_name: Optional[str] = raw_element.get("zosSystemName")
        self.zos_total_general_purpose_processors: Optional[int] = raw_element.get("zosTotalGeneralPurposeProcessors")
        self.zos_total_physical_memory: Optional[int] = raw_element.get("zosTotalPhysicalMemory")
        self.zos_total_ziip_processors: Optional[int] = raw_element.get("zosTotalZiipProcessors")
        self.zos_virtualization: Optional[str] = raw_element.get("zosVirtualization")


class TechnologyInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.edition: str = raw_element.get("edition")
        self.type: str = raw_element.get("type")
        self.version: str = raw_element.get("version")

        
class ModuleInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.instances: List[ModuleInstance] = [ModuleInstance(raw_element=i) for i in raw_element.get("instances",[])]
        self.module_type: str = raw_element.get("moduleType")


class ModuleInstance(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.active: bool = raw_element.get("active")
        self.faulty_version: bool = raw_element.get("faulty_Version")
        self.instance_name: str = raw_element.get("instanceName")
        self.module_version: str = raw_element.get("moduleVersion")
        
        
class PluginInfo(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.instances: List[PluginInstance] = [PluginInstance(raw_element=i) for i in raw_element.get("instances",[])]
        self.plugin_name: str = raw_element.get("pluginName")


class PluginInstance(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.plugin_version: str = raw_element.get("pluginVersion")
        self.state: PluginState = PluginState(raw_element.get("state"))
