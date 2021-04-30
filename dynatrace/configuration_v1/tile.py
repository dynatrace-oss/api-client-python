from dynatrace.dynatrace_object import DynatraceObject


class Tile(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.name = raw_element.get("name")
        self.tile_type = raw_element.get("tileType")  # TODO - This branches, maybe Tile is a subclass
        self.configured = raw_element.get("configured")
        self.bounds = raw_element.get("bounds")  # TODO - This is a TileBounds
        self.tile_filter = raw_element.get("tileFilter")  # TODO - This is a TileFilter
