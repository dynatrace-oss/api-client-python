from datetime import datetime
from typing import List, Optional, Union, Dict, Any

from dynatrace.environment_v2.schemas import EntityType, ManagementZone
from dynatrace.http_client import HttpClient
from dynatrace.configuration_v1.metag import METag
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime, timestamp_to_string


class EntityService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        entity_selector: str,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None,
        fields: Optional[str] = None,
        sort: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> PaginatedList["Entity"]:
        """
        :return: A list of monitored entities along with their properties.
        """
        params = {
            "pageSize": page_size,
            "entitySelector": entity_selector,
            "from": timestamp_to_string(time_from),
            "to": timestamp_to_string(time_to),
            "fields": fields,
            "sort": sort,
        }
        return PaginatedList(Entity, self.__http_client, "/api/v2/entities", target_params=params, list_item="entities")

    def get(
        self, entity_id: str, time_from: Optional[Union[datetime, str]] = None, time_to: Optional[Union[datetime, str]] = None, fields: Optional[str] = None
    ) -> "Entity":
        params = {"from": timestamp_to_string(time_from), "to": timestamp_to_string(time_to), "fields": fields}
        response = self.__http_client.make_request(f"/api/v2/entities/{entity_id}", params=params).json()
        return Entity(raw_element=response)

    def post_custom_device(self, device: "CustomDeviceCreation"):
        # TODO - Implement
        pass

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
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.last_seen: Optional[datetime] = int64_to_datetime(raw_element.get("lastSeenTms", 0))
        self.first_seen: Optional[datetime] = int64_to_datetime(raw_element.get("firstSeenTms", 0))

        self.from_relationships: Dict[str, List["EntityId"]] = {
            key: [EntityId(raw_element=entity) for entity in entities] for key, entities in raw_element.get("fromRelationships", {}).items()
        }
        self.to_relationships: Dict[str, List["EntityId"]] = {
            key: [EntityId(raw_element=entity) for entity in entities] for key, entities in raw_element.get("toRelationships", {}).items()
        }
        self.management_zones: List[ManagementZone] = [ManagementZone(m) for m in raw_element.get("managementZones", [])]
        self.icon: Optional[EntityIcon] = EntityIcon(raw_element=raw_element.get("icon")) if raw_element.get("icon") else None
        self.display_name: str = raw_element.get("displayName")
        self.entity_id: str = raw_element.get("entityId")
        self.properties: Optional[Dict[str, Any]] = raw_element.get("properties", {})
        self.tags: List[METag] = [METag(raw_element=tag) for tag in raw_element.get("tags", [])]


class EntityShortRepresentation(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id = raw_element.get("id")
        self.name = raw_element.get("name")
        self.description = raw_element.get("description")


class EntityId(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.type: str = raw_element.get("type")


class EntityIcon(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.primary_icon_type = raw_element.get("primaryIconType")
        self.secondary_icon_type = raw_element.get("secondaryIconType")
        self.custom_icon_path = raw_element.get("customIconPath")


class CustomDeviceCreation:
    pass
