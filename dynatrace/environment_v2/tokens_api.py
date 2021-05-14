from typing import Union, Optional, List
from datetime import datetime

from requests import Response

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
from dynatrace.utils import timestamp_to_string, iso8601_to_datetime


SCOPE_INSTALLER_DOWNLOAD = "InstallerDownload"  # PaaS integration - Installer download.
SCOPE_DATA_EXPORT = "DataExport"  # Access problem and event feed, metrics, and topology.
SCOPE_PLUGIN_UPLOAD = "PluginUpload"  # Upload Extension.
SCOPE_SUPPORT_ALERT = "SupportAlert"  # PaaS integration - Support alert.
SCOPE_DCRUM_INTEGRATION = "DcrumIntegration"  # Dynatrace module integration - NAM.
SCOPE_ADVANCED_SYNTHETIC_INTEGRATION = "AdvancedSyntheticIntegration"  # Dynatrace module integration - Synthetic Classic.
SCOPE_EXTERNAL_SYNTHETIC_INTEGRATION = "ExternalSyntheticIntegration"  # Create and read synthetic monitors, locations, and nodes.
SCOPE_APP_MON_INTEGRATION = "AppMonIntegration"  # Dynatrace module integration - AppMon.
SCOPE_LOG_EXPORT = "LogExport"  # Read log content.
SCOPE_READ_CONFIG = "ReadConfig"  # Read configuration.
SCOPE_WRITE_CONFIG = "WriteConfig"  # Write configuration.
SCOPE_DTAQLAccess = "DTAQLAccess"  # User sessions.
SCOPE_USER_SESSION_ANONYMIZATION = "UserSessionAnonymization"  # Anonymize user session data for data privacy reasons.
SCOPE_DATA_PRIVACY = "DataPrivacy"  # Change data privacy settings.
SCOPE_CAPTURE_REQUEST_DATA = "CaptureRequestData"  # Capture request data.
SCOPE_DAVIS = "Davis"  # Dynatrace module integration - Davis.
SCOPE_DSS_FILE_MANAGEMENT = "DssFileManagement"  # Mobile symbolication file management.
SCOPE_LOG_IMPORT = "LogImport"  # Log import.
SCOPE_RUM_JAVA_SCRIPT_TAG_MANAGEMENT = "RumJavaScriptTagManagement"  # Real user monitoring JavaScript tag management.
SCOPE_TENANT_TOKEN_MANAGEMENT = "TenantTokenManagement"  # Token management.
SCOPE_ACTIVEGATE_CERT_MANAGEMENT = "ActiveGateCertManagement"  # ActiveGate certificate management.
SCOPE_REST_REQUEST_FORWARDING = "RestRequestForwarding"  # Fetch data from a remote environment.
SCOPE_READ_SYNTHETIC_DATA = "ReadSyntheticData"  # Read synthetic monitors, locations, and nodes.
SCOPE_DATA_IMPORT = "DataImport"  # Data ingest, e.g.  # metrics and events.
SCOPE_AUDIT_LOG_READ = "auditLogs.read"  # Read audit logs.
SCOPE_METRICS_READ = "metrics.read"  # Read metrics.
SCOPE_METRICS_WRITE = "metrics.write"  # Write metrics.
SCOPE_ENTITIES_READ = "entities.read"  # Read entities.
SCOPE_ENTITIES_WRITE = "entities.write"  # Write entities.
SCOPE_PROBLEMS_READ = "problems.read"  # Read problems.
SCOPE_PROBLEMS_WRITE = "problems.write"  # Write problems.
SCOPE_NETWORK_ZONES_READ = "networkZones.read"  # Read network zones.
SCOPE_NETWORK_ZONES_WRITE = "networkZones.write"  # Write network zones.
SCOPE_ACTIVE_GATES_READ = "activeGates.read"  # Read ActiveGates.
SCOPE_ACTIVE_GATES_WRITE = "activeGates.write"  # Write ActiveGates.
SCOPE_CREDENTIAL_VAULT_READ = "credentialVault.read"  # Read credential vault entries.
SCOPE_CREDENTIAL_VAULT_WRITE = "credentialVault.write"  # Write credential vault entries.
SCOPE_EXTENSIONS_READ = "extensions.read"  # Read extensions.
SCOPE_EXTENSIONS_WRITE = "extensions.write"  # Write extensions.
SCOPE_EXTENSION_CONFIGURATIONS_READ = "extensionConfigurations.read"  # Read extension monitoring configurations.
SCOPE_EXTENSION_CONFIGURATIONS_WRITE = "extensionConfigurations.write"  # Write extension monitoring configurations.
SCOPE_EXTENSION_ENVIRONMENT_READ = "extensionEnvironment.read"  # Read extension environment configurations.
SCOPE_EXTENSION_ENVIRONMENT_WRITE = "extensionEnvironment.write"  # Write extension environment configurations.
SCOPE_METRICS_INGEST = "metrics.ingest"  # Ingest metrics.
SCOPE_SECURITY_PROBLEMS_READ = "securityProblems.read"  # Read security problems.
SCOPE_SECURITY_PROBLEMS_WRITE = "securityProblems.write"  # Write security problems.
SCOPE_SYNTHETIC_LOCATIONS_READ = "syntheticLocations.read"  # Read synthetic locations.
SCOPE_SYNTHETIC_LOCATIONS_WRITE = "syntheticLocations.write"  # Write synthetic locations.
SCOPE_TENANT_TOKEN_ROTATION_WRITE = "tenantTokenRotation.write"  # Tenant token rotation.
SCOPE_SLO_READ = "slo.read"  # Read SLO.
SCOPE_SLO_WRITE = "slo.write"  # Write SLO.
SCOPE_RELEASES_READ = "releases.read"  # Read releases.
SCOPE_API_TOKENS_READ = "apiTokens.read"  # Read API tokens.
SCOPE_API_TOKENS_WRITE = "apiTokens.write"  # Write API tokens.


