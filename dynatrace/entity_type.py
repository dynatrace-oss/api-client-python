from typing import List

from dynatrace.management_zone import ManagementZone
from dynatrace.metag import METag
from dynatrace.dynatrace_object import DynatraceObject


class EntityType(DynatraceObject):
    @property
    def from_relationships(self):
        return ""

    @property
    def to_relationships(self):
        return ""

    @property
    def type(self) -> str:
        """
        The name of the entity, displayed in the UI.
        :return:
        """
        return self._entity_type

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
        self._entity_type = raw_element.get("type")
        self._properties = raw_element.get("properties", [])
