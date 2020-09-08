from typing import List, Optional
from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.entity import EntityShortRepresentation
from dynatrace.tile import Tile


class DashboardFilter(DynatraceObject):
    @property
    def timeframe(self) -> str:
        return self._timeframe

    @property
    def management_zone(self) -> Optional[EntityShortRepresentation]:
        return self._management_zone

    def _create_from_raw_data(self, raw_element):
        self._timeframe = raw_element.get("timeframe")
        self._management_zone = (
            EntityShortRepresentation(self._http_client, None, raw_element.get("managementZone"))
            if raw_element.get("managementZone")
            else None
        )


class SharingInfo(DynatraceObject):
    @property
    def link_shared(self):
        return self._link_shared

    @property
    def published(self):
        return self.published

    def _create_from_raw_data(self, raw_element):
        self._link_shared = raw_element.get("linkShared")
        self._published = raw_element.get("published")


class DashboardMetadata(DynatraceObject):
    @property
    def name(self) -> str:
        return self._name

    @property
    def shared(self) -> bool:
        return self._shared

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def sharing_details(self) -> SharingInfo:
        return self._sharing_details

    @property
    def dashboard_filter(self):
        return self._dashboard_filter

    @property
    def tags(self) -> List[str]:
        return self._tags

    @property
    def preset(self) -> bool:
        return self._preset

    @property
    def valid_filter_keys(self) -> List[str]:
        return self._valid_filter_keys

    def _create_from_raw_data(self, raw_element):
        self._name = raw_element.get("name")
        self._shared = raw_element.get("shared")
        self._owner = raw_element.get("owner")
        self._sharing_details = SharingInfo(self._http_client, None, raw_element.get("sharingDetails"))
        self._dashboard_filter = DashboardFilter(self._http_client, None, raw_element.get("dashboardFilter"))
        self._tags = raw_element.get("tags")
        self._preset = raw_element.get("preset")
        self._valid_filter_keys = raw_element.get("validFilterKeys")


class Dashboard(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def dashboard_metadata(self) -> DashboardMetadata:
        return self._dashboard_metadata

    @property
    def tiles(self) -> List[Tile]:
        return self._tiles

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._dashboard_metadata = DashboardMetadata(self._http_client, None, raw_element.get("dashboardMetadata"))
        self._tiles = [Tile(self._http_client, None, raw_tile) for raw_tile in raw_element.get("tiles", [])]


class DashboardStub(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def owner(self) -> str:
        return self._owner

    def delete(self) -> Response:
        """
        Deletes this dashboard
        """
        return self._http_client.make_request(f"/api/config/v1/dashboards/{self.id}", method="DELETE")

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._owner = raw_element.get("owner")

    def get_full_dashboard(self) -> Dashboard:
        """
        Gets the full dashboard for this stub
        """
        response = self._http_client.make_request(f"/api/config/v1/dashboards/{self.id}").json()
        return Dashboard(self._http_client, None, response)
