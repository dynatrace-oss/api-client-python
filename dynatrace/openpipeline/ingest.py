"""
Copyright 2026 Dynatrace LLC

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

from typing import Any, Dict, List

from requests import Response

from dynatrace.http_client import HttpClient


class OpenPipelineService:
    SMARTSCAPE_ENDPOINT = "/platform/ingest/v1/smartscape.events"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def smartscape_eventv1_ingest(self, events: List[Dict[str, Any]]):
        return self.__http_client.make_request(self.SMARTSCAPE_ENDPOINT, params=events, method="POST")
