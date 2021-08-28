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
from dynatrace.dynatrace_object import DynatraceObject
from typing import List, Optional, Union, Dict, Any

from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class NetworkZoneService:
    ENDPOINT = "/api/v2/networkZones"
    ENDPOINT_GLOBALSETTINGS = "/api/v2/networkZoneSettings"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList["NetworkZone"]:
        """Lists all network zones. No params

        :return: a list of Network Zones with details
        """
        return PaginatedList(NetworkZone, self.__http_client, target_url=self.ENDPOINT, list_item="networkZones")

    def get(self, networkzone_id: str):
        """Gets parameters of specified network zone

        :param networkzone_id: the ID of the network zone
        :return: a Network Zone + details
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{networkzone_id}").json()
        return NetworkZone(raw_element=response)

    def update(self, networkzone_id: str, alternate_zones: Optional[List[str]] = None, description: Optional[str] = None):
        """Updates an existing network zone or creates a new one

        :param networkzone_id: the ID of the network zone, if none exists, will create
        :param alternate_zones: optional list of text body of alternative network zones
        :param description: optional text body for short description of network zone
        :return: HTTP response
        """
        params = {"alternativeZones": alternate_zones, "description": description}
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{networkzone_id}", params=params, method="PUT")

    def delete(self, networkzone_id: str):
        """Deletes the specified network zone

        :param networkzone_id: the ID of the network zone
        :return: HTTP response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{networkzone_id}", method="DELETE")

    def getGlobalConfig(self):
        """Gets the global configuration of network zones. No params
        :return: Network Zone Global Settings object
        """
        response = self.__http_client.make_request(path=self.ENDPOINT_GLOBALSETTINGS).json()
        return NetworkZoneSettings(raw_element=response)

    def updateGlobalConfig(self, configuration: bool):
        """Updates the global configuration of network zones.

        :param configuration: boolean setting to enable/disable NZs
        :return: HTTP response
        """
        params = {"networkZonesEnabled": configuration}
        return self.__http_client.make_request(path=self.ENDPOINT_GLOBALSETTINGS, method="PUT", params=params)


class NetworkZone(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.id: str = raw_element.get("id")
        self.description: str = raw_element.get("description")
        self.alternative_zones: List[str] = raw_element.get("alternativeZones")
        self.num_oneagents_using: int = raw_element.get("numOfOneAgentsUsing")
        self.num_oneagents_configured: int = raw_element.get("numOfConfiguredOneAgents")
        self.num_oneagents_from_other_zones: int = raw_element.get("numOfOneAgentsFromOtherZones")
        self.num_configured_activegates: int = raw_element.get("numOfConfiguredActiveGates")


class NetworkZoneSettings(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, bool]):
        self.network_zones_enabled: bool = raw_element.get("networkZonesEnabled")
