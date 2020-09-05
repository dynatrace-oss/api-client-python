from datetime import datetime
from typing import List

from dynatrace.management_zone import ManagementZone
from dynatrace.metag import METag
from dynatrace.dynatrace_object import DynatraceObject


class Entity(DynatraceObject):
    @property
    def from_relationships(self):
        # TODO
        return ""

    @property
    def to_relationships(self):
        # TODO
        return ""

    @property
    def first_seen_t_ms(self) -> datetime:
        # TODO
        """
        The timestamp at which the entity was first seen, in UTC milliseconds.
        :return:
        """
        return datetime.now()

    @property
    def last_seen_t_ms(self) -> datetime:
        # TODO
        """
        The timestamp at which the entity was last seen, in UTC milliseconds.
        :return:
        """
        return datetime.now()

    @property
    def entity_id(self) -> str:
        """
        The ID of the entity.
        :return:
        """
        return self._entity_id

    @property
    def display_name(self) -> str:
        """
        The name of the entity, displayed in the UI.
        :return:
        """
        return self._display_name

    @property
    def management_zones(self) -> List[ManagementZone]:
        return []

    @property
    def tags(self) -> List[METag]:
        return []

    @property
    def properties(self) -> List[dict]:
        return self._properties

    def _create_from_raw_data(self, raw_element: dict):
        self._display_name = raw_element.get("displayName")
        self._entity_id = raw_element.get("entityId")
        self._properties = raw_element.get("properties", [])
