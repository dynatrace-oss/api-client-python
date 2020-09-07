from requests import Response
from dynatrace.entity import EntityShortRepresentation
from dynatrace.endpoint import EndpointShortRepresentation
from dynatrace.pagination import PaginatedList


class PluginShortRepresentation(EntityShortRepresentation):
    def delete(self) -> Response:
        """
        Deletes the ZIP file of this plugin
        """
        return self._http_client.make_request(f"/api/config/v1/plugins/{self.id}/binary", method="DELETE")

    @property
    def endpoints(self) -> PaginatedList[EndpointShortRepresentation]:
        return PaginatedList(
            EndpointShortRepresentation,
            self._http_client,
            f"/api/config/v1/plugins/{self.id}/endpoints",
            None,
            list_item="values",
        )
