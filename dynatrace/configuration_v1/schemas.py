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


from enum import Enum
from typing import List, Dict, Any, Optional

from dynatrace.dynatrace_object import DynatraceObject

# Schemas that don't belong to a specific API tag.


class UpdateWindowsConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.windows: List[UpdateWindow] = [UpdateWindow(raw_element=uw) for uw in raw_element.get("windows", [])]

    def to_json(self) -> Dict[str, Any]:
        return {"windows": [w.to_json for w in self.windows]}


class UpdateWindow(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.name: Optional[str] = raw_element.get("name", "")

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
        }


class AutoUpdateSetting(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    INHERITED = "INHERITED"

    def __str__(self):
        return self.value


class EffectiveSetting(Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"

    def __str__(self):
        return self.value
