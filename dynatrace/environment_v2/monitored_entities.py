from typing import List, Optional

from dynatrace.environment_v2.schemas import EntityType
from dynatrace.http_client import HttpClient
from dynatrace.configuration_v1.metag import METag
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList


class EntityService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        entity_selector: str,
        time_from: str = "now-2h",
        time_to: str = "now",
        fields: Optional[str] = None,
        page_size=50,
    ) -> PaginatedList["Entity"]:
        """
        :return: A list of monitored entities along with their properties.
        """
        params = {"pageSize": page_size, "entitySelector": entity_selector, "from": time_from, "to": time_to, "fields": fields}
        return PaginatedList(Entity, self.__http_client, "/api/v2/entities", params, list_item="entities")

    def list_types(self, page_size=50) -> PaginatedList[EntityType]:
        """
        Gets a list of properties for all entity types

        :param page_size: The desired amount of entities in a single response payload.
            The maximal allowed page size is 500.
            If not set, 50 is used.
        :return: A list of properties of all available entity types.
        """
        params = {"pageSize": page_size}
        return PaginatedList(EntityType, self.__http_client, "/api/v2/entityTypes", params, list_item="types")


class Entity(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        # TODO - Implement rest of properties
        self.display_name = raw_element.get("displayName")
        self.entity_id = raw_element.get("entityId")
        self.properties = raw_element.get("properties", {})
        self.tags: List[METag] = [METag(raw_element=tag) for tag in raw_element.get("tags", {})]


class EntityShortRepresentation(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id = raw_element.get("id")
        self.name = raw_element.get("name")
        self.description = raw_element.get("description")
