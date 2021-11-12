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
from typing import Dict, Any, Union, List

from requests import Response

from dynatrace.http_client import HttpClient


class LogService:
    # TODO - Add search and get
    ENDPOINT = "/api/v2/logs"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def ingest(self, payload: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Response:
        """
        Ingests logs into the Dynatrace log store.
        :param payload: A list of log entries or a single log entry, which are JSON objects (dictionaries)
        :return: The HTTP Response
        """
        headers = {"Content-Type": "application/json; charset=utf-8"}
        return self.__http_client.make_request(f"{self.ENDPOINT}/ingest", params=payload, method="POST", headers=headers)
