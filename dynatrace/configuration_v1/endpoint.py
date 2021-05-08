from requests import Response
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation


class EndpointShortRepresentation(EntityShortRepresentation):
    def delete(self, plugin_id: str) -> Response:
        """
        Deletes this endpoint
        """
        return self._http_client.make_request(f"/api/config/v1/plugins/{plugin_id}/endpoints/{self.id}", method="DELETE")
