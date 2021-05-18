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

import pprint
from typing import Optional, Dict, Any

from requests import Response

from dynatrace.http_client import HttpClient


class DynatraceObject:
    def __init__(self, http_client: Optional[HttpClient] = None, headers: Optional[Dict[str, str]] = None, raw_element: Optional[Dict[str, Any]] = None):
        if raw_element is None:
            raw_element = {}
        self._http_client = http_client
        self._headers = headers
        self._raw_element = raw_element
        self._create_from_raw_data(raw_element)

    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({pprint.pformat(self._raw_element, width=130)})"

    def _make_request(self, path: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, method="GET", data=None) -> Response:
        return self._http_client.make_request(path, params, headers, method, data)
