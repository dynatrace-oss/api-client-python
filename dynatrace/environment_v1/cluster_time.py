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

from datetime import datetime

from dynatrace.http_client import HttpClient


class ClusterTimeService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def time(self) -> datetime:
        return datetime.utcfromtimestamp(float(self.__http_client.make_request("/api/v1/time").text) / 1000)
