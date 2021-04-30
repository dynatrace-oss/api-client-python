from dynatrace.dynatrace_object import DynatraceObject


class METag(DynatraceObject):
    def _create_from_raw_data(self, raw_element: dict):
        self.context: str = raw_element.get("context")
        self.key: str = raw_element.get("key")
        self.value: str = raw_element.get("value")
        self.string_representation: str = raw_element.get("stringRepresentation")
