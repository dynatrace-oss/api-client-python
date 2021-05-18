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

from dynatrace.dynatrace_object import DynatraceObject


class Tile(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.name = raw_element.get("name")
        self.tile_type = raw_element.get("tileType")  # TODO - This branches, maybe Tile is a subclass
        self.configured = raw_element.get("configured")
        self.bounds = raw_element.get("bounds")  # TODO - This is a TileBounds
        self.tile_filter = raw_element.get("tileFilter")  # TODO - This is a TileFilter
