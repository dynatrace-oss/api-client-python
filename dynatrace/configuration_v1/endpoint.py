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

from requests import Response
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation


class EndpointShortRepresentation(EntityShortRepresentation):
    def delete(self, plugin_id: str) -> Response:
        """
        Deletes this endpoint
        """
        return self._http_client.make_request(f"/api/config/v1/plugins/{plugin_id}/endpoints/{self.id}", method="DELETE")
