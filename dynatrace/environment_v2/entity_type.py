from dynatrace.dynatrace_object import DynatraceObject


class EntityType(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        # TODO - Implement other properties
        self.entity_type = raw_element.get("type")
        self.properties = raw_element.get("properties", [])