class TokenService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        api_token_selector: Optional[str] = None,
        fields: Optional[str] = None,
        time_from: Optional[Union[str, datetime]] = None,
        time_to: Optional[Union[str, datetime]] = None,
        sort: Optional[str] = None,
    ) -> PaginatedList["ApiToken"]:

        params = {
            "apiTokenSelector": api_token_selector,
            "fields": fields,
            "from": timestamp_to_string(time_from),
            "to": timestamp_to_string(time_to),
            "sort": sort,
        }

        return PaginatedList(ApiToken, self.__http_client, "/api/v2/apiTokens", params, list_item="apiTokens")

    def get(self, token_id: str):
        response = self.__http_client.make_request(f"/api/v2/apiTokens/{token_id}", method="GET")
        return ApiToken(raw_element=response.json())

    def delete(self, token_id: str) -> Response:
        return self.__http_client.make_request(f"/api/v2/apiTokens/{token_id}", method="DELETE")

    def create(
        self, name: str, scopes: List[str], personal_access_token: Optional[bool] = None, expiration_date: Optional[Union[datetime, str]] = None
    ) -> "ApiTokenCreated":

        body = {"personalAccessToken": personal_access_token, "expirationDate": expiration_date, "name": name, "scopes": scopes}

        response = self.__http_client.make_request("/api/v2/apiTokens", method="POST", params=body)
        return ApiTokenCreated(raw_element=response.json())

    def lookup(self, token: str):
        response = self.__http_client.make_request("/api/v2/apiTokens/lookup", method="POST", params={"token": token})
        return ApiToken(raw_element=response.json())


class ApiToken(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.last_used_date: Optional[datetime] = iso8601_to_datetime(raw_element.get("lastUsedDate"))
        self.last_used_ip_address: str = raw_element.get("lastUsedIpAddress")
        self.personal_access_token: bool = raw_element.get("personalAccessToken", False)
        self.expiration_date: Optional[datetime] = iso8601_to_datetime(raw_element.get("expirationDate"))
        self.creation_date: Optional[datetime] = iso8601_to_datetime(raw_element.get("creationDate"))
        self.name: str = raw_element.get("name")
        self.id: str = raw_element.get("id")
        self.owner: str = raw_element.get("owner")
        self.scopes: List[str] = raw_element.get("scopes", [])
        self.enabled: bool = raw_element.get("enabled")

    def delete(self):
        return self._http_client.make_request(f"/api/v2/apiTokens/{self.id}", method="DELETE")

    def __repr__(self):
        return f"ApiToken(id={self.id}, owner={self.owner}, name={self.name})"


class ApiTokenCreated(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.token: str = raw_element.get("token")
        self.expiration_date: Optional[datetime] = iso8601_to_datetime(raw_element.get("expirationDate"))
        self.id: str = raw_element.get("id")
