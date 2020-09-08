from dynatrace.dynatrace_object import DynatraceObject


class Tile(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self._name = raw_element.get("name")
        self._tile_type = raw_element.get("tileType")  # TODO - This branches, maybe Tile is a subclass
        self._configured = raw_element.get("configured")
        self._bounds = raw_element.get("bounds")  # TODO - This is a TileBounds
        self._tile_filter = raw_element.get("tileFilter")  # TODO - This is a TileFilter
