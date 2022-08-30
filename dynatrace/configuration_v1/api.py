from dynatrace.configuration_v1.geographic_regions import GeoRegionsIpAddressMappingsService
from dynatrace.http_client import HttpClient


class ConfigurationV1:
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

        self.geo_regions_ip_address_mappings = GeoRegionsIpAddressMappingsService(http_client)
