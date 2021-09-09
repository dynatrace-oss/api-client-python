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

from datetime import datetime
from enum import Enum
from requests import Response
from typing import List, Optional, Union, Dict, Any

from dynatrace.environment_v2.schemas import ManagementZone
from dynatrace.environment_v2.custom_tags import METag
from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime, timestamp_to_string


class EntityService:
    ENDPOINT_ENTITIES = "/api/v2/entities"
    ENDPOINT_TYPES = "/api/v2/entityTypes"

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
        """Gets the information about monitored entities.

        Lists entities observed within the specified timeframe along with their properties.
        When you query entities of the SERVICE_METHOD type, only the following requests are returned:
            - Key requests
            - Top X requests that are used for baselining
            - Requests that have caused a problem

        :param page_size: The amount of entities per page. If not set, 50 is used.
        :param entity_selector: Defines the scope of the query. Only entities matching the specified criteria are included into response.
                                You must set one of these criteria:
                                    - Entity type: type("TYPE")
                                    - Dynatrace entity ID: entityId("id"). Several IDs can be separated by a comma (entityId("id-1","id-2")).
                                The length of the string is limited to 10,000 characters.
        :param time_from: The start of the requested timeframe. If not set, the relative timeframe of three days is used (now-3d).
        :param time_to: The end of the requested timeframe. If not set, the current timestamp is used.
        :param fields: Defines the list of entity properties included in the response. The ID and the name of an entity are always included to the response.
        :param sort: Defines the ordering of the entities returned. Currently ordering is only available for the display name (for example sort=name or sort =+name for ascending, sort=-name for descending)

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
        return PaginatedList(Entity, self.__http_client, self.ENDPOINT_ENTITIES, target_params=params, list_item="entities")

    def get(
        self, entity_id: str, time_from: Optional[Union[datetime, str]] = None, time_to: Optional[Union[datetime, str]] = None, fields: Optional[str] = None
    ) -> "Entity":
        """Gets the properties of the specified monitored entity.

        :param entity_id: The ID of the required entity.
        :param time_from: The start of the requested timeframe. If not set, the relative timeframe of three days is used (now-3d).
        :param time_to: The end of the requested timeframe. If not set, the current timestamp is used.
        :param fields: Defines the list of entity properties included in the response. The ID and the name of an entity are always included to the response.

        :returns Entity: the monitored entity requested
        """
        params = {"from": timestamp_to_string(time_from), "to": timestamp_to_string(time_to), "fields": fields}
        response = self.__http_client.make_request(f"{self.ENDPOINT_ENTITIES}/{entity_id}", params=params).json()
        return Entity(raw_element=response)

    def post_custom_device(self, device: "CustomDeviceCreation") -> "Response":
        """Creates or updates a custom device.

        If the Custom Device ID matches an existing device, the respective parameters will be updated.

        :returns Response: HTTP Response for the request
        """
        return device.post()

    def create_custom_device(
        self,
        custom_device_id: str,
        display_name: str,
        group: Optional[str] = None,
        ip_addresses: Optional[List[str]] = None,
        listen_ports: Optional[List[int]] = None,
        device_type: Optional[str] = None,
        favicon_url: Optional[str] = None,
        config_url: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
        dns_names: Optional[List[str]] = None,
        message_type: Optional["MessageType"] = None,
    ) -> "CustomDeviceCreation":
        """Creates a Custom Device object from scratch.

        :param custom_device_id: The internal ID of the custom device. Max. length 512.
        :param display_name: The name of the custom device to be displayed in the user interface.
        :param group: User defined group ID of entity.
        :param ip_addresses: The list of IP addresses that belong to the custom device.
        :param listen_ports: The list of ports the custom devices listens to.
        :param device_type: The technology type definition of the custom device.
        :param favicon_url: The icon to be displayed for your custom component within Smartscape. Provide the full URL of the icon file.
        :param config_url: The URL of a configuration web page for the custom device, such as a login page for a firewall or router.
        :param properties: Key-value pair properties that will be shown beneath the infographics of your custom device.
        :param dns_names: The list of DNS names related to the custom device.
        :param message_type: Use the Enum for possible values

        :returns CustomDeviceCreation: The resulting Custom Device. This can now be used in POST calls.
        """
        raw_device = {
            "customDeviceId": custom_device_id,
            "displayName": display_name,
            "group": group,
            "ipAddresses": ip_addresses,
            "listenPorts": listen_ports,
            "type": device_type,
            "faviconUrl": favicon_url,
            "configUrl": config_url,
            "properties": properties,
            "dnsNames": dns_names,
            "messageType": message_type,
        }
        return CustomDeviceCreation(raw_element=raw_device, http_client=self.__http_client)

    def list_types(self, page_size: Optional[int] = 50) -> PaginatedList["EntityType"]:
        """
        Gets a list of properties for all entity types

        :param page_size: The amount of entity types in a single response payload.
            The maximal allowed page size is 500.
            If not set, 50 is used.
        :return: A list of properties of all available entity types.
        """
        params = {"pageSize": page_size}
        return PaginatedList(EntityType, self.__http_client, self.ENDPOINT_TYPES, params, list_item="types")

    def get_types(self, entity_type: str) -> "EntityType":
        """Gets the properties of a specified entity type.

        :param entity_type: The entity type required

        :returns EntityType: The properties of the specified entity type.
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT_TYPES}/{entity_type}")
        return EntityType(raw_element=response.json())


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
        self.display_name: str = raw_element["displayName"]
        self.entity_id: str = raw_element["entityId"]
        self.properties: Optional[Dict[str, Any]] = raw_element.get("properties", {})
        self.tags: List[METag] = [METag(raw_element=tag) for tag in raw_element.get("tags", [])]


