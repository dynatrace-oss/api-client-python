from abc import ABC, abstractmethod
from base64 import b64encode
from typing import List, Optional

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class CredentialVaultService:
    _ENDPOINT = "/api/config/v1/credentials"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList["CredentialsResponseElement"]:
        """
        Lists all sets of credentials stored in your environment

        Required Api-Token scope:
            credentialVault.read (Read credential vault entries)
        """
        return PaginatedList(CredentialsResponseElement, self.__http_client, self._ENDPOINT, list_item="credentials")

    def post(self, credential: "Credentials"):
        response = self.__http_client.make_request(path=self._ENDPOINT,
                                                  params=credential.to_json(),
                                                  method="POST")

        return CredentialsResponseElement(raw_element=response.json())



class CredentialUsageHandler(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.type: str = raw_element.get("type", "")
        self.count: int = raw_element.get("count", 0)


class CredentialsResponseElement(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.name: str =  raw_element.get("name", "")
        self.id: str = raw_element.get("id", "")
        self.type: str = raw_element.get("type", "")
        self.description: str = raw_element.get("description", "")
        self.owner: str = raw_element.get("owner", "")
        self.owner_access_only = raw_element.get("ownerAccessOnly", False)
        self.scope: str = raw_element.get("scope", "")
        self.credential_usage_summary: List[CredentialUsageHandler] = [CredentialUsageHandler(raw_element=summary) for summary in raw_element.get("credentialUsageSummary", [])]


class Credentials(ABC):
    def __init__(self,
                 name: str,
                 scope: str,
                 description: Optional[str] = None,
                 owner_access_only: Optional[bool] = False,
                 credential_type: Optional[str] = None):
        self.name: str = name
        self.scope: str = scope
        self.description: Optional[str] = description
        self.owner_access_only: Optional[bool] = owner_access_only
        self.type: Optional[str] = credential_type

    @abstractmethod
    def to_json(self) -> dict:
        pass


class PublicCertificateCredentials(Credentials):
    def __init__(self,
                 name: str,
                 scope: str,
                 certificate: str,
                 password: str,
                 certificate_format: str,
                 description: Optional[str] = None,
                 owner_access_only: Optional[bool] = False,
                 credential_type: Optional[str] = None):
        super().__init__(name, scope, description, owner_access_only, credential_type)
        self.certificate: str = b64encode(certificate.encode()).decode()

        self.password: str = password
        self.certificate_format: str = certificate_format

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "scope": self.scope,
            "description": self.description,
            "ownerAccessOnly": self.owner_access_only,
            "type": self.type,
            "certificate": self.certificate,
            "password": self.password,
            "certificateFormat": self.certificate_format
        }
