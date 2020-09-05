import logging
from typing import Dict, Optional

from dynatrace.http_client import HttpClient
from dynatrace.entity import Entity
from dynatrace.entity_type import EntityType
from dynatrace.metric import Metric
from dynatrace.pagination import PaginatedList

default_log = logging.getLogger("dynatrace")


class Dynatrace:
    def __init__(self, base_url: str, token: str, log: logging.Logger = default_log, proxies: Dict = None):
        self.__http_client = HttpClient(base_url, token, log, proxies)

    def get_entities(
        self, entity_selector: str, time_from: str = "now-2h", time_to: str = "now", fields: Optional[str] = None, page_size=50
    ) -> PaginatedList[Entity]:
        params = {"pageSize": page_size, "entitySelector": entity_selector, "from": time_from, "to": time_to, "fields": fields}
        return PaginatedList(Entity, self.__http_client, "/api/v2/entities", params, list_item="entities")

    def get_entity_types(self, page_size=50) -> PaginatedList[EntityType]:
        params = {"pageSize": page_size}
        return PaginatedList(EntityType, self.__http_client, "/api/v2/entityTypes", params, list_item="types")

    def query_metrics(
        self,
        metric_selector: str,
        page_size: int = None,
        resolution: str = None,
        time_from=None,
        time_to=None,
        entity_selector=None,
    ) -> PaginatedList[Metric]:
        params = {
            "pageSize": page_size,
            "metricSelector": metric_selector,
            "resolution": resolution,
            "from": time_from,
            "to": time_to,
            "entitySelector": entity_selector,
        }
        return PaginatedList(Metric, self.__http_client, "/api/v2/metrics/query", params, list_item="result")
