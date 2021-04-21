import logging
from typing import Dict, Optional

from dynatrace.configuration_v1.dashboard import DashboardService
from dynatrace.configuration_v1.plugins import PluginService
from dynatrace.environment_v1.cluster_time import ClusterTimeService
from dynatrace.environment_v1.custom_device import CustomDeviceService
from dynatrace.environment_v1.event import EventService
from dynatrace.environment_v1.synthetic_third_party import ThirdPartySyntheticTestsService
from dynatrace.environment_v2.activegate import ActiveGateService
from dynatrace.environment_v2.activegate_autoupdate import ActiveGateAutoUpdateService
from dynatrace.environment_v2.entity import EntityService
from dynatrace.environment_v2.extension import ExtensionService
from dynatrace.environment_v2.metric import MetricService
from dynatrace.environment_v2.token import TokenService
from dynatrace.configuration_v1.maintenance_windows import MaintenanceWindowService
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
        self.activegates_autoupdate: ActiveGateAutoUpdateService = ActiveGateAutoUpdateService(self.__http_client)
        self.cluster_time: ClusterTimeService = ClusterTimeService(self.__http_client)
        self.custom_devices: CustomDeviceService = CustomDeviceService(self.__http_client)
        self.dashboards: DashboardService = DashboardService(self.__http_client)
        self.entities: EntityService = EntityService(self.__http_client)
        self.events: EventService = EventService(self.__http_client)
        self.extensions: ExtensionService = ExtensionService(self.__http_client)
        self.metrics: MetricService = MetricService(self.__http_client)
        self.plugins: PluginService = PluginService(self.__http_client)
        self.third_part_synthetic_tests: ThirdPartySyntheticTestsService = ThirdPartySyntheticTestsService(self.__http_client)
        self.tokens: TokenService = TokenService(self.__http_client)
        self.maintenance_windows = MaintenanceWindowService(self.__http_client)
