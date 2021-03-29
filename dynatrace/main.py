import logging
from typing import Dict, Optional

from dynatrace.activegate import ActiveGateService
from dynatrace.cluster_time import ClusterTimeService
from dynatrace.custom_device import CustomDeviceService
from dynatrace.dashboard import DashboardService
from dynatrace.entity import EntityService
from dynatrace.event import EventService
from dynatrace.extension import ExtensionService
from dynatrace.http_client import HttpClient
from dynatrace.metric import MetricService
from dynatrace.plugins import PluginService
from dynatrace.synthetic_third_party import ThirdPartySyntheticTestsService


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
        self.cluster_time: ClusterTimeService = ClusterTimeService(self.__http_client)
        self.custom_devices: CustomDeviceService = CustomDeviceService(self.__http_client)
        self.dashboards: DashboardService = DashboardService(self.__http_client)
        self.entities: EntityService = EntityService(self.__http_client)
        self.events: EventService = EventService(self.__http_client)
        self.extensions: ExtensionService = ExtensionService(self.__http_client)
        self.metrics: MetricService = MetricService(self.__http_client)
        self.plugins: PluginService = PluginService(self.__http_client)
        self.third_part_synthetic_tests: ThirdPartySyntheticTestsService = ThirdPartySyntheticTestsService(self.__http_client)
