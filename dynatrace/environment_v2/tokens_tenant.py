from typing import Dict, Any, Optional
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient


class TenantTokenService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def cancel_rotation(self) -> "TenantTokenConfig":
        return TenantTokenConfig(raw_element=self.__http_client.make_request("/api/v2/tenantTokenRotation/cancel", method="POST").json())

    def start_rotation(self) -> "TenantTokenConfig":
        return TenantTokenConfig(raw_element=self.__http_client.make_request("/api/v2/tenantTokenRotation/start", method="POST").json())

    def finish_rotation(self) -> "TenantTokenConfig":
        return TenantTokenConfig(raw_element=self.__http_client.make_request("/api/v2/tenantTokenRotation/finish", method="POST").json())


class TenantTokenConfig(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.active: Optional[TenantToken] = TenantToken(raw_element=raw_element.get("active"))
        self.old: Optional[TenantToken] = TenantToken(raw_element=raw_element.get("old"))


class TenantToken(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.value: str = raw_element.get("value")
