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

import logging
from typing import Dict, Optional

from dynatrace.configuration_v1.alerting_profiles import AlertingProfileService
from dynatrace.configuration_v1.anomaly_detection_process_groups import AnomalyDetectionPGService
from dynatrace.configuration_v1.auto_tags import AutoTagService
from dynatrace.configuration_v1.dashboard import DashboardService
from dynatrace.configuration_v1.extensions import ExtensionService
from dynatrace.configuration_v1.maintenance_windows import MaintenanceWindowService
from dynatrace.configuration_v1.metric_events import MetricEventService
from dynatrace.configuration_v1.notifications import NotificationService
from dynatrace.configuration_v1.plugins import PluginService
from dynatrace.configuration_v1.oneagent_on_a_host import OneAgentOnAHostService as OneAgentOnAHostConfigService
from dynatrace.configuration_v1.oneagent_in_a_hostgroup import OneAgentInAHostGroupService
from dynatrace.configuration_v1.oneagent_environment_wide_configuration import OneAgentEnvironmentWideConfigService
from dynatrace.environment_v1.cluster_time import ClusterTimeService
from dynatrace.environment_v1.custom_device import CustomDeviceService
from dynatrace.environment_v1.event import EventService
from dynatrace.environment_v1.oneagents import OneAgentOnAHostService
from dynatrace.environment_v1.smartscape_hosts import SmartScapeHostsService
from dynatrace.environment_v1.synthetic_monitors import SyntheticMonitorsService
from dynatrace.environment_v1.synthetic_third_party import ThirdPartySyntheticTestsService
from dynatrace.environment_v1.timeseries import TimeSerieService
from dynatrace.environment_v1.deployment import DeploymentService
from dynatrace.environment_v2.activegates import ActiveGateService
from dynatrace.environment_v2.activegates_autoupdate_configuration import ActiveGateAutoUpdateConfigurationService
from dynatrace.environment_v2.activegates_autoupdate_jobs import ActiveGateAutoUpdateJobsService
from dynatrace.environment_v2.audit_logs import AuditLogsService
from dynatrace.environment_v2.extensions import ExtensionsServiceV2
from dynatrace.environment_v2.events import EventServiceV2
from dynatrace.environment_v2.monitored_entities import EntityService
from dynatrace.environment_v2.custom_tags import CustomTagService
from dynatrace.environment_v2.metrics import MetricService
from dynatrace.environment_v2.networkzones import NetworkZoneService
from dynatrace.environment_v2.tokens_api import TokenService
from dynatrace.environment_v2.tokens_tenant import TenantTokenService
from dynatrace.environment_v2.problems import ProblemService
from dynatrace.environment_v2.service_level_objectives import SloService
from dynatrace.http_client import HttpClient


class Dynatrace:
    def __init__(
        self,
        base_url: str,
        token: str,
        log: logging.Logger = None,
        proxies: Dict = None,
        too_many_requests_strategy=None,
        retries: int = 0,
        retry_delay_ms: int = 0,
        mc_jsession_id: Optional[str] = None,
        mc_b925d32c: Optional[str] = None,
        mc_sso_csrf_cookie: Optional[str] = None,
    ):
        self.__http_client = HttpClient(
            base_url,
            token,
            log,
            proxies,
            too_many_requests_strategy,
            retries,
            retry_delay_ms,
            mc_jsession_id,
            mc_b925d32c,
            mc_sso_csrf_cookie,
        )

        self.activegates: ActiveGateService = ActiveGateService(self.__http_client)
        self.activegates_autoupdate_configuration: ActiveGateAutoUpdateConfigurationService = ActiveGateAutoUpdateConfigurationService(self.__http_client)
        self.activegates_autoupdate_jobs = ActiveGateAutoUpdateJobsService(self.__http_client)
        self.alerting_profiles: AlertingProfileService = AlertingProfileService(self.__http_client)
        self.anomaly_detection_metric_events = MetricEventService(self.__http_client)
        self.anomaly_detection_process_groups = AnomalyDetectionPGService(self.__http_client)
        self.audit_logs: AuditLogsService = AuditLogsService(self.__http_client)
        self.auto_tags: AutoTagService = AutoTagService(self.__http_client)
        self.cluster_time: ClusterTimeService = ClusterTimeService(self.__http_client)
        self.custom_devices: CustomDeviceService = CustomDeviceService(self.__http_client)
        self.custom_tags: CustomTagService = CustomTagService(self.__http_client)
        self.dashboards: DashboardService = DashboardService(self.__http_client)
        self.deployment: DeploymentService = DeploymentService(self.__http_client)
        self.entities: EntityService = EntityService(self.__http_client)
        self.events: EventService = EventService(self.__http_client)
        self.events_v2: EventServiceV2 = EventServiceV2(self.__http_client)
        self.extensions: ExtensionService = ExtensionService(self.__http_client)
        self.extensions_v2: ExtensionsServiceV2 = ExtensionsServiceV2(self.__http_client)
        self.maintenance_windows = MaintenanceWindowService(self.__http_client)
        self.metrics: MetricService = MetricService(self.__http_client)
        self.network_zones: NetworkZoneService = NetworkZoneService(self.__http_client)
        self.notifications: NotificationService = NotificationService(self.__http_client)
        self.oneagents: OneAgentOnAHostService = OneAgentOnAHostService(self.__http_client)
        self.oneagents_config_environment: OneAgentEnvironmentWideConfigService = OneAgentEnvironmentWideConfigService(self.__http_client)
        self.oneagents_config_host: OneAgentOnAHostConfigService = OneAgentOnAHostConfigService(self.__http_client)
        self.oneagents_config_hostgroup: OneAgentInAHostGroupService = OneAgentInAHostGroupService(self.__http_client)
        self.plugins: PluginService = PluginService(self.__http_client)
        self.problems: ProblemService = ProblemService(self.__http_client)
        self.slos: SloService = SloService(self.__http_client)
        self.smartscape_hosts: SmartScapeHostsService = SmartScapeHostsService(self.__http_client)
        self.synthetic_monitors: SyntheticMonitorsService = SyntheticMonitorsService(self.__http_client)
        self.tenant_tokens = TenantTokenService(self.__http_client)
        self.third_part_synthetic_tests: ThirdPartySyntheticTestsService = ThirdPartySyntheticTestsService(self.__http_client)
        self.timeseries: TimeSerieService = TimeSerieService(self.__http_client)
        self.tokens: TokenService = TokenService(self.__http_client)