class EntityShortRepresentation(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id = raw_element.get("id")
        self.name = raw_element.get("name")
        self.description = raw_element.get("description")

    def to_json(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name, "description": self.description}


class EntityStub(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.entity_id: EntityId = EntityId(raw_element=raw_element["entityId"])
        self.name: str = raw_element["name"]

    def to_json(self) -> Dict[str, Any]:
        return {"entityId": self.entity_id.to_json(), "name": self.name}


class EntityId(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element["id"]
        self.type: str = raw_element["type"]

    def to_json(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type}


class EntityIcon(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.primary_icon_type = raw_element.get("primaryIconType")
        self.secondary_icon_type = raw_element.get("secondaryIconType")
        self.custom_icon_path = raw_element.get("customIconPath")


class CustomDeviceCreation(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.custom_device_id: str = raw_element["customDeviceId"]
        self.display_name: str = raw_element["displayName"]
        self.group: Optional[str] = raw_element.get("group")
        self.ip_addresses: Optional[List[str]] = raw_element.get("ipAddresses")
        self.listen_ports: Optional[List[int]] = raw_element.get("listenPorts")
        self.type: Optional[str] = raw_element.get("type")
        self.favicon_url: Optional[str] = raw_element.get("faviconUrl")
        self.config_url: Optional[str] = raw_element.get("configUrl")
        self.properties: Optional[Dict[str, str]] = raw_element.get("properties")
        self.dns_names: Optional[List[str]] = raw_element.get("dnsNames")
        self.message_type: Optional[MessageType] = MessageType(raw_element.get("messageType"))

    def to_json(self):
        return {
            "customDeviceId": self.custom_device_id,
            "displayName": self.display_name,
            "group": self.group,
            "ipAddresses": self.ip_addresses,
            "listenPorts": self.listen_ports,
            "type": self.type,
            "faviconUrl": self.favicon_url,
            "configUrl": self.config_url,
            "properties": self.properties,
            "dnsNames": self.dns_names,
            "messageType": str(self.message_type),
        }

    def post(self) -> "Response":
        return self._http_client.make_request(path=f"{EntityService.ENDPOINT_ENTITIES}/custom", method="POST", params=self.to_json())


class EntityType(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        self.type: str = raw_element["type"]
        self.display_name: str = raw_element["displayName"]
        self.entity_limit_exceeded: bool = raw_element.get("entityLimitExceeded", False)
        self.properties: Optional[List[EntityTypePropertyDto]] = [EntityTypePropertyDto(raw_element=p) for p in raw_element.get("properties", [])]
        self.from_relationships: Optional[List[FromPosition]] = [FromPosition(raw_element=fr) for fr in raw_element.get("fromRelationships", [])]
        self.to_relationships: Optional[List[ToPosition]] = [ToPosition(raw_element=tr) for tr in raw_element.get("toRelationships", [])]
        self.dimension_key: Optional[str] = raw_element.get("dimensionKey")
        self.management_zones: Optional[str] = raw_element.get("managementZones")
        self.tags: Optional[str] = raw_element.get("tags")


class EntityTypePropertyDto(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element["id"]
        self.type: str = raw_element["type"]
        self.display_name: Optional[str] = raw_element.get("displayName")


class ToPosition(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.from_types: List[str] = raw_element["fromTypes"]
        self.id: str = raw_element["id"]


class FromPosition(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.to_types: List[str] = raw_element["toTypes"]
        self.id: str = raw_element["id"]


class MessageType(Enum):
    CUSTOM_DEVICE = "CUSTOM_DEVICE"
    DELETE_ENTITY_PER_TYPE = "DELETE_ENTITY_PER_TYPE"
    FILTER_VALUE_SUGGESTIONS = "FILTER_VALUE_SUGGESTIONS"
    MULTI = "MULTI"
    MULTI_TYPE = "MULTI_TYPE"
    SINGLE = "SINGLE"
    SINGLE_TYPE = "SINGLE_TYPE"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
